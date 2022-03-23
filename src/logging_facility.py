# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=invalid-name,line-too-long

import logging

def logger_initialize(loglevel):
    """
    Initialize logger instance common to the framework
    """
    # Get the instance of the root logger to set level for forge and 3rd party libs.
    logger = logging.getLogger('')

    # Setup handler printing to console
    logger_handler = logging.StreamHandler()
    logger.addHandler(logger_handler)

    # Parse the logging level specified as string (most likely from the config file)
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logger.setLevel(numeric_level)

    # make paramiko logger from fabric quiet
    paramiko_sftp_logger = logging.getLogger('paramiko')
    paramiko_sftp_logger.setLevel(logging.WARN)

    # This is the only message that is logged using the 'print' function because we
    # always want to have this message printed. Further log messages should go through
    # the logger.
    print('Logger has been successfully initialized to %s level' % loglevel.upper())
