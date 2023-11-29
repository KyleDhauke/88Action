"""
The main control centre connecting all the sub modules together.
Automates validating a batch of cases in CSV format. Accepted cases
produce successful reports and are logged into the system for future
validation. 
Rejected cases output the reasons why they failed. They are not logged.

Classes:
    _validation: Validates the CSV against an establihed criteria.
    click: Command-line interface used during development. [TEMPORARY]
    pandas: Open-source data analysis library to interact with the CSV's.
    _config: Manages the configuration file containing the settings for
        this application.
    
Functions:

    main(): TBA
    
    
Returns:
"""

import click
import pandas as pd
import _validation
import _config
import _backlog
import _set_up
import numpy as np


# @click.command()
# @click.option('--csv', required = True, type = str, prompt="Path to CSV", help = "Path to the CCL CSV Import File" )
# @click.option('--log', type = str, help = "Path to 88Legal's uploaded cases")
def main():
    """
    TODO: Add method documentation once complete.
    Args:
    Returns:
    """
    config = _config.Config()
    
    csv = "C:/Users/kyle4/repos/Project 88Action/util/docs/CCL Import sheet (Cases to be funded).csv"   
    import_settings = config.data['configuration']['importCSV']

    ccl = _set_up.pandas_import(csv, import_settings)
    print(_validation.validate_batch(ccl, config))
    return


if __name__ == '__main__':
    main()
    

