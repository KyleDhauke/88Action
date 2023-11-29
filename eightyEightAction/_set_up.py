"""
_set_up.py handles importing csv files and converting them into clean pandas
dataframes according to the configuration settings.

Classes:
    pandas: Open-source data analysis library to interact with the CSV's.
    _io: Python's interface for stream-handling
    re: Python's library for regular expressions
    datetime: Python DateTime objects
    Enum: Allows creation of constant key and value pairs.

Functions:
    pandas_import: Converts import CSV sheet into pandas dataframe
        alongside addition functionality.
"""


import pandas as pd
from io import StringIO
from enum import Enum
import re
import numpy as np
from datetime import datetime
import _config
from _config import AutoHeaders

def pandas_import(csv_file, import_settings):
    """
    Reads the CSV path and returns a pandas dataframe.
    Additional functionality includes handling 'sep = ,' at the start of the
    csv and cleaning column datatypes according to the import settings.
    
    Args:
        csv_file (_type_): String or path-like object directing to the CSV
        import_settings: Dict object retrieved from the JSON config.

    Returns:
        pandas.DataFrame: The dataframe object corresponding to the CSV.
    """
    encoding = "utf-8"
    new_sep = ","
    with open(csv_file, encoding=encoding) as f:
        lines = [l.replace("\uFFFD", "") for l in f.readlines()]
        firstLine = lines[0].rstrip().lower()
        if ('sep=' in firstLine ):
            new_sep = firstLine.replace('sep=', '')
            lines.pop(0)
    ccl = pd.read_csv(StringIO("\n".join(lines)), dtype = object , sep=new_sep, encoding = encoding, skipinitialspace= True)
    ccl.set_index(keys= ["ID"], inplace= True, verify_integrity= False)
    auto_headers = AutoHeaders(import_settings['AutoHeaders'])
    #Enabling 'CLEAN' option in Import Settings means columns are organized
    # based on their user-defined import column settings.
    if auto_headers == AutoHeaders.CLEAN:
        headers = import_settings['headers']
        new_ccl = pd.DataFrame(ccl.apply(_clean_df, args=[headers]) )
        return new_ccl
    # AUTO setting custom parses each section before applying a datatype.
    elif auto_headers == AutoHeaders.AUTO:
        pass
    else:
    # Not recommended. All columns will likely be object datatypes.
        return ccl

import math

def _clean_df(curr_series: pd.Series, headers):
    """
    Cleans each column according to the desired type set by the headers
    dictionary in the import_settings.

    Args:
        curr_series (_type_): The series to be cleaned/assigned a type.
        headers (_type_): A dictionary containing the desired type.

    Returns:
        series: Returns a series with an attempt of classifying its type.
    """
    col_name = curr_series.name
    new_series = curr_series
    p_type = PandaTypes(headers[col_name]['type'])
    
    # Try-except statements to catch TypeError in case of 
    # unforseen circumstances.
    if p_type == PandaTypes.INT64:
        try:
            new_series = (pd.Series.apply(_clean_series_int)).astype(int)
        except TypeError:
            print("Failed to clean dataframe to INT64 single type")
        finally:
            return new_series
    elif p_type == PandaTypes.STRING64:
    
        try:
            new_series = curr_series.apply(lambda e: e if isinstance(e, str) else "None" ).astype(str)
        except TypeError:
            print("Failed to clean dataframe to single (STRING 64) type")
        finally:
            return new_series
        
    elif p_type == PandaTypes.FLOAT64:
        try:
            new_series = (curr_series.apply(_clean_series_float)).astype(float)
        except TypeError:
            print("Failed to clean dataframe to FLOAT64 single type")
        finally:
            return new_series 
    elif p_type == PandaTypes.DATETIME64:
        try:
            new_series = (curr_series.apply(_clean_series_date)).astype('datetime64[ns]')
        except TypeError as te:
            print("Failed to clean dataframe to DATETIME64 single type", te)
        except ValueError as ve:
            print("Time Data does not match DATETIME64 format", ve)
        finally:
            return new_series
    else:
        return curr_series
    

def _clean_series_float(obj):
    """ Removes non-numeric chars (except period) from obj and attempts to parse as float."""
    # Remove non-numeric characters (apart from period) courtesy of Miles
    # https://stackoverflow.com/a/947789/22358902
    if isinstance(obj, str):
        non_decimal = re.compile(r"[^\d.]+")
        s = non_decimal.sub('', obj)
        return float(s)
    else:
        return obj
    
def _clean_series_int(obj):
    """ Removes non-numeric chars from obj and attempts to parse as int."""
    # Removing non-numeric characters courtesy of Ned Batchedler
    # https://stackoverflow.com/a/1249424/22358902
    if isinstance(obj, str):
        s = re.sub(r"[^0-9]", "", obj)
        return int(s)
    else:
        return obj
    
    
def _clean_series_date(obj):
    """ Remove non-alphanumeric chars and attempts to parse str as a datetime object."""
    if isinstance(obj, str):
        non_alpha = re.compile(r"[^A-Za-z0-9 ]+")
        d = non_alpha.sub('', obj)
        # Current accepted date format: 01 Jun 2021
        date = datetime.strptime(d, "%d%b%y")
        return date
    else:
        return obj
    
    
class PandaTypes(Enum):
    INT64 = 'Int'
    STRING64 = 'String'
    FLOAT64 = 'Float'
    DATETIME64 = 'DateTime'
    BOOL = 'bool'