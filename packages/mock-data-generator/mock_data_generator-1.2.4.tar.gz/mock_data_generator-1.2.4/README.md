# Data Generator - WIP

## Overview
During every data project I came across a very basic common problem where we have to wait for the test data. For fewer columns it's quite easy to generate the data using online utilities but those have certain limitations on the number of columns and rows.
To solve this, I’ve built a utility to generate the mock data based on the supplied json schema.
This utility is using Python Faker module to randomly generate the test data.

## How to use
Follow below steps to run the utility. I am open to your suggestions, please add comments or mail me your suggestions.

### Inputs
It accept valid json schema files only with supported data types: `"STRING","INT","INTEGER","NUMBER","FLOAT","DATE","BOOLEAN","BOOL","TIMESTAMP"`
#### Supported Input Parameters

- --input_json_schema_path: Provide absolute path of the json schema file/folder. It accepts folders(that contains valid json schema files) or absolute path of a json schema file.

> Json schema file format.
```json
{
  "type": "<object/record,etc>",
  "properties": {
    "<column_name>": { "type": "<data_type>" },
    "<column_name>": { "type": "<data_type>" }
  }
}

```
> The sample json schema file would look like below.
```json
{
  "type": "object",
  "properties": {
    "price": { "type": "number" },
    "name": { "type": "string" },
    "a": { "type": "integer" },
    "b": { "type": "float" },
    "c": { "type": "boolean" },
    "dt": { "type": "date" },
    "ts": { "type": "timestamp" },
    "e": { "type": "boolean" }
  }
}
```
The generator will skip the current json schema file if an error occurred. Mock data would get generated for rest of the valid schema files.

- --output_file_format: The output file format should be one of the `"CSV","JSON","XML","EXCEL","PARQUET","ORC"`

- --output_path: Absolute path to store the generated mock dataset. If an output path does not exists, it will create it and store the data inside the directory into data.<output file format> file.

- --number_of_rows: Number of output rows to be generated

### Pre-requisites
1. Python ^3.10


### Steps to execute the utility
1. pip install mock-data-generator
2. specify the parameters mentioned above
4. Sample command: `generate --input_json_schema_path=resources/schema.json --output_file_format=csv --output_path=output_data --number_of_rows=10 ` :

### Licensing
Distributed under the MIT license. See ``LICENSE`` for more information.
