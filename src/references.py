# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

from src.forge_cfg import step

#
# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#


@step(r'References: (\S+).')
def references_check(references):
    assert len(references), "References cannot be empty."


@step(r'Tags: (\S+)')
def tags_check(tags):
    assert len(tags), "Tags cannot be empty."
