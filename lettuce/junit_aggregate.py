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
    """
    Extract short test class name from the default class name constructed
    by lettuce. The default class name consists of the 'Feature' name and
    'Scenario' name, separated with double colon. This function returns only
    trimmed scenario name.
    """
    m = re.split(':', classname)
    # We are having an expected format of the class name. Let's return
    # the second element assuming it is a 'Scenario' name.
    if (len(m) == 2):
        return m[1].strip()
    # If it is not expected format of the class name then no-op.
    return classname

def setNumericAttribute(doc, parent_node, attr_name, new_value):
    """
    Set the tag's attribute to a given numeric value.
    """
    new_attr = doc.createAttribute(attr_name)
    new_attr.nodeValue = str(new_value)
    # Replace any existing attribute with the new one.
    parent_node.setAttributeNodeNS(new_attr)

def increaseNumericAttribute(doc, parent_node, attr_name, add_value,
                             is_float = False):
    """
    Increase the numeric value of the attribute by a specified
    value. If an attribute is not present, it is created.
    """
    # We want to increase the value of the attribute so we have to
    # first get ths current value.
    attr = parent_node.getAttributeNode(attr_name)
    # If there is no attribute we have to create one, with the
    # initial value equal add_value.
    if not attr:
        setNumericAttribute(doc, parent_node, attr_name, add_value)
        return
    # If there is an attribute already, increase the value.
    current_value = 0
    if (is_float):
        current_value = float(attr.nodeValue)
    else:
        current_value = int(attr.nodeValue)

    current_value = current_value + add_value
    attr.nodeValue = str(current_value)

def createAggregatedTestCase(doc, parent_node, testclass_name):
    """
    Create a node which represents a single aggregated testcase.
    Aggregated testcase sums the result of all test cases that
    belong to the speified classname. If one of these test cases
    fails, the aggregated test case's status is set to failed.
    """
    testcase = doc.createElement('testcase')
    # This holds the complete test id.
    testcase.setAttribute('classname', testclass_name)
    # classname holds the whole test id already, so the 'name'
    # attribute holds just a persistent label, common to all
    # test cases. Let's call it aggregated, to indicate that
    # the result represents multiple steps in lettuce scenario.
    testcase.setAttribute('name', 'aggregated')
    testcase.setAttribute('time', "0")
    return testcase


def aggregateTestSuite(doc, testsuite):
    """
    Aggregate results for a particular test suite.
    """
    # Iterate over all <testcase> tags.
    testcases = testsuite.getElementsByTagName('testcase')
    # This will hold a single instance of 'testcase' which will
    # represent multiple testcases within the input XML.
    aggregated_testcase = None
    # Reset counters in <testsuite> tag.
    setNumericAttribute(doc, testsuite, 'failures', 0)
    setNumericAttribute(doc, testsuite, 'errors', 0)

    # Go over all testcases.
    for testcase in testcases:
        # Class name holds test identifier, so if it is missing we can't
        # differentiate between testcases. Therefore, it is a fatal error.
        testclass_name = testcase.getAttributeNode('classname').nodeValue
        if not testclass_name:
            raise JUnitFormatError('testcase tag lacks classname attribute')
        # It is None in case, we are processing the first element in testsuite.
        if aggregated_testcase == None:
            aggregated_testcase = createAggregatedTestCase(doc, testsuite,
                                                           shortClassName(testclass_name))
            testsuite.appendChild(aggregated_testcase)
        else:
            aggregated_classname = aggregated_testcase.getAttributeNode('classname')
            # If the class name of the currently processed <testcase> tag and the name
            # of the one we processed previously are different, it means that we have
            # just switched to the new class of tests and the aggregation of the
            # tests for a particular classname is done. Thus, we create new instance
            # of the aggregated test case and append it.
            if ((aggregated_classname) and
                (shortClassName(testclass_name) != aggregated_classname.nodeValue)):
                aggregated_testcase = createAggregatedTestCase(doc, testsuite,
                                                               shortClassName(testclass_name))
                testsuite.appendChild(aggregated_testcase)

        # Presence of the tag <failure> indicates that the particular testcase
        # in the input results failed. In such case we have to mark aggregated
        # testcase failed.
        testcase_failures = testcase.getElementsByTagName('failure')
        if testcase_failures.length > 0:
            increaseNumericAttribute(doc, testsuite, 'failures', 1)
            # For now let's append just one failure. Is it possible to
            # have more than one?
            aggregated_testcase.appendChild(testcase_failures[0])

        # Update aggregated time.
        testcase_time = testcase.getAttributeNode('time')
        if not testcase_time:
            raise JUnitFormatError('testcase lacks time attribute')
        # The value of 'time' for the currently processed tag is added
        # to the current 'time' value of the aggregated testcase.
        increaseNumericAttribute(doc, aggregated_testcase, 'time',
                                 float(testcase_time.nodeValue), True)

        # testsuite tag holds total time, so we have to update it too.
        increaseNumericAttribute(doc, testsuite, 'time',
                                 float(testcase_time.nodeValue), True)

        # We have processed single <testcase> tag, we can now remove it from DOM.
        testsuite.removeChild(testcase)

    # We have processed all <testcase> tags. Now we only have <testcase> tags,
    # which represent aggregated results. Let's count them, and update the
    # corresponding 'tests' counter in <testsuite> tag.
    testcases = testsuite.getElementsByTagName('testcase')
    setNumericAttribute(doc, testsuite, 'tests', testcases.length)

# Parse the XML document
result_dom = parse('lettucetests.xml')

# It must contain at least one test suite
test_suite = result_dom.getElementsByTagName('testsuite')
if test_suite.length == 0:
    raise JUnitFormatErrror('testsuite tag not found')

# Currently we will have just one test suite anyway.
aggregateTestSuite(result_dom, test_suite[0])

# We have chosen the arbitrary name for the output file for simplicity of the
# script. At some point, we may want to make it configurable.
f = open('lettucetests-aggregated.xml', 'w+')
try:
    f.write(result_dom.toprettyxml())
except IOError:
    close(f)
    print 'Unable to write the output XML file'

print 'lettucetests-aggregated.xml has been saved successfully'
