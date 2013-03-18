# Copyright (C) 2013 Internet Systems Consortium, Inc. ("ISC")
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS.  IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

# Author: Tomek Mrugalski

Feature: DHCPv4 options
    This is a simple DHCPv4 options validation. Its purpose is to check
    if requested option are assigned properly.

    Scenario: v4.options.subnet-mask
    # Checks that server is able to serve subnet-mask option to clients.

        Test Setup:
        Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
        #Server is configured with subnet-mask option with value 255.255.255.0.
        #Server is started.

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    #Server MUST respond with OFFER message.
    #Response MUST include option 1.
    #Response option 1 MUST contain value 255.255.255.0.

    #References: v4.options, v4.prl, RFC2131

    #Tags: v4 options subnet automated
