#!/usr/bin/env python

# Script to parse mixed milliseconds and microsecond data from NVIDIA NSight Profiling tools;
# e.g., "40.116 ms" will be converted to  40116 (microseconds) for a common basis of comparison 
# STEP 1:
# Script assumes all `us` units removed from CSV with "find / replace" 


from datetime import datetime
import pandas as pd
import re


timestamp = datetime.today().strftime('%Y-%m-%d-%H-%m')

#input_filename = "/Users/ajpowel/Desktop/mhm2_profiling/mhm2_parsed.xlsx"
input_filename = "/Users/ajpowel/LEAP_profiling/FAPI_unit_test_profile_April_19.xlsx"

output_filename = "test_parser" + "_" + timestamp + "_" + ".xlsx"

#output_filename = "mhm2_prof_microsecs_" + timestamp + ".xlsx"
#output_filename = "FAPI_prof_usecs_" + timestamp + ".xlsx"


def spreadsheet_to_dataframe(input_filename):
    df = pd.read_excel(input_filename)
    return df


def convert_to_microseconds(value):
    # Check if the value contains (milliseconds) "ms" or (nanoseconds) "ns", and if match, convert to microseconds
    # 1 millisecond : 1000 microseconds
    # 1 microsecond : 1000 nanoseconds

    milli_match = re.search(r'(\d+(.\d+)?)\s*ms', str(value))
    nano_match = re.search(r'(\d+(.\d+)?)\s*ns', str(value))
    if milli_match:
        milliseconds = milli_match.group(1)
        microseconds = float(milliseconds)*1000
        return microseconds
    elif nano_match:
        nanoseconds = nano_match.group(1)
        microseconds = float(nanoseconds)/1000
        return microseconds
    else:
        # If no value to convert to microseconds found, return the original value
        return value


def process_input_spreadsheet(df, output_filename):
    df['Duration-microseconds'] = df['Duration'].apply(convert_to_microseconds)
    df.to_excel(output_filename, columns=["Name", "Duration-microseconds"], index=False)


if __name__ == "__main__":
    timestamp = datetime.today().strftime('%Y-%m-%d-%H-%m')
    input_filename = "/Users/ajpowel/LEAP_profiling/FAPI_unit_test_profile_April_19.xlsx"
    output_filename = "test_parser" + "_" + timestamp + "_" + ".xlsx"
    df = spreadsheet_to_dataframe(input_filename)
    process_input_spreadsheet(df, output_filename)
    print(f"Parsing milliseconds, nanoseconds, etc. to microseconds completed.  Results saved to {output_filename}.")
