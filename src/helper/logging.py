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


def _get_log_level(args, config):
    if args.debug:
        return 'DEBUG'
    else:
        try:
            return config['Logging']['logLevel']
        except Exception:
            logging.warning('no log level set in config. Setting log level to INFO')
            return "INFO"


def _setup_console_logger(log_level, log_format):
    console_logger = logging.StreamHandler()
    console_logger.setLevel(log_level)
    console_logger.setFormatter(log_format)
    return(console_logger)


def _setup_file_logger(log_level, log_format, config):
    try:
        log_file = config['Logging']['logFile']
    except Exception:
        logging.error('no log file set in config')
        log_file = 'dias.log'
    file_logger = logging.FileHandler(log_file)
    file_logger.setLevel(log_level)
    file_logger.setFormatter(log_format)
    return file_logger
    
     
def setup_logging(args, config):
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    
    log_level = _get_log_level(args, config)
    log_format = logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if not args.silent:
        logger.addHandler(_setup_console_logger(log_level, log_format))

    logger.addHandler(_setup_file_logger(log_level, log_format, config))
