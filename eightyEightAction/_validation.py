# TODO: Add documentation once complete.

import pandas as pd
from _config import Config
import _backlog
from enum import Enum
from _config import AutoHeaders
from _set_up import PandaTypes
import _set_up
import numpy as np
from datetime import datetime


def validate_batch(ccl:pd.DataFrame, config:Config) -> tuple[pd.DataFrame]:    
    valid_settings = config.data['configuration']['validation_settings']
    headers = config.data['configuration']['importCSV']['headers'] 
    if AutoHeaders(config.data['configuration']['importCSV']['autoHeaders']) != (AutoHeaders.CLEAN or AutoHeaders.AUTO):
        headers = None
    checked_cases = ccl.apply(_check_dataframe, args = [valid_settings, headers], axis = 1, result_type = 'expand')
    bool_cols = checked_cases.map(_filter_fn).any(bool_only= bool, axis = 1)
    rejected_blueprint = checked_cases.loc[bool_cols.values.tolist(), :]
    rejected_cases = ccl.loc[bool_cols.values.tolist(), :]
    # Create a fail blueprint of the whole dataframe.
    # fail_blueprint_full = _combine_dataframes(ccl, rejected_blueprint)
    

    return rejected_cases, rejected_blueprint


def _filter_fn(elem):
    return len(set(listify(elem)).intersection(list(Rejection))) > 0


def _combine_dataframes(df1, df2):
    df_concat = pd.concat([df1, df2])
    df_merge = df_concat.loc[~df_concat.index.duplicated(keep='last')]
    df_merge.index = df_merge.index.astype(int)
    df_merge = df_merge.sort_index( ascending= False)
    return df_merge


def _check_dataframe(series, valid_settings, headers):
    rejection_reasons = {}
    required_cols = valid_settings['required']
    opt_cols = valid_settings['opt_required']
    combined_cols = _flatten_list(required_cols + opt_cols)
    
    for i in required_cols:
        if isinstance(i, list):
            # rejection_reasons = _check_list(i)
            # rejection_reasons[i] = "test"
            pass
            
        else:
            rejection_reasons[i] = _check_element(i, series.get(i), headers, series.name)
    
    return rejection_reasons



def _check_element(name, elem, headers, g):
    rejectionReason = []
    if __isNaN(elem):
        rejectionReason.append(Rejection.MISSING)
        return rejectionReason
    elif isinstance(elem, str) and elem == "None":
        rejectionReason.append(Rejection.MISSING)
        return rejectionReason
    if headers:
        p_type = _set_up._panda_mapping(headers[name]['type'])
        reasons = _eval_element(p_type, elem)
        if isinstance(reasons, list):
            rejectionReason + reasons
              
    return elem if not(rejectionReason) else rejectionReason
    
    

def _check_list(elem, headers):
    pass


def _eval_element(p_type, elem):
    rejectionReason = []
    if p_type == PandaTypes.STRING64 and (not(isinstance(elem, str))):
        return rejectionReason.append(Rejection.INVALID_VALUE)
    elif p_type == PandaTypes.FLOAT64 and not(isinstance(elem, float)):
        return rejectionReason.append(Rejection.INVALID_VALUE)
    elif p_type == PandaTypes.INT64 and not(isinstance(elem, int)):
        return rejectionReason.append(Rejection.INVALID_VALUE)
    elif p_type == PandaTypes.DATETIME64 and not(isinstance(elem, datetime)):
        return rejectionReason.append(Rejection.INVALID_VALUE)
    else:
        return elem if not(rejectionReason) else rejectionReason


def _flatten_list(packed_list):
    unpacked_list = []
    for i in packed_list:
        if isinstance(i, list):
            unpacked_list += _flatten_list(i)
        else:
            unpacked_list.append(i)
    return unpacked_list


def __isNaN(x):
    if isinstance(x, str):
        return x == "nan" and not(x and not x.isspace())
    # Courtesy of C.K. Young
    # https://stackoverflow.com/a/944712/22358902
    return x != x

def listify(x):
    return x if isinstance(x, list) else [x]


class Rejection(Enum):
    MISSING = 'Missing'
    INVALID_ORDER = 'Invalid Order'
    INVALID_VALUE = 'Invalid Value'
    
    

