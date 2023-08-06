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


# Define the SedonaAggLogicJob class
class SedonaAggLogicJob(BaseJob):
    # Define the job options, required parameters, and optional parameters specific to this job
    @property
    def job_options(self):
        return []

    @property
    def required_parameters(self):
        return ["INPUT_DATA_PATH"]  # Add any other required parameters

    @property
    def optional_parameters(self):
        return ["OUTPUT_DATA_PATH"]  # Add any other optional parameters

    def body(self):
        # Retrieve the input and output data paths from the job parameters
        # Retrieve the input and output data paths from the job parameters
        input_data_path = self.get_option(JobOptions.INPUT_DATA_PATH)
        output_data_path = self.get_option(JobOptions.OUTPUT_DATA_PATH)

        # Perform your custom logic using Sedona here
        SedonaRegistrator.registerAll(self.spark_context)

        # Load spatial data
        states_wkt = self.spark_session.read.option("delimiter", "\t").option("header", "false").csv(input_data_path)

        states_wkt = states_wkt.toDF("s_name", "s_bound")
        states_wkt.show()
        states_wkt.printSchema()

        states = states_wkt.selectExpr("s_name", "ST_GeomFromWKT(s_bound) as s_bound")
        states.printSchema()
        states.createOrReplaceTempView("states")

        # Perform the desired aggregation logic using Sedona
        aggregated_data = self.spark_session.sql("SELECT s_name, ST_UnionAgg(s_bound) as agg_geometry FROM states GROUP BY s_name")

        # Write the aggregated data to the output path
        aggregated_data.write.mode("overwrite").parquet(output_data_path)

# Define any job-specific options as an Enum
class JobOptions(Enum):
    INPUT_DATA_PATH = "input_data_path"
    OUTPUT_DATA_PATH = "output_data_path"