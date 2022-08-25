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
import logging


def setup_logging(args, config):
    try:
        log_level = config['Logging']['logLevel']
    except Exception:
        logging.error('no log level set in config')
        log_level = "INFO"
    log_format = logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    
    if args.debug:
        log_level = "DEBUG"

    if not args.silent:
        console_logger = logging.StreamHandler()
        console_logger.setLevel(log_level)
        console_logger.setFormatter(log_format)
        logger.addHandler(console_logger)

    try:
        log_file = config['Logging']['logFile']
    except Exception:
        logging.error('no log file set in config')
        log_file = 'dias.log'
    file_log = logging.FileHandler(log_file)
    file_log.setLevel(log_level)
    file_log.setFormatter(log_format)
    logger.addHandler(file_log)
