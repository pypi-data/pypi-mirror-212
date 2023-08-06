import os
from app.nexteraa_glue_jobs.base_job import BaseJob

class SedonaLogicJob2(BaseJob):
    def __init__(self, glueContext):
        super().__init__(glueContext)

    def body(self):
        # Load spatial data
        states_wkt_path = os.getenv("STATES_WKT_S3_PATH")
        cities_csv_path = os.getenv("CITIES_CSV_S3_PATH")

        states_wkt = self.glueContext.read.option("delimiter", "\t").option("header", "false").csv(states_wkt_path).toDF("s_name", "s_bound")
        states = states_wkt.selectExpr("s_name", "ST_GeomFromWKT(s_bound) as s_bound")
        states.createOrReplaceTempView("states")

        cities_csv = self.glueContext.read.option("delimiter", ",").option("header", "false").csv(cities_csv_path).toDF("c_name", "c_loc")
        cities = cities_csv.selectExpr("c_name", "ST_PointFromText(c_loc, \'_\') as c_loc")
        cities.createOrReplaceTempView("cities")

        # Perform spatial queries
        city_per_state = self.glueContext.sql("select * from states s, cities c where ST_Contains(s.s_bound, c.c_loc)")
        dist_to_seattle = self.glueContext.sql(
            "select c_name, ST_Distance(c_loc, ST_Point(-122.313323, 47.622715)) as dist from cities")

        # Show results
        city_per_state.show()
        dist_to_seattle.show()


class SedonaLogicJob(BaseJob):
    def __init__(self, glueContext):
        super().__init__(glueContext)

    def body(self):
        # Load spatial data
        states_wkt_path = os.getenv("STATES_WKT_S3_PATH")
        cities_csv_path = os.getenv("CITIES_CSV_S3_PATH")

        states_wkt = self.glueContext.read.option("delimiter", "\t").option("header", "false").csv(states_wkt_path).toDF("s_name", "s_bound")
        states = states_wkt.selectExpr("s_name", "ST_GeomFromWKT(s_bound) as s_bound")
        states.createOrReplaceTempView("states")

        cities_csv = self.glueContext.read.option("delimiter", ",").option("header", "false").csv(cities_csv_path).toDF("c_name", "c_loc")
        cities = cities_csv.selectExpr("c_name", "ST_PointFromText(c_loc, \'_\') as c_loc")
        cities.createOrReplaceTempView("cities")

        # Perform spatial queries
        city_per_state = self.glueContext.sql("select * from states s, cities c where ST_Contains(s.s_bound, c.c_loc)")
        dist_to_seattle = self.glueContext.sql(
            "select c_name, ST_Distance(c_loc, ST_Point(-122.313323, 47.622715)) as dist from cities")

        # Show results
        city_per_state.show()
        dist_to_seattle.show()
