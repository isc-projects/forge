# Copyright (C) 2013 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
