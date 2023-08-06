"""Utility functions for Jautomate"""

import csv
import os
from typing import Dict, List, Union

from jautomate.assets import Asset


def get_assets_from_csv(file_path: Union[str, os.PathLike]) -> List[Asset]:
    """
    Imports assets from csv file and stores as Asset Objects.

    Will import from a CSV file of assets using specific keys for the information.
    The keys are as follows

    CCPS Tag#
    Serial Number
    School Calc
    Homeroom
    First
    Last
    Grade

    Args:
        file_path (Union[str, os.PathLike]): Path to csv file to import.

    Returns:
        List: List of Asset objects
    """
    assets = []
    with open(file_path, newline='', encoding='utf8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Hardware Type'] == 'Handheld Device':
                device_type = 'mobile'
            elif row['Hardware Type'] == 'Laptop':
                device_type = 'computer'

            asset = Asset(
                device_type=device_type,
                asset_tag=row['CCPS Tag#'],
                serial_number=row['Serial Number'],
                building=row['School Calc'],
                homeroom=row['Homeroom'],
                student_name=f"{row['First']} {row['Last']}",
                student_grade=row['Grade']
            )
            assets.append(asset)
    return assets


def determine_serial_number_key_format(remote_asset: Dict) -> str:
    """
    Determines the format of the serial number key being used by 
    Jamf (Classic or Pro) and returns that as a string.

    Args:
        remote_asset (Dict): A Dict obj of a remote asset that was returned 
        by Jamf API

    Raises:
        KeyError: Raises a KeyError if neither of the key options was found

    Returns:
        str: String value for the serial number key.
    """
    if remote_asset.get('serialNumber'):
        return 'serialNumber'
    if remote_asset.get('Serial_Number'):
        return 'Serial_Number'
    raise KeyError('No valid key found for Serial Number')
