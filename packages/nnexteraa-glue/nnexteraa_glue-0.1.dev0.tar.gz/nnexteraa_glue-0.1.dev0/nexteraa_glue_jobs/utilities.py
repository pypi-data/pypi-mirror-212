import json
from datetime import datetime

from awsglue.dynamicframe import DynamicFrame
from awsglue.gluetypes import NullType, StructType, DecimalType, ChoiceType, StringType, DynamicRecord


def decide_datatype(choices: dict):
    """
    Logic to determine the ~preferred~ DataType given multiple DataType choices. This will be used when building the
    specs used in the `DynamicFrame.resolveChoice()` method.
    """
    if "date" in choices and "timestamp" in choices:
        return "timestamp"
    elif "float" in choices and "double" in choices:
        return "double"
    elif "int" in choices and "long" in choices:
        return "long"
    else:
        # last resort
        return "string"


def get_json(input_str):
    return json.loads(input_str or '{}')


def build_path_name(path_prefix, field_name):
    if path_prefix:
        return f"{path_prefix}.{field_name}"
    else:
        return field_name


def find_datatype(field, specs, custom_input_datatypes, path_prefix=None):
    path_name = build_path_name(path_prefix, field.name)
    if field.name in custom_input_datatypes:
        spec = (path_name, f"cast:{custom_input_datatypes[field.name]}")
        specs.append(spec)
    elif isinstance(field.dataType, ChoiceType):
        datatype = decide_datatype(field.dataType.choices)
        spec = (path_name, f"cast:{datatype}")
        specs.append(spec)
    elif isinstance(field.dataType, StructType):
        specs.extend(build_specs(field.dataType, path_name, custom_input_datatypes=custom_input_datatypes))


def build_specs(schema: StructType, path_prefix=None, custom_input_datatypes={}):
    """
    Recursive function that iterates through a DynamicFrame schema, which is a list of possibly nested data types, and
    builds a list of specs. Specs are a list of specific ambiguities to resolve, with each spec in the form of a
    tuple:(path, action).
    The path identifies a specific column name, and the action casts the column to the datatype decided upon by the
    `decide_datatype` function.
    """
    specs = []
    for field in schema:
        find_datatype(field, specs, custom_input_datatypes, path_prefix=path_prefix)
    return specs


def resolve_datatype_choices(dynf: DynamicFrame, transformation_ctx="", custom_input_datatypes={}) -> DynamicFrame:
    """
    DynamicFrames reference the Glue Data Catalog to determine the schema. But because Glue crawlers only read 2MB of
    data to determine column types, a dataset containing many NULL values could actually contain more complex DataTypes.
    The Spark DataFrame API however considers the whole dataset and therefore resorts to the most general DataType when
    there are complex types or variations of data.
    This method handles cases where the DynamicFrame schema contains multiple choices of DataTypes and casts the column
    to the more general data type determined by the `decide_datatype` method.
    """
    specs = build_specs(dynf.schema(), custom_input_datatypes=custom_input_datatypes)
    if specs:
        dynf = dynf.resolveChoice(specs=specs, transformation_ctx=transformation_ctx)
    return dynf


def field_to_resolve_spec(field):
    """Given a field structure, return the equivalent DynamicFrame.resolveChoice spec."""
    type_str = field.dataType.typeName()
    if isinstance(field.dataType, DecimalType):
        type_str = f"{field.dataType.typeName()}({field.dataType.precision},{field.dataType.scale})"
    return field.name, f"cast:{type_str}"


def fix_null_types(output_dynf: DynamicFrame, schema: StructType):
    """Repair null field types in the given DynamicFrame using the field types in the given schema."""
    null_type_fields = [f.name for f in output_dynf.schema() if isinstance(f.dataType, NullType)]
    if null_type_fields:
        input_fields = {f.name: f for f in schema}
        specs = [field_to_resolve_spec(input_fields[n]) for n in null_type_fields]
        return output_dynf.resolveChoice(specs)
    else:
        return output_dynf


def null_safe_map(input_dynf, f, transformation_ctx='schema_stable_map'):
    """Map a function over a DynamicFrame without altering the types of fields that contain only null values."""
    return fix_null_types(
        input_dynf.map(f, transformation_ctx=transformation_ctx),
        input_dynf.schema()
    )


def fill_null_strings(dynf: DynamicFrame, glue_context) -> DynamicFrame:
    """
    In Spark <=2.4, when saving the contents of a DataFrame in JSON format, any string column that contains ONLY null
    values will be excluded in the JSON output.  By converting the null values to empty strings, this forces Spark to
    include the column in the JSON output.
    In Spark >=3.0, this utility function can be deprecated in favor of setting the `ignoreNullFields` parameter to
    false in the DataFrameWriter.json() method.
    https://spark.apache.org/docs/3.0.0/api/python/pyspark.sql.html#pyspark.sql.DataFrameWriter.json
    :param dynf: awsglue.dynamicframe.DynamicFrame to transform.
    :param glue_context: The GlueContext Class object that specifies the context for this transform.
    :return: awsglue.dynamicframe.DynamicFrame
    """

    # Define list of columns that are StringType
    string_type_fields = [f.name for f in dynf.schema() if isinstance(f.dataType, StringType)]

    if string_type_fields:
        # Fill nulls with empty string
        df = dynf.toDF().na.fill(value='', subset=string_type_fields)
        dynf = DynamicFrame.fromDF(df, glue_context, 'fill_null_strings')
    return dynf


iso_8601_no_tz_format = f"%Y-%m-%dT%H:%M:%S.%f"
iso_8601_format = f"{iso_8601_no_tz_format}%z"
date_format = "%Y-%m-%d"


def get_datetime(input_str,
                 input_format=iso_8601_format,
                 output_format=iso_8601_format,
                 default_time=datetime.utcnow()):
    try:
        if input_str and input_str.lower() != 'none':
            return datetime.strptime(input_str, input_format).strftime(output_format)
    except ValueError:
        pass

    return default_time.strftime(output_format)


def get_date_iso_8601(input_str, default_time=datetime.utcnow()):
    """Given an input str possibly containing a datetime in ISO-8601 format, return a date string."""
    return get_datetime(input_str, iso_8601_format, date_format, default_time)


def get_timestamp_iso_8601(input_str, default_time=datetime.utcnow()):
    """Given an input str possibly containing a datetime in ISO-8601 format, return a timestamp string."""
    return get_datetime(input_str, iso_8601_format, iso_8601_no_tz_format, default_time)


def add_columns(columns_to_values_dict, dyn_rec: DynamicRecord):
    dyn_rec.update(columns_to_values_dict)
    return dyn_rec


def add_date_column(column_name, column_value, dyn_rec: DynamicRecord):
    return add_columns({
        column_name: column_value
    }, dyn_rec)


def py4j_java_error_to_class_name(java_error):
    if java_error.java_exception.getCause():
        return java_error.java_exception.getCause().getClass().getName()
    else:
        # AttributeError: 'NoneType' object has no attribute 'getClass'
        return java_error.java_exception
