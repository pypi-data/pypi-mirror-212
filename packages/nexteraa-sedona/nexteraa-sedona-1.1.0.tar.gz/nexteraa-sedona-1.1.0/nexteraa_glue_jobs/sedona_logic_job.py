import functools
from enum import Enum

from allied_glue_common.utilities import get_date_iso_8601, null_safe_map, \
    resolve_datatype_choices, fill_null_strings, get_json, get_timestamp_iso_8601, add_columns
from allied_glue_jobs.base_job import BaseJob


class RequiredParameters(Enum):
    DATE_COLUMN_NAME = "date_column_name"
    DESTINATION_PATH = "destination_path"
    OUTPUT_FORMAT = "output_format"
    RUN_DATE_ISO_8601 = "run_date_iso_8601"
    SOURCE_DATABASE = "source_database"
    SOURCE_TABLE = "source_table"


class OptionalParameters(Enum):
    BOOKMARK_KEYS = "bookmark_keys"
    BOOKMARK_KEYS_SORT_ORDER = "bookmark_keys_sort_order"
    INPUT_DATATYPES = "input_datatypes"
    METADATA_COLUMNS = "metadata_columns"


class SedonaLogicJob(BaseJob):
    def __init__(self, glueContext):
        super().__init__(glueContext)

    def body(self):
        # Load spatial data
        states_wkt = self.glueContext.read.option("delimiter", "\t").option("header", "false").csv(
            "s3://glue-sedona/data/customers_database/country_csv/boundary-each-state.tsv").toDF("s_name", "s_bound")
        states = states_wkt.selectExpr("s_name", "ST_GeomFromWKT(s_bound) as s_bound")
        states.createOrReplaceTempView("states")

        cities_csv = self.glueContext.read.option("delimiter", ",").option("header", "false").csv(
            "s3://glue-sedona/data/customers_database/country_csv/cities.csv").toDF("c_name", "c_loc")
        cities = cities_csv.selectExpr("c_name", "ST_PointFromText(c_loc, \'_\') as c_loc")
        cities.createOrReplaceTempView("cities")

        # Perform spatial queries
        city_per_state = self.glueContext.sql("select * from states s, cities c where ST_Contains(s.s_bound, c.c_loc)")
        dist_to_seattle = self.glueContext.sql(
            "select c_name, ST_Distance(c_loc, ST_Point(-122.313323, 47.622715)) as dist from cities")

        # Show results
        city_per_state.show()
        dist_to_seattle.show()

