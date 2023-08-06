from awsglue.context import GlueContext
from pyspark.context import SparkContext
from sedona.register import SedonaRegistrator

sc = SparkContext()
glueContext = GlueContext(sc)

# Create a SparkSession using the GlueContext
spark = glueContext.spark_session

logger = glueContext.get_logger()
SedonaRegistrator.registerAll(spark)

# Load spatial data
# states_wkt = spark.read \
#     .format("csv") \
#     .option("header", "true") \
#     .load("s3://glue-sedona/data/customers_database/country_csv/boundary-each-state.csv")

states_wkt = spark.read.option("delimiter", "\t").option("header", "false").csv("s3://glue-sedona/data/customers_database/country_csv/boundary-each-state.tsv").toDF("s_name","s_bound")
states_wkt.show()
states_wkt.printSchema()

states = states_wkt.selectExpr("s_name", "ST_GeomFromWKT(s_bound) as s_bound")
# states.show()
states.printSchema()
states.createOrReplaceTempView("states")

# cities_csv = spark.read \
#     .format("csv") \
#     .option("header", "true") \
#     .load("s3://glue-sedona/data/customers_database/country_csv/cities.csv")

cities_csv = spark.read.option("delimiter", ",").option("header", "false").csv("s3://glue-sedona/data/customers_database/country_csv/cities.csv").toDF("c_name","c_loc")
cities_csv.show()
cities_csv.printSchema()

cities = cities_csv.selectExpr("c_name", "ST_PointFromText(c_loc, \'_\') as c_loc")
# cities.show()
cities.printSchema()
cities.createOrReplaceTempView("cities")
city_per_state = spark.sql("select * from states s, cities c where ST_Contains(s.s_bound, c.c_loc)")
# city_per_state.show()
dist_to_seattle = spark.sql("select c_name, ST_Distance(c_loc, ST_Point(-122.313323, 47.622715)) as dist from cities")
# dist_to_seattle.show()
# geopandas_df = gpd.GeoDataFrame(states.toPandas(), geometry="s_bound")
# geopandas_df.printSchema()
# Stop the SparkSession
spark.stop()
