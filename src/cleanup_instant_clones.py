#! /usr/bin/env python3
'''
    DIAS - DI Automation Scripts
    Copyright (C) 2022 Universitaetsklinikum Bonn AoeR
    This Script is inspired by non_persistent_vdi_cleanup.py from 
    https://github.com/pvz01/deepinstinct_rest_api_wrapper

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

import argparse
import logging
import deepinstinct30 as di

from datetime import datetime
from sys import exit
from helper.logging import setup_logging
from helper.config import load_config

PROGRAM_NAME = 'CleanUp Instant VDI Clones'
PROGRAM_VERSION = '0.0.1'
PROGRAM_DESCRIPTION = 'remove temporary DI clients'


def _setup_argparser():
    parser = argparse.ArgumentParser(description='{} - {}'.format(PROGRAM_NAME, PROGRAM_DESCRIPTION))
    parser.add_argument('-c', '--config_file', default='./dias.cfg', help='load a config file')
    parser.add_argument('-L', '--log_level', help='define the log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default=None)
    parser.add_argument('-V', '--version', action='version', version='{} {}'.format(PROGRAM_NAME, PROGRAM_VERSION))
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='print debug messages')
    parser.add_argument('-s', '--silent', action='store_true', default=False, help='disable console output')
    return parser.parse_args()


def get_offline_vdi_clones(devices, tag, group, offline_hours=12):
    offline_clones = list()
    now = datetime.utcnow()
    
    for device in devices:
        if 'tag' in device:
            if device['tag'] == tag:
                if device['group_name'] == group:
                    if device['connectivity_status'] == 'OFFLINE':
                        if device['deployment_status'] == 'REGISTERED':
                            last_contact = datetime.fromisoformat(device['last_contact'].replace('Z',''))
                            if (now - last_contact) > datetime.timedelta(hours=offline_hours):
                                offline_clones.append(device)
    return offline_clones


def remove_devices(devices):
    for device in devices:
        logging.info('removing device {}: {}'.format(device['id'], device['hostname']))
        di.remove_device(device)
    

if __name__ == '__main__':
    args = _setup_argparser()
    config = load_config(args.config_file, log_level_overwrite=args.log_level)
    setup_logging(args, config)
    
    di.fqdn = config['Appliance']['fqdn']
    di.key = config['Appliance']['api_key']
    
    devices = di.get_devices(include_deactivated=False)
    
    offline_clones = get_offline_vdi_clones(devices, config['Cleanup_VDI_instant_clones']['tag'], config['Cleanup_VDI_instant_clones']['group'])
    
    remove_devices(offline_clones)

    exit()
