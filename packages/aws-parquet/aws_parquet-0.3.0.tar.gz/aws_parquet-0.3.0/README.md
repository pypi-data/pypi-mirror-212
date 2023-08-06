# Brief

`aws-parquet` is a toolkit than enables working with parquet datasets on AWS. It handles AWS S3 reads/writes, AWS Glue catalog updates and AWS Athena queries by providing a simple and intuitive interface.

## Motivation

The goal is to provide a simple and intuitive interface to create and manage parquet datasets on AWS.

`aws-parquet` makes use of the following tools: 
- [awswrangler](https://aws-sdk-pandas.readthedocs.io/en/stable/) as an AWS SDK for pandas
- [pandera](https://pandera.readthedocs.io/en/stable/) for pandas-based data validation
- [typeguard](https://typeguard.readthedocs.io/en/stable/userguide.html) and [pydantic](https://docs.pydantic.dev/latest/) for runtime type checking

## Features
`aws-parquet` provides a `ParquetDataset` class that enables the following operations:

- create a parquet dataset that will get registered in AWS Glue
- append new data to the dataset and update the AWS Glue catalog
- read a partition of the dataset and perform proper schema validation and type casting
- overwrite data in the dataset after performing proper schema validation and type casting
- delete a partition of the dataset and update the AWS Glue catalog
- query the dataset using AWS Athena


## How to setup

Using pip:

```bash
pip install aws_parquet
```

## How to use

Create a parquet dataset that will get registered in AWS Glue

```python
import os

from aws_parquet import ParquetDataset
import pandas as pd
import pandera as pa
from pandera.typing import Series

# define your pandera schema model
class MyDatasetSchemaModel(pa.SchemaModel):
    col1: Series[int] = pa.Field(nullable=False, ge=0, lt=10)
    col2: Series[pa.DateTime]
    col3: Series[float]

# configuration
database = "default"
bucket_name = os.environ["AWS_S3_BUCKET"]
table_name = "foo_bar"
path = f"s3://{bucket_name}/{table_name}/"
partition_cols = ["col1", "col2"]
schema = MyDatasetSchemaModel.to_schema()

# create the dataset
dataset = ParquetDataset(
    database=database,
    table=table_name,
    partition_cols=partition_cols,
    path=path,
    pandera_schema=schema,
)

dataset.create()
```

instead with awswrangler one would have to do the following:

```python
import awswrangler as wr

wr.catalog.create_parquet_table(
    database=database,
    path=path,
    table=table,
    # figure out the equivalent glue/athena types to use
    partitions_types={"col1": "bigint", "col2": "timestamp"},
    columns_types={"col3": "double"},
)
```

Append new data to the dataset

```python
df = pd.DataFrame({
    "col1": [1, 2, 3],
    "col2": ["2021-01-01", "2021-01-02", "2021-01-03"],
    "col3": [1.0, 2.0, 3.0]
})

dataset.update(df)
```

instead with awswrangler one would have to do the following:

```python
df = pd.DataFrame({
    "col1": [1, 2, 3],
    "col2": ["2021-01-01", "2021-01-02", "2021-01-03"],
    "col3": [1.0, 2.0, 3.0]
})

# perform schema validation and type casting 
df_validated = validate_schema(df)

wr.s3.to_parquet(
    df=df,
    path="s3://my-bucket/my-dataset",
    dataset=True,
    database="my_database",
    table="my_table",
    partition_cols=["col1", "col2"],
    mode="append"
)
```

Read a partition of the dataset

```python
df = dataset.read({"col2": "2021-01-01"})
```

instead with awswrangler one would have to do the following:

```python
df = wr.s3.read_parquet(
    path="s3://my-bucket/my-dataset",
    dataset=True,
    database="my_database",
    table="my_table",
    # make sure to cast the partition values to the right dtype
    partition_filter=lambda x: pd.Timestamp(x["col2"]) == pd.Timestamp("2021-01-01")
)

# perform schema validation and type casting 
df_validated = validate_schema(df)
```

Overwrite data in the dataset

```python
df_overwrite = pd.DataFrame({
    "col1": [1, 2, 3],
    "col2": ["2021-01-01", "2021-01-02", "2021-01-03"],
    "col3": [4.0, 5.0, 6.0]
})
dataset.update(df_overwrite, overwrite=True)
```

instead with awswrangler one would have to do the following:

```python
df_overwrite_validated = validate_schema(df_overwrite)

wr.s3.to_parquet(
    df=df_overwrite_validated,
    path="s3://my-bucket/my-dataset",
    dataset=True,
    database="my_database",
    table="my_table",
    partition_cols=["col1", "col2"],
    mode="overwrite_partitions"
)
```

Delete a partition of the dataset

```python
dataset.delete({"col1": 1, "col2": "2021-01-01"})
```

instead with awswrangler one would have to do the following:

```python
# remove the partitions from s3
wr.s3.delete_objects(path="s3://infima-package-testing/foo/bar/col1=1/col2=2021-01-01")

# remove the partitions from glue
wr.catalog.delete_partitions(
    database="default",
    table="foo_bar",
    partitions_values=[["1", "2021-01-01 00:00:00"]],
)
```


Query the dataset using AWS Athena

```python
df = dataset.query("SELECT col1 FROM foo_bar")
```

instead with awswrangler one would have to do the following:

```python
out = wr.athena.read_sql_query("SELECT col1 FROM foo_bar", database=database)
```

