#!/usr/bin/env python

# Script to parse mixed milliseconds and microsecond data from NVIDIA NSight Profiling tools;
# e.g., "40.116 ms" will be converted to  40116 (microseconds) for a common basis of comparison 
# Script assumes all `us` units removed from CSV 


from datetime import datetime
import pandas as pd
import re


input_filename = "/Users/ajpowel/Desktop/mhm2_parsed.xlsx"

timestamp = datetime.today().strftime('%Y-%m-%d-%H-%m')
output_filename = "mhm2_prof_microsecs_" + timestamp + ".xlsx"


def spreadsheet_to_dataframe(input_filename):
    df = pd.read_excel(input_filename)
    return df


def convert_to_millisecs(value):
    # Check if the value contains "ms" and convert to milliseconds
    match = re.search(r'(\d+(.\d+)?)\s*ms', str(value))
    if match:
        milliseconds = match.group(1)
        milliseconds = float(milliseconds)*1000
        return milliseconds
    else:
        # If no value to convert to milliseconds found, return the original value
        return value


def process_input_spreadsheet(df, output_filename):
    df['Duration-microseconds'] = df['Duration'].apply(convert_to_millisecs)
    df.to_excel(output_filename, columns=["Name", "Duration-microseconds"], index=False)


if __name__ == "__main__":

    input_filename = "/Users/ajpowel/Desktop/mhm2_parsed.xlsx"
    timestamp = datetime.today().strftime('%Y-%m-%d-%H-%m')
    output_filename = "mhm2_prof_microsecs_" + timestamp + ".xlsx"
    df = spreadsheet_to_dataframe(input_filename)
    process_input_spreadsheet(df, output_filename)
    print(f"Parsing milliseconds to microseconds completed.  Results saved to {output_filename}.")
