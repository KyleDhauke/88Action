# TODO: Add documentation once complete.

import pandas as pd
import _backlog
from enum import Enum
from _config import AutoHeaders
from _set_up import PandaTypes
import numpy as np
import math
from datetime import datetime



def validate_batch(ccl, config):
    isValid = True       
    # Iterate through every case (row)
        # Check 88 backlog via backlog.check(row) <-- leave till later
            # If it fails, add to failed df. <-- build up
    
    valid_settings = config.data['configuration']['validation_settings']
    headers = config.data['configuration']['importCSV']['headers'] 
    if AutoHeaders(config.data['configuration']['importCSV']['AutoHeaders']) != (AutoHeaders.CLEAN or AutoHeaders.AUTO):
        headers = None
    checked_cases = ccl.apply(_check_dataframe, args = [valid_settings, headers], axis = 1, result_type = 'expand')
    print(checked_cases)
    bool_cols = checked_cases.map(_filter_fn).any(bool_only= bool, axis = 1)
    print(bool_cols)
    
    pass


def _filter_fn(series):
    if isinstance(series, list):
        return True
    return False

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
        p_type = PandaTypes(headers[name]['type'])
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


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class Rejection(ExtendedEnum):
    MISSING = 'Missing'
    INVALID_ORDER = 'Invalid Order'
    INVALID_VALUE = 'Invalid Value'
    
    

