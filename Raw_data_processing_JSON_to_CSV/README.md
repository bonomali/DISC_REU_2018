# Project Title

To get anything meaningful out of our data, we must first process the raw JSON files we've received to create CSV files that have only useful information in them.

### Prerequisites

This code makes use of python3.5, though should be backcompatible with python2.7. The modules required are csv, json, datetime.

### How to Use

Open up json_conversion_to_csv.py into a text editor.

Change the variable "json_filepath" to the raw JSON file you would like to convert

```
json_filepath = "SP18RawActivityData/SP18_FYS_10101_activity_03_23.json"
```

Change the variable "csv_filepath" to whatever you would like the output file saved as. Make sure it is unique to each json filepath.

```
csv_filepath = "SP18_03_23.csv"
```

Repeat for every json file, being sure to change both the json and csv filepaths each time (i.e. don't overwrite the previous csv filepath).

After creating all the csv files you are interested in, run csv_joiner.py in the bash terminal. The system arguments are: csv_filepath1, csv_filepath2, ... csv_filepathN, output_filepath.

```
$python3 csv_joiner.py SP18_03_16.csv SP18_03_23.csv SP18_04_2.csv SP18_04_9.csv SP18_04_17.csv SP18_05_1.csv SP18_05_7.csv SP18_05_14.csv SP18_all_data.csv
```

Next, open up data_filtering.py in a text editor.

Note that whatever you saved as the output file in csv_joiner.py (in this case, SP18_all_data.csv) should be the csv_filepath variable in data_filtering.py as well.


