import pandas as pd
from faker import Faker
from pandas import DataFrame
from tqdm import tqdm


def generate_string_data(fkr: Faker):
    return fkr.pystr()


def generate_integer_data(fkr: Faker):
    return fkr.random_int()


def generate_float_data(fkr: Faker):
    return fkr.pyfloat()


def generate_date_data(fkr: Faker):
    return fkr.date()


def generate_boolean_data(fkr: Faker):
    return fkr.pybool()


def generate_timestamp_data(fkr: Faker):
    return fkr.date_time()


def save_output_as_csv(pd: DataFrame, output_path: str):
    pd.to_csv(f"{output_path}/data.csv")


def save_output_as_json(pd: DataFrame, output_path: str):
    pd.to_json(
        f"{output_path}/data.json", orient="records", date_format="iso", lines=True
    )


def save_output_as_xml(pd: DataFrame, output_path: str):
    pd.to_xml(f"{output_path}/data.xml")


def save_output_as_excel(pd: DataFrame, output_path: str):
    pd.to_excel(f"{output_path}/data.xlsx", header=True)


def save_output_as_parquet(pd: DataFrame, output_path: str):
    pd.to_parquet(f"{output_path}/data.parquet", compression="snappy")


def save_output_as_orc(pd: DataFrame, output_path: str):
    pd.to_orc(f"{output_path}/data.orc")


data_type_to_func_map = {
    "STRING": "generate_string_data",
    "INT": "generate_integer_data",
    "INTEGER": "generate_integer_data",
    "NUMBER": "generate_integer_data",
    "FLOAT": "generate_float_data",
    "DATE": "generate_date_data",
    "BOOLEAN": "generate_boolean_data",
    "BOOL": "generate_boolean_data",
    "TIMESTAMP": "generate_timestamp_data",
}

file_format_to_func_map = {
    "CSV": "save_output_as_csv",
    "JSON": "save_output_as_json",
    "XML": "save_output_as_xml",
    "EXCEL": "save_output_as_excel",
    "PARQUET": "save_output_as_parquet",
    "ORC": "save_output_as_orc",
}


def runner(json_schema: any, num_of_rows: int, output_path: str, file_format: str):
    schema_dict = json_schema["properties"]
    fkr = Faker()
    pd_df = pd.DataFrame()
    for column_name in schema_dict:
        type_dict = schema_dict[column_name]
        column_type = type_dict["type"]
        for cnt in tqdm(
            range(num_of_rows), desc=f"Generating mock data for: {column_name}"
        ):
            function_name = data_type_to_func_map[column_type.upper()]
            pd_df.loc[cnt, column_name] = globals()[function_name](fkr=fkr)

    file_format_function_name = file_format_to_func_map[file_format.upper()]
    globals()[file_format_function_name](pd_df, output_path)
