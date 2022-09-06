#! /usr/bin/env python3
'''
    DIAS - DI Automation Scripts
    Copyright (C) 2022 Universitaetsklinikum Bonn AoeR
    This Script is inspired by deepinstinct30.py from 
    https://github.com/pvz01/deepinstinct_rest_api_wrapper written by
    Patrick Van Zandt, Principal Professional Services Engineer, Deep Instinct

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import requests
import time
import logging


def get_devices(fqdn, api_key, include_deactivated=True):
    last_id = 0
    collected_devices = []
    headers = {'accept': 'application/json', 'Authorization': api_key}

    # The method we are using (/api/v1/devices) returns up to 50 devices at a
    # time, and the response includes a last_id which indicates the highest
    # device id returned. We will know we have all devices visible to our API
    # key when we get last_id=None in a response.

    error_count = 0
    while last_id != None and error_count < 10: #loop until all visible devices have been collected
        #calculate URL for request
        request_url = f'https://{fqdn}/api/v1/devices?after_device_id={last_id}'
        #make request, store response
        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            response = response.json() #convert to Python list
            if 'last_id' in response:
                last_id = response['last_id'] #save returned last_id for reuse on next request
            else: #added this to handle issue where some server versions fail to return last_id on final batch of devices
                last_id = None
            logging.debug('{} returned 200 with last_id {}'.format(request_url, last_id))
            if 'devices' in response:
                devices = response['devices'] #extract devices from response
                for device in devices: #iterate through the list of devices
                    if device['license_status'] == 'ACTIVATED' or include_deactivated:
                        collected_devices.append(device) #add to collected devices
        else:
            logging.error('Unexpected return code {} on request to "{}" with headers "{}"'.format(response.status_code, request_url, headers))
            error_count += 1  #increment error counter
            time.sleep(10) #wait before trying request again
    logging.info('{} devices found'.format(len(collected_devices)))
    return collected_devices


def remove_device(fqdn, api_key, device_id):
    request_url = f'https://{fqdn}/api/v1/devices/{device_id}/actions/remove'
    headers = {'Authorization': api_key}
    response = requests.post(request_url, headers=headers)
    if response.status_code == 204:
        logging.info('Successfully removed device: {}'.format(device_id))
    else:
        logging.error('Failed to remove device: {}'.format(device_id))
