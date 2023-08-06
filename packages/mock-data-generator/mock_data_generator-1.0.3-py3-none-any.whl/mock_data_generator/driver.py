import argparse

from generator.generate import runner
from schema_handler.schema_validator import validate_and_read_json_as_object
from utils.constants import FILE_FORMATS
from utils.fileutils import make_path_if_not_exists, read_json_file_as_string


def validate_file_format(value):
    if value.upper() not in FILE_FORMATS:
        raise argparse.ArgumentTypeError(
            f"Unsupported output file format {value} detected. Supported file formats are {FILE_FORMATS}"
        )
    return value

def validate_num_rows(value):
    num_rows = int(value)
    if num_rows <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid number of rows. The value for number of rows should be positive integer" % value)
    return num_rows



def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_json_schema_path",
        help="Input absolute path of the schema json. e.g:/user/test/data/json_schema/schema.json",
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

    make_path_if_not_exists(args.output_path)
    json_schema_string = read_json_file_as_string(args.input_json_schema_path)
    json_schema = validate_and_read_json_as_object(json_schema=json_schema_string)

    runner(
        json_schema=json_schema,
        num_of_rows=int(args.number_of_rows),
        output_path=args.output_path,
        file_format=args.output_file_format,
    )


if __name__ == "__main__":
    run()
