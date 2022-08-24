'''
    DAS - Dracoon Automation Scripts
    Copyright (C) 2022 Universitaetsklinikum Bonn AoeR

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
import configparser
import sys

from pathlib import Path


def load_config(config_file, log_level_overwrite=None):
    config = configparser.ConfigParser()
    config_file = Path(config_file)
    if not config_file.exists():
        sys.exit('config file not found: {}'.format(config_file))
    config.read(config_file)
    if log_level_overwrite is not None:
        config['Logging']['logLevel'] = log_level_overwrite
    return config
