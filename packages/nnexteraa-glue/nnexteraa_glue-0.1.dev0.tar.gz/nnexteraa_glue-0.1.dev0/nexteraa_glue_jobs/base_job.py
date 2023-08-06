from abc import abstractmethod, ABC
from enum import EnumMeta

from py4j.protocol import Py4JJavaError
from pyspark.context import SparkContext

from utilities import py4j_java_error_to_class_name, get_json
from allied_glue_jobs.exceptions import EntityNotFoundException
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection
from awsglue.job import Job
from awsglue.utils import getResolvedOptions


def as_list(value):
    """
    Given a value, if it's a list return it, otherwise return a single-element list containing the value.
    """
    return value if isinstance(value, list) else list([value])


def enums_to_values(enums: list):
    """
    Given a list of enums, return a flattened list of the string values of those enums.
    """
    output = []
    for enum in enums:
        if isinstance(enum, EnumMeta):
            output.extend([p.value for p in enum])
        else:
            raise NotImplementedError(
                f"Value must be an enum. Type '{type(enum)}' is not supported.")
    return output


def generate_defaults(argv, parameters):
    """
    Given a list of provided arguments ('argv') and parameters, return a list
     of argument + '' for any parameter not found.
    """
    output = []
    for parameter in parameters:
        parameter_string = f"--{parameter}"
        if parameter_string not in argv:
            output += [parameter_string, ""]
    return output


class BaseJob(ABC):

    @property
    def job_options(self):
        return []

    @property
    def required_parameters(self):
        return []

    @property
    def optional_parameters(self):
        return []

    def __init__(self, argv):
        # Gather job parameters, folding the deprecated 'job_options' into 'required_parameters'
        _required_parameters = self.get_required_parameters()
        _optional_parameters = self.get_optional_parameters()
        all_parameters = _required_parameters + _optional_parameters

        # Generate any necessary default values to satisfy Glue's internal 'argparse.ArgumentParser'
        argv_defaults = generate_defaults(argv, _optional_parameters)
        argv_with_defaults = argv + argv_defaults

        # Use Glue's argument parsing, which in addition to being strict, will also de-conflict
        #  internal or special Glue arguments in case we pass those inadvertently.
        self.resolved_options = getResolvedOptions(argv_with_defaults, all_parameters)

        # Do the work of setting up the various Spark/Glue internal stuff
        self.spark_context = SparkContext.getOrCreate()
        self.glue_context = GlueContext(self.spark_context)
        self.logger = self.glue_context.get_logger()
        self.job = Job(self.glue_context)
        self.job_name = self.resolved_options["JOB_NAME"]

        # TODO: Remove this when we remove 'job_options'
        if self.job_options:
            self.logger.warn(
                "The 'BaseJob.job_options' property is deprecated and will be removed "
                "in a future release of 'allied_world_glue'. "
                "Please use 'BaseJob.required_parameters' and 'BaseJob.optional_parameters' instead.")

    def get_required_parameters(self):
        _job_options = as_list(self.job_options)
        _required_parameters = as_list(self.required_parameters)

        return ["JOB_NAME"] + enums_to_values(_job_options + _required_parameters)

    def get_optional_parameters(self):
        _optional_parameters = as_list(self.optional_parameters)
        return enums_to_values(_optional_parameters)

    def get_option(self, enum_member):
        return self.resolved_options[enum_member.value]

    def get_list_option(self, enum_member, separator=","):
        value = self.get_option(enum_member)
        if value:
            items = value.split(separator)
            return [i.strip() for i in items]
        else:
            return []

    def get_json_option(self, enum_member):
        value = self.get_option(enum_member)
        if value:
            return get_json(value)
        else:
            return dict

    def load_catalog_table(self, database: str, table: str, push_down_predicate: str = "",
                           additional_options: dict = {}) -> DynamicFrame:
        """
        Creates a DynamicFrame from loading a table from the Glue Data Catalog.
        push_down_predicate are only supported by data catalog table backed by S3
        and if no push_down_predicate is passed complete data is loaded

        :param database: Name of the Glue Data Catalog Database
        :param table: Name of the Glue Data Catalog Table
        :param push_down_predicate: Pre-Filters Table based on partition specified in push_down_predicate
        :param additional_options: Dictionary of additional options to pass to the 'from_catalog' method.
        :return: awsglue.dynamicframe.DynamicFrame
        """
        try:
            self.logger.info(f"Loading data from Glue Catalog source [{database}/{table}]")
            dynf = self.glue_context.create_dynamic_frame.from_catalog(
                database=database,
                table_name=table,
                transformation_ctx=f"load_{database}_{table}",
                push_down_predicate=push_down_predicate,
                additional_options=additional_options
            )
            self.logger.info(f"Finished loading data from [{database}/{table}]")

        except Py4JJavaError as e:
            error_class = py4j_java_error_to_class_name(e)
            if error_class is "com.amazonaws.services.glue.model.EntityNotFoundException":
                message = f"Glue Catalog Source [{database}/{table}] was not found!"
                self.logger.warn(message)
                raise EntityNotFoundException(message)
            else:
                raise e

        return dynf

    def load_catalog_table_without_ctx(self, database: str, table: str, push_down_predicate: str = "") -> DynamicFrame:
        """
        Creates a DynamicFrame from loading a table from the Glue Data Catalog
        purposely excluding a transformation context to avoid Glue job bookmarking for the data source
        push_down_predicate are only supported by data catalog table backed by S3
        and if no push_down_predicate is passed complete data is loaded

        :param database: Name of the Glue Data Catalog Database
        :param table: Name of the Glue Data Catalog Table
        :param push_down_predicate: Pre-Filters Table based on partition specified in push_down_predicate
        :return: awsglue.dynamicframe.DynamicFrame
        """
        try:
            self.logger.info(f"Loading data from Glue Catalog source [{database}/{table}]")
            dynf = self.glue_context.create_dynamic_frame.from_catalog(
                database=database,
                table_name=table,
                push_down_predicate=push_down_predicate
            )
            self.logger.info(f"Finished loading data from [{database}/{table}]")

        except Py4JJavaError as e:
            error_class = py4j_java_error_to_class_name(e)
            if error_class is "com.amazonaws.services.glue.model.EntityNotFoundException":
                message = f"Glue Catalog Source [{database}/{table}] was not found!"
                self.logger.warn(message)
                raise EntityNotFoundException(message)
            else:
                raise e

        return dynf

    def load_catalog_tables(self, database: str, tables: list, push_down_predicate: str = "") -> DynamicFrameCollection:
        """
        Creates a collection of DynamicFrames by loading tables from the Glue Data Catalog.
        push_down_predicate are only supported by data catalog table backed by S3
        and if no push_down_predicate is passed complete data is loaded

        :param database: Name of the Glue Data Catalog Database
        :param tables: List of Glue Data Catalog Tables
        :param push_down_predicate: Pre-Filters all Tables based on partition specified in push_down_predicate
        :return: awsglue.dynamicframe.DynamicFrameCollection
        """

        dynfs = {}
        for table in tables:
            dynfs[table] = self.load_catalog_table(database, table, push_down_predicate)

        return DynamicFrameCollection(dynfs, self.glue_context)

    @abstractmethod
    def body(self):
        pass

    def run(self):
        self.logger.info(f"Running job [{self.job_name}]")
        self.job.init(self.job_name, self.resolved_options)
        self.body()
        self.job.commit()
        self.logger.info(f"Finished running job [{self.job_name}]")
