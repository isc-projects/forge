#!/usr/bin/python
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
#
# author: Wlodzimierz Wencel

import datetime
import os
import sys


class TestHistory ():
    def __init__(self):
        self.date = self.present_time()
        self.start_time = None
        self.stop_time = None
        self.time_elapsed = None
        self.passed = 0
        self.ran = 0
        self.failed = 0
        self.percent = 0.0
        self.tags = None
        self.path = None

        from features.init_all import SOFTWARE_UNDER_TEST
        self.software_type = str(SOFTWARE_UNDER_TEST)

        #TODO: implement this
        self.bind10_version = "N/A"
        self.dibbler_version = "N/A"
        self.isc_dhcp_version = "N/A"

        self.check_file()

    def present_time(self):
        return datetime.datetime.now()

    def start(self):
        self.start_time = self.present_time()

    def information(self, passed, ran, tags, path):
        self.stop_time = self.present_time()
        self.passed = passed
        self.ran = ran
        self.failed = ran - passed
        if ran > 0:
            self.percent = (1.0 * passed/ran) * 100
        else:
            self.percent = 0
        self.tags = tags
        self.path = path

    def check_file(self):
        if not os.path.exists('history.html'):
            new_file = open('history.html', 'w')
            new_file.close()

    def build_report(self):
        scenarios = self.read_result()
        scenarios.reverse()
        scenarios_html = '<tr><th colspan="2" align = left>TESTS:</th></tr><tr><td>NAME:</td><td>RESULT:</td></tr>'

        for i in range(len(scenarios)/2):
            name = str(scenarios.pop())
            result = str(scenarios.pop())
            if 'True' in result:
                result = 'FAILED'
                color = 'red'
            elif 'False':
                result = 'PASSED'
                color = 'green'
            else:
                result = 'N/A'
                color = 'black'
            scenarios_html += '<tr><td>'+name+'</td><td bgcolor = \''+color+'\'>'+result+'</td></tr>'

        report = open('history.html', 'a')
        self.time_elapsed = self.stop_time - self.start_time
        report.write('<table border = \'1\' style = \"font-family: monospace; font-size:12\"><tr><td>DATE:</td><td>'
                     + str(self.date.year)+'.'+str(self.date.month)+'.'+str(self.date.day)+'; '+str(self.date.hour)+':'
                     + str(self.date.minute)+'</td></tr><tr><td> SOFTWARE TYPE: </td><td>'+self.software_type
                     + '</td></tr><tr><td> TAGS: </td><td>'+str(self.tags)+' </td></tr><tr><td> PATH: </td><td>'
                     + str(self.path)+' </td></tr><tr><td> RAN: </td><td>'+str(self.ran)
                     + ' </td></tr><tr><td> PASSED: </td><td>'+str(self.passed)+' </td></tr><tr><td> FAILED: </td><td>'
                     + str(self.failed)+' </td></tr><tr><td> PASS-RATE: </td><td>'+str('%2.3f' % self.percent)
                     + ' </td></tr><tr><td> TIME ELAPSED: </td><td>'+str(self.time_elapsed)
                     + ' </td></tr>'+scenarios_html+'</table><br/>\n')
        report.close()

    def read_result(self):
        res = []
        result = open('result', 'r')
        for line in result:
            res.append(line)
        result.close()

        os.remove('result')
        return res


class UserHelp ():
    def __init__(self):
        self.tags = ''
        self.all_tags = ''

    def check_tags(self, line):
        """
        Add only unique tags to list
        """
        tag_list = line.split('@')
        tag_list = [x.strip() for x in tag_list]
        for tag in tag_list:
            if tag is not None:
                if tag in self.tags or tag == 'v4' or tag == 'v6':
                    pass
                else:
                    self.tags += tag + ', '

    def test(self, ip_version, more):
        """
        Generate list of test sets, features, test names and all available tags
        """
        #  make for each in number because it starts in two points: in forge.py by using -l option,
        #  then it create list only for one IP version,
        #  and in help.py generating whole test list.

        print "Test tree schema:\nroot directory\n\ttest set (available by option -s in forge.py)\n\t\ttest feature"
        if more:
            print "\t\t\ttest name (available by option -n in forge.py)"
        for each_number in ip_version:
            self.tags = ''
            sets_number = 0
            features_number = 0
            tests_number = 0
            outline_tests_number = 0
            outline_generate_test = 0
            outline_tag = False
            freespace = "  "
            #  this code is ugly hack! make it much better
            print "\nIPv" + each_number + " Tests:"
            print "features/dhcpv" + each_number + "/"
            for path, dirs, files in os.walk("features/dhcpv" + each_number + "/"):
                if len(path[16:]) > 1 and len(path[16:]) < 10:
                    print freespace + path[16:]
                if len(path[23:]) > 1:
                    print freespace*2 + path[23:]
                    sets_number += 1
                for each_file in files:
                    print freespace*3, each_file[:-8], '\n', freespace*4, 'Test Names:'
                    features_number += 1
                    names = open(path + '/' + each_file, 'r')
                    for line in names:
                        line = line.strip()
                        if len(line) > 0:
                            if line[0] == '@':
                                self.check_tags(line)
                            elif "Scenario" in line:
                                if "Outline" in line:
                                    outline_tag = True
                                    outline_tests_number += 1
                                    if more:
                                        print freespace*6 + line[18:]
                                else:
                                    outline_tag = False
                                    tests_number += 1
                                    if more:
                                        print freespace*6 + line[10:]
                            elif "|" in line and outline_tag:
                                outline_generate_test += 1
                            else:
                                pass

                    names.close()
            print "Totally: \n\t", outline_generate_test + tests_number - outline_tests_number, "tests. ",\
                tests_number, "simple tests and", outline_tests_number, "multi-tests. Grouped in", features_number,\
                "features, and in", sets_number, "sets.\n\nTest tags you can use: \n", self.tags[:-2], "\n"

            if not more:
                print 'For more information, use help.py to generate UserHelp document.\n'

    def steps(self):
        """
        Generate list of available steps in tests.
        """
        files = ['srv_control', 'srv_msg']  # if you add file that help will be generated, add also description below.
        message = ['All steps available in preparing DHCP server configuration:',
                   'All steps available in building tests procedure:']

        for file_name, text in zip(files, message):
            steps = open('features/' + file_name + '.py', 'r')
            print '\n', text,
            for line in steps:
                line = line.strip()
                if len(line) > 0:
                    if line[0] == '#' and len(line) > 1:
                        if line[1] == '#':
                            print '\n\t', line[2:]
                    elif line[0] == '@':
                        print "\t\t    ", line[7:-2]
            steps.close()
        print "\nFor definitions of (\d+) (\w+) (\S+) check Python " \
              "regular expressions at http://docs.python.org/2/library/re.html"


def find_scenario(name, IPversion):
    from features.init_all import SOFTWARE_UNDER_TEST
    testType = ""
    for each in SOFTWARE_UNDER_TEST:
        if "client" in each:
            testType = "client"
        elif "server" in each:
            testType = "server"

    for path, dirs, files in os.walk("features/dhcpv" + IPversion + "/" + testType + "/"):
        for each_file in files:
            if not each_file.endswith('.feature') and not each_file.endswith('.py'):
                continue

            fpath = os.path.join(path, each_file)
            scenario_idx = 0
            with open(fpath, 'r') as f:

                if each_file.endswith('.feature'):
                    for line in f:
                        if 'Scenario' in line:
                            scenario_idx += 1
                            line = line.strip()
                            if name == line[10:]:
                                return os.path.join(path, each_file), str(scenario_idx)
                            elif name == line[18:]:
                                return os.path.join(path, each_file), str(scenario_idx)

                elif each_file.endswith('.py'):
                    prev_line_func = False
                    scen_docstr = '"""%s"""' % name
                    for line in f:
                        if prev_line_func and scen_docstr in line:
                            return os.path.join(path, each_file), str(scenario_idx)

                        if line.startswith('def test_'):
                            scenario_idx += 1
                            prev_line_func = True
                        else:
                            prev_line_func = False

    return None, 0


def find_scenario_in_path(name, path):
    from features.init_all import SOFTWARE_UNDER_TEST
    for each_software_name in SOFTWARE_UNDER_TEST:
        if "server" in each_software_name:
            testType = "server"
        elif "client" in each_software_name:
            testType = "client"

    scenario = 0
    for path, dirs, files in os.walk(path):
        for each_file in files:
            file_name = open(path + '/' + each_file, 'r')
            for each_line in file_name:
                if 'Scenario' in each_line:
                    scenario += 1
                    tmp_line = each_line.strip()
                    if name == tmp_line[10:]:
                        file_name.close()
                        return path + '/' + each_file, str(scenario)
                    elif name == tmp_line[18:]:
                        file_name.close()
                        return path + '/' + each_file, str(scenario)
            else:
                scenario = 0
                file_name.close()
    return None, 0

if __name__ == '__main__':
    #orginal_stdout = sys.stdout
    help_file = file('UserHelp.txt', 'w')
    sys.stdout = help_file
    generate_help = UserHelp()
    print """
                 FORGE - An Automated DHCP Validation Framework

1. Introduction
---------------
This is the user guide for Forge, the automated DHCP validation framework. It
covers setting up and running of the tests, and describes how to write new
tests.

Forge tests a DHCP server by starting it on the different machine than the one on
which Forge is running, sending it DHCP packets and checking the responses.
It also monitors the server's logging output: as well as allowing the framework
to check that the server has started and stopped correctly (Forge may restart
the server several times during its operation), monitoring the logging output
allows the reaction of the server to different events to be tested.

Forge uses Lettuce, a Python-based utility that allows tests to be
written in a semi-natural form of English.  As a result, the tests are
easily understood, and it is easy to learn how to write new tests.

Instructions for installation of Forge can be found in the file doc/info.txt
in the Forge git repository at:

    https://github.com/isc-projects/forge/blob/master/doc/info.txt

Further Forge documentation can be found at the Forge project web site:

    http://kea.isc.org/wiki/IscForge


2. Setting Up the Tests
-----------------------
Assuming that Forge has been installed, the first step is to create the
"lettuce/features/init_all.py" file.  This is a file that gives Forge
information about software being tested as well as setting parameters
for the tests.  The easiest way to do this is to copy the file
"lettuce/features/init_all.py_example" and edit it.  The file contains
comprehensive explanations of all the parameters.


3. Running the Tests
--------------------
Running the tests involves running the file "forge.py" with appropriate options.

Note: you must set your current directory to be the "lettuce" directory containing
"forge.py" first.

The options control what tests are run:

* All tests for IPv6:
    forge.py -6

* All tests from specific set e.g. relay_agent (one test set is a whole
  directory e.g. test_v6/address_validation):
    forge.py -6 -s relay_agent

* All tests from specific set with specific tag (e.g. "basic"):
    forge.py -6 -s relay_agent -t basic

* All tests with a specific tag (e.g. "basic"):
    forge.py -6 -t basic

  Multiple tags can be given, in which case Forge will run all tests with the
  first tag, then all tests with the second tag, e.g. to run the basic tests
  and the relay tests:

    forge.py -6 -t basic, relay

* To run a specific test, specify the test name, e.g.

    forge.py -6 -n v6.basic.message.unicast.solicit

The detail produced by the tests can be controlled with the Lettuce verbosity (-v option):

    1 - Print dots as each feature is executed
    2 - Print scenario names
    3 - Full feature print, but colorless
    4 - Full feature print, but colorful (this is the default level)


4. Writing New Tests
--------------------
The following is an example of a test.  Lines started with the '#'
character are comments are are ignored.

    # In Lettuce, a "feature" is a group of tests that check a particular
    # application feature.  It is introduced by a line starting with the word
    # "Feature:" giving a one-line description of the feature.  The "Feature:"
    # line is then followed by one or more lines containing a more detailed
    # explanation.

    Feature: Standard DHCPv6 address validation
        This feature is for checking the response to messages sent on a UNICAST
        address.  A Request message should be answered with a Reply message
        containing the option StatusCode with code 5.  Solicit, Confirm,
        Rebind, and Info-Request messages should be discarded.

    # In Lettuce, a test is known as a "scenario".  Each scenario has a name
    # and is identified by a line starting wiuth the "Scanario:" keyword.
    # Optionally, the "Scenario:" line is preceded by one or more tags (each
    # preceded by the "@" sign) that identifies the broad category in which
    # the scenario is grouped. These tags allow groups of tests to be selected
    # with the "-t" command-line option.

        @basic @v6 @unicast test name
        Scenario: v6.basic.message.unicast.solicit

    # Each scenario consists of a setup procedure, followed by one of more
    # sets of "Test Procedures" and "Pass Criteria".  In the "Test Procedure",
    # Lettuce executes a set of steps that exercise the software being tested.
    # The "Pass Criteria" block gets Lettuce to examine the results of the
    # test procedure.  Note that the setup steps only get executed once, at
    # the start of the scenario.  Thereafter the actions taken by the test
    # procedures and pass criteria following one another in the order written:
    # the software being tested is not reset between the blocks.
    #
    # The following setup procedure configures a DHCPv6 server with a subnet
    # and a pool comprising 256 addresses.  It then starts the server.

            Test Setup:
            Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
            DHCP Server is started.

    # The following steps now check the behavior of the server in response to a
    # sequence of packets. The first test procedure sets up a packet and, with
    # the "Client Sends" line, tells Lettuce to send the packet to the server

            Test Procedure:
            Client requests option 7.
            Client chooses UNICAST address.
            Client sends SOLICIT message.

    # The next block tells Lettuce to execute the code that checks the reply
    # sent by the server.

            Pass Criteria:
            Server MUST NOT respond with ADVERTISE message.

    # Another test procedure and check:

            Test Procedure:
            Client requests option 7.
            Client sends SOLICIT message.

            Pass Criteria:
            Server MUST respond with ADVERTISE message.

    # Finally, there is an optional line (for documentation purposes only)
    # that refers to the document describing the behavior being tested.

            References: RFC3315 section 15

Note: Each section in the test ("Test Procedure", "Pass Criteria" etc.)
starts with the name of the section and ends with the colon character.
The "Test Procedure" and "Pass Criteria" section comprise a set of statements,
each ending with the period character ('.').  Although virtually all the
section names and statements have been put into separate lines in the example
above, there is no need to: they can be put on one line, as is the case with
the "Feature", "Scanario" and "References" sections.

Where a number of scenarios are similar, a "Scenario Outline" may be used
instead of a Scenario.  Here, the scenario include placeholders, plus a list of
substitution values.  Lettuce will run the scenario a number of times, each time
using a different substitution value.  The following example illustrates this.

# As expected, a scenario Outline" is introduced by the "Scenario Outline"
# keywords.  As with "Scenario", the Scenario Outline line is preceded by the
# list of tags.

    @v6 @solicit_invalid @invalid_option @outline
    Scenario Outline: v6.solicit.invalid.options.outline

        Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is started.

# The following test procedure now uses a placeholder for one of its values.
# In this case, the placeholder is named opt_name.  A placeholder is indicated
# by enclosing the name between the '<' and '>' angle brackets, e.g. '<opt_name>'.

        Test Procedure:
        Client requests option 7.
        Client does include <opt_name>.
        Client sends SOLICIT message.

        Pass Criteria:
        Server MUST NOT respond with ADVERTISE message.

        Test Procedure:
        Client requests option 7.
        Client sends SOLICIT message.

        Pass Criteria:
        Server MUST respond with ADVERTISE message.

        References: RFC3315 section 15.2, 17.2.1

# There now follows the "Examples:" section containing the list of substitution
# values for the place holder.

        Examples:
            | opt_name       |
            | relay-msg      |
            | preference     |
            | server-unicast |
            | status-code    |
            | interface-id   |
            | reconfigure    |

# The contents of the examples section is a table, using the vertical bar '|' as
# separators between columns.  The first row of each column is the name of the
# option and the subsequent rows are the substitution values.  Multiple options
# can be used within a scenario outline: all substitution values are specified
# in the examples section, in multiple column tables, e.g. if the outline uses
# the place holders "node_name" and "address", they would be specified as:
#
#       Examples:
#           | node_name | address  |
#           | foo       | 3000::25 |
#           | bar       | 3000::26 |
#           |    :      |     :    |

More information about Scenario Outlines can be found at:

    http://pythonhosted.org/lettuce/intro/wtf.html#outlined.

Unfortunately Lettuce is little complex with scenario outlines. They are not
scenarios so Lettuce features like @after.each_scenario (not illustrated in
the above examples) are not considered when they are executed.  Instead, you
need to use command such as @before.outline and @after.outline (which are not
mentioned in the current Lettuce documentation).

The following steps are available:"""
    generate_help.steps()
    help_file.flush()
    print """
(All the information above was automatically generated by parsing two files:

        srv_msg.py
        srv_control.py

in the directory lettuce/features.  As you can see, the test steps marked with
'@step' and the family of steps family is marked with '##' (don't remove #,
it needs to be double)).

Writing new steps is outside the scope of this guide.  However, if you do,
please ensure that they are added to the correct family.

4.1 Tips for Writing Tests
--------------------------
* Do NOT use 'Scenario' in tests other than to set the test name. The "Scenario"
  line must come right below the tags (e.g. @my_tag)

* When writing a tag, do not separate the "@" from the name of the tag with a space, i.e.

        good tag: @basic
        bad tag:  @ basic

* For efficiency, DO NOT put a lot of different tags in one feature. It takes
  a lot of time for lettuce to to parse them tags. It's better to create two
  separate features (as it is with options.feature in options_validation set).

* "Test Procedure" and "Pass Criteria" can be used multiple times in a scenario.  If
  "Test Setup" appears twice, the remote server will be stopped, the configuration
  removed, a new configuration generated, and the server restarted.

5. Full List of Tests
---------------------
The complete set of tests availabole in Forge is listed here.  This list
(in fact, this entire document) is generated programatically by the script
"help.py".  If you add additional tests, run help.py and they will be included
in the list:
"""
    generate_help.test(["4", "6"], 1)
    help_file.flush()
    print """Tests are simple Scenarios, multi-test are Scenario Outlines.
"""
    help_file.close()

    #sys.stdout = orginal_stdout
