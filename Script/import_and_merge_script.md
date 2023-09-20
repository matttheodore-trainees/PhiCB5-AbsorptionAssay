# Import and Merge Script

This script demonstrates how to import the `data_master` and `trial_data` datasets and then merge them into a single dataframe.

## Import Libraries

First, we import the required libraries.

```python
import pandas as pd
```

## Read Data Master

Here we read in the `data_master` dataset from an Excel file.

```python
data_master = pd.read_excel('/path/to/data_master.xlsx')
```

## Read Trial Data

To read the `trial_data`, we follow a chunking approach. We loop through sets of 3 columns at a time to read in the data and then concatenate these chunks. We also add a 'rep' column to denote the replicate number (1, 2, or 3).

```python
# Reading the data in chunks of 3 columns and adding 'rep' column to each chunk
dfs = []
for i in range(1, 4):  # Looping through each set of 3 columns
    cols_to_read = [0, 1, i + 1]  # The columns to read in
    df_chunk = pd.read_csv('/path/to/trial_data_easier.csv', usecols=cols_to_read, header=None)
    df_chunk.columns = ['unique_id', 'strain', 'titer']
    df_chunk['rep'] = i  # Adding 'rep' column
    dfs.append(df_chunk)

# Concatenating all the chunks into one DataFrame
trial_data_long_corrected = pd.concat(dfs, ignore_index=True)
```

## Merge the Datasets

Finally, we merge the two datasets into one combined dataframe.

```python
# Merging the dataframes
combined_data = pd.concat([data_master, trial_data_long_corrected], ignore_index=True)
```

And that's it! Now, `combined_data` contains the merged datasets.
