"""Module to handle various actions performed with Jamf"""

from typing import Dict, List
from jautomate.api import jamf_p, jamf_c
from jautomate.assets import Asset, Assets
from jautomate.logger import j_logger
from jautomate import utils


class JautomateException(Exception):
    """
    Base Exception for Jautomate
    """


def get_all_mobile_devices_pro() -> List[Dict]:
    """
    Returns dict of all mobile devices from Jamf using Pro API

    Returns:
        List[Dict]: List of all mobile devices from Jamf Pro API
    """
    # Pro API max page size is 2000
    page_size = 2000
    page = 0
    # remaining_results needs to be higher than the total amount of devices
    remaining_results = 10000
    device_list = []
    while remaining_results > 0:
        response = jamf_p.get_mobile_devices(
            page=page, page_size=page_size)

        if remaining_results == 10000:
            remaining_results = int(response['totalCount']) - page_size
        else:
            remaining_results -= page_size

        device_list.extend(response['results'])
        page += 1
    return device_list


def get_all_mobile_devices() -> List[Dict]:
    """
    Returns all mobile devices from Jamf Classic API

    This function looks for a saved search on Jamf that is
    set up return only Jamf ID, Serial Number, and Asset Tag.
    The name used was 'All iPads by Asset Tag'.

    This is done because Jamf does not include asset tag in their
    default information that gets returned. A custom search number be
    saved first from the Jamf Pro GUI.

    Also, note the structure of the response that is returned as there
    is a lot of other unneeded info returned with the saved search.

    Returns:
        List[Dict]: List of Dicts for all mobile devices on Jamf.
    """
    response = jamf_c.get_advanced_mobile_device_search(
        name='All iPads by Asset Tag',
        data_type='json')
    return response['advanced_mobile_device_search']['mobile_devices']


def get_mobile_device_jamf_ids_by_serial_number(asset_list: Assets) -> Assets:
    """
    Gets the Jamf IDs of the local assets by checking the serial number against those in Jamf.

    Compares the serial numbers of local assets to those retrieved from Jamf servers
    and sets the jamf_id proptery of each asset object. This is done because most of the
    Jamf API endpoints work off of the id jamf gives each asset.

    This is used when assigning assets as the serial numbers are typically more
    accurate of a comparison when assigning

    Args:
        asset_list (Assets): Obj of assets being worked with. See Assets class for structure.

    Returns:
        Assets: Asset object with lists of both local and remote assets
    """
    serial_format = utils.determine_serial_number_key_format(
        asset_list.remote[0])

    for asset in asset_list.local:
        matching_device = next(
            (device for device in asset_list.remote
                if device[serial_format] == asset.serial_number), None)
        if matching_device:
            asset.jamf_id = matching_device['id']
    return asset_list


def get_mobile_device_jamf_ids_by_asset_tag(asset_list: Assets) -> Assets:
    """
    Gets the Jamf IDs of the local assets by checking the asset tag against those in Jamf.

    Compares the asset tags of local assets to those retrieved from Jamf servers
    and sets the jamf_id proptery of each asset object.

    This is used mostly for unassigning assets where it is more likely the
    asset tag has been set and is accurate.

    Args:
        asset_list (Assets): Obj of assets being worked with. See Assets class for structure.

    Returns:
        Assets: Asset object with lists of both local and remote assets
    """
    for asset in asset_list.local:
        matching_device = next(
            (device for device in asset_list.remote
                if device['Asset_Tag'] == asset.asset_tag), None)
        if matching_device:
            asset.jamf_id = matching_device['id']
            # This isn't ideal, but we need to sync the serial
            # number so it stays in jamf
            if asset.serial_number is None:
                asset.serial_number = matching_device['Serial_Number']
    return asset_list


def get_building_id(building_name: str) -> str:
    """
    Gets building Id used by Jamf from string abbreviation 

    Args:
        building_name (str): String abbreviation of building

    Returns:
        String: String representation of building ID number
    """
    # We return 0 as an int to unset the building during unassign
    if building_name == '0':
        return None

    response = jamf_p.get_buildings()
    jamf_buildings = []
    jamf_buildings.extend(response['results'])
    return [building['id'] for building in jamf_buildings
            if building['name'] == building_name][0]


def sync_assets_to_jamf(asset_list: List[Asset]) -> None:
    """
    Syncs data from local assets to Jamf Pro server.

    Structure of payload can be found on Jamf's API doc:
    https://developer.jamf.com/jamf-pro/reference/patch_v2-mobile-devices-id
    https://developer.jamf.com/jamf-pro/reference/patch_v1-computers-inventory-detail-id

    Args:
        asset_list (Assets): Obj of assets being worked with. 
            See Assets class for structure.
    """
    j_logger.debug('Syncing assets to Jamf')

    for asset in asset_list:
        # Process for mobile devices
        if asset.device_type == 'mobile':
            payload = {
                "location": {
                    "realName": asset.student_name,
                    "emailAddress": asset.email_address,
                    "room": asset.homeroom,
                    "buildingId": get_building_id(asset.building),
                    "position": "",
                    "phoneNumber": "",
                },
                "updatedExtensionAttributes": [
                    {
                        "name": "Grade",
                        "value": [asset.student_grade],
                    },
                    {
                        "name": "Owner",
                        "value": [asset.owner],
                    }
                ],
                # This is set because it allows techs to see asset tag from settings on device
                "name": asset.asset_tag,
                "enforceName": True
            }

            jamf_p.update_mobile_device(payload, asset.jamf_id)
            j_logger.info("Asset: %s Ok", asset.asset_tag)

        # Process for computers
        if asset.device_type == 'computer':
            payload = {
                "userAndLocation": {
                    "realname": asset.student_name,
                    "email": asset.email_address,
                    "position": asset.position,
                    "phone": "",
                    "buildingId": get_building_id(asset.building),
                    "room": asset.homeroom,
                    "extensionAttributes": [
                        {
                            "definitionId": "4",
                            "name": "Grade",
                            "values": [
                                asset.student_grade
                            ]
                        },
                        {
                            "definitionId": "3",
                            "name": "GradYear",
                            "values": [
                                asset.grad_year
                            ]
                        }
                    ]
                }
            }

            jamf_p.update_computer_inventory(payload, asset.jamf_id)
            j_logger.debug("Asset: %s Ok", asset.asset_tag)


def get_single_computer_record_by_asset_tag(asset_tag: str):
    j_logger.debug("Asset Tag: %s", asset_tag)
    # This endpoint allows us to filter by asset tag so we
    # only need to get the device we need
    endpoint_filter = f'general.assetTag==\"{asset_tag}\"'
    response = jamf_p.get_computer_inventories(
        section=["GENERAL"], filter=endpoint_filter)
    if response["totalCount"] >= 1:
        return response["results"]
    else:
        raise JautomateException("Computer record could not be found.")


def update_computer_jamf_ids(asset_list: Assets):
    for asset in asset_list.local:
        matching_device = next(
            (device for device in asset_list.remote
                if device['general']['assetTag'] == asset.asset_tag), None)
        if matching_device:
            asset.jamf_id = matching_device['id']
    return asset_list
