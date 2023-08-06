# Sabia Utils

This is a collection of utilities for Sabia.

## Concat Module

This module is used to concatenate files.


### Concatenate all files from a path

* Returns a concatenated dataframe from all files in a path.
* Can save the concatenated dataframe to a file.

```python
from sabia_utils import concat

concat.concatenate_all_from_path(
    path='path\\to\\files',
    output_file='output\\file\\path', # optional
    fine_name='file_name'           # optional 
)
```

### Concatenate some files from a path

* Returns a concatenated dataframe from some files in a path.
* Can save the concatenated dataframe to a file.

```python
from sabia_utils import concat

concat.concatenate_files(
    path='path\\to\\files',
    files=['file1', 'file2'],
    output_file='output\\file\\path', # optional
    fine_name='file_name'           # optional 
)
```


### Copy files from a path to another

* Verify if the files exist in the path before copy.

```python
from sabia_utils import group

group.copy_new_files(
    PATH_IN='path\\to\\files1',
    PATH_OUT='path\\to\\files2'
)
```

## Group Module

This module is used to group files.

### Process files in both paths

* Verify if the files exist in the path before process.

```python
from sabia_utils import group

group.process_existent_files(
    PATH_IN='path\\to\\files1',
    PATH_OUT='path\\to\\files2'
)
```

### Process all files

* apply the function of copy and process files between the paths.

```python

from sabia_utils import group

group.process_all_files(
    PATH_IN='path\\to\\files1',
    PATH_OUT='path\\to\\files2'
)
```

## Pre_process Module

This module is used to pre_process parquet files.

### Process all parquet files

* Define a class that inherit sabia_utils.pre_process.Processing
* Override method apply_to_df(self, df, column), defining the pre-processing to be applied

* Apply this function on a folder containing parquet files to process them.

```python
from sabia_utils.pre_process import Processing
from sabia_utils import pre_process

class MyProcessor(Processing):
    def apply_to_df(self, df, column): 
        # Your pre-processing steps

pre_process.pre_process_parquets(
    folder_path='path\\to\\folder',
    colomun_to_pre_process='column_name_to_be_processed',
    pre_processed_column='processed_column_name',
    processor=MyProcessor()
)
```
