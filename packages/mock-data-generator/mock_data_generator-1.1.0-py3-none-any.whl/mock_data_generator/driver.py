import argparse
import os
from generator.generate import runner
from utils.constants import FILE_FORMATS
from utils.fileutils import process


def validate_file_format(value):
    if value.upper() not in FILE_FORMATS:
        raise argparse.ArgumentTypeError(
            f"Unsupported output file format {value} detected. Supported file formats are {FILE_FORMATS}"
        )
    return value


def validate_num_rows(value):
    num_rows = int(value)
    if num_rows <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid number of rows. The value for number of rows should be positive integer"
            % value
        )
    return num_rows


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_json_schema_path",
        help="Input absolute path of the schema json, schema file or schema folder",
        required=True,
    )
    parser.add_argument(
        "--output_file_format",
        type=validate_file_format,
        help="Expected output file format(csv,json,xml,excel,parquet)",
        required=True,
    )
    parser.add_argument(
        "--output_path", help="Output path for mock dataset.", required=True
    )
    parser.add_argument(
        "--number_of_rows",
        type=validate_num_rows,
        help="Number of mock records to be generated.",
        required=True,
    )
    args = parser.parse_args()
    process(args=args)


if __name__ == "__main__":
    run()
