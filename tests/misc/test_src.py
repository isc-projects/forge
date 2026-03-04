# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""One test for any helper classes and functions defined in src."""

import pytest

from src.misc import Version


# pylint: disable = unnecessary-negation
@pytest.mark.src
def test_src():
    assert not Version('5.4.3') < Version('5.4.3')

    assert Version('5.4.2') < Version('5.4.3')
    assert not Version('5.4.3') < Version('5.4.2')

    assert Version('5.4.3') < Version('5.4.30')
    assert not Version('5.4.30') < Version('5.4.3')

    assert Version('5.4') < Version('5.4.3')
    assert not Version('5.4.3') < Version('5.4')

    assert Version('5.4.3') < Version('5.6')
    assert not Version('5.6') < Version('5.4.3')

    assert Version('5') < Version('5.0.1')
    assert not Version('5.0.1') < Version('5')

    assert Version('5.4.3') < Version('6')
    assert not Version('6') < Version('5.4.3')

    with pytest.raises(ValueError):
        Version('version')
