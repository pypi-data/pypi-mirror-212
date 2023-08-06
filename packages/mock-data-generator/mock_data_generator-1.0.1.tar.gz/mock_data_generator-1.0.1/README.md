# Data Generator - WIP

## Overview
During every data project I came across a very basic problem where we have to wait for the test data. For fewer columns it's quite easy to generate the data using online utilities but those has certain limitations on number of columns and rows. 
Solve this, I invested some time to build a utility to generate the mock data based on the supplied json schema. 
This utility is using Python Faker module to randomly generate the test data. 

## How to use
Follow below step to run the utility. I am open to the suggestions, please add comment or mail me your suggestions.
### Inputs
- input_json_schema_path: Provide absolute path of the json schema file. The sample json schema file should be 
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

- output_file_format: The output file format should be one of the `"CSV","JSON","XML","EXCEL","PARQUET","ORC"`

- output_path: Absolute path where the generated output should be stored

- number_of_rows: Number of output rows to be generated

- Supported data types are: `"STRING","INT","INTEGER","NUMBER","FLOAT","DATE","BOOLEAN","BOOL","TIMESTAMP"`


### Pre-requisites 
1. Python 3.11.3
2. Poetry 1.3.2

### Steps to execute the utility
1. `clone the repo`
2. `cd mock_data_generator`
3. `poetry install`
4. Sample command: `poetry run generate --input_json_schema_path=resources/schema.json --output_file_format=csv --output_path=output_data --number_of_rows=10 ` : If output path does not exists, it will create it and store the data inside the directory into data.csv file

### Licensing
Distributed under the MIT license. See ``LICENSE`` for more information.