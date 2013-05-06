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

import re
from xml.dom.minidom import *

# Exception thrown when parsing JUnit file failed
class JUnitFormatError(Exception):
    pass

def shortClassName(classname):
    m = re.split(':', classname)
    if (len(m) == 2):
        return m[1].strip()

    return classname

def setIntegerAttribute(doc, parent_node, attr_name, new_value):
    """
    Set the tag's attribute to a given integer value
    """
    new_attr = doc.createAttribute(attr_name)
    new_attr.nodeValue = str(new_value)
    parent_node.setAttributeNodeNS(new_attr)

def increaseIntegerAttribute(doc, parent_node, attr_name, add_value):
    """
    Increase the integer value of the attribute by a specified
    value. If attribute is not present, it is created.
    """
    attr = parent_node.getAttributeNode(attr_name)
    if not attr:
        setIntegerAttribute(doc, parent_node, attr_name, add_value)
        return

    current_value = int(attr.nodeValue)
    current_value = current_value + 1
    attr.nodeValue = str(current_value)

def createAggregatedTestCase(doc, parent_node, testclass_name):
    """
    Create a node which represents a single aggregated testcase.
    Aggregated testcase sums the result of all test cases that
    belong to the speified classname. If one of these test cases
    fails, the aggregated test case's status is set to failed.
    """
    testcase = doc.createElement('testcase')
    testcase.setAttribute('classname', testclass_name)
    testcase.setAttribute('name', testclass_name)
    testcase.setAttribute('time', "0")
    return testcase


def aggregateTestSuite(doc, testsuite):
    """
    Aggregate results for a particular test suite.
    """
    testcases = testsuite.getElementsByTagName('testcase')
    aggregated_testcase = None
    setIntegerAttribute(doc, testsuite, 'failures', 0)
    setIntegerAttribute(doc, testsuite, 'errors', 0)
    for testcase in testcases:
        testclass_name = testcase.getAttributeNode('classname').nodeValue
        if not testclass_name:
            raise JUnitFormatError('testcase tag lacks classname attribute')

        if aggregated_testcase == None:
            aggregated_testcase = createAggregatedTestCase(doc, testsuite,
                                                           shortClassName(testclass_name))
            testsuite.appendChild(aggregated_testcase)
        else:
            aggregated_classname = aggregated_testcase.getAttributeNode('classname')
            if ((aggregated_classname) and
                (shortClassName(testclass_name) != aggregated_classname.nodeValue)):
                aggregated_testcase = createAggregatedTestCase(doc, testsuite,
                                                               shortClassName(testclass_name))
                testsuite.appendChild(aggregated_testcase)

        if testcase.getElementsByTagName('failure').length > 0:
            increaseIntegerAttribute(doc, testsuite, 'failures', 1)

        testsuite.removeChild(testcase)

    testcases = testsuite.getElementsByTagName('testcase')
    setIntegerAttribute(doc, testsuite, 'tests', testcases.length)

# Parse the XML document
result_dom = parse('lettucetests.xml')

# It must contain at least one test suite
test_suite = result_dom.getElementsByTagName('testsuite')
if test_suite.length == 0:
    raise JUnitFormatErrror('testsuite tag not found')

# Currently we will have just one test suite anyway.
aggregateTestSuite(result_dom, test_suite[0])

f = open('lettucetests-aggregated.xml', 'w+')
try:
    f.write(result_dom.toprettyxml())
except IOError:
    close(f)
    print 'Unable to write the output XML file'

print 'Output file has been saved successfully'
