#!/usr/bin/env python3

# Copyright (C) 2019-2019 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
import sys
import os
import re


def load_steps():
    steps = []
    funcs = set()
    for fname in os.listdir('features'):
        if not fname.endswith('.py'):
            continue
        path = os.path.join('features', fname)
        with open(path) as f:
            regex = None
            for line in f:
                line = line.strip()

                if regex:
                    func = line.split(' ')[1].split('(')[0]
                    if func in funcs:
                        raise Exception("Func '%s' from '%s' already present" % (func, fname))
                    else:
                        funcs.add(func)
                    steps.append((regex, fname, func))
                    regex = None

                if not line.startswith('@step('):
                    continue
                regex = line[7:-2]

    return steps


def _find_matching_func(steps, line):
    # if 'Server MUST NOT respond' in line:
    #     print('  %r' % line)
    for regex, fname, func in steps:
        # if 'Server MUST NOT respond' in line:
        #     print('  %r' % regex)
        m = re.search(regex, line)
        if m:
            # print('match %s' % str(m.groups()))
            # print('  %r' % line)
            # print('  %r' % regex)
            return fname, func, m.groups(), regex
    raise Exception("no match for '%s'" % line)


def parse_feature_file(feature_file_path, steps):
    scenarios_list = []
    used_modules = set()

    scenario = None
    with open(feature_file_path) as f:
        for lineno, line in enumerate(f):
            try:
                line = line.rstrip()
                sline = line.strip()

                if line.startswith('Feature:'):
                    feature = line[9:]
                    continue

                if sline.startswith('@'):
                    sline = sline.replace('@', '')
                    tags = [t for t in sline.split(' ') if t]
                    scenario = None
                    continue

                if sline.startswith('Scenario:'):
                    scen_name = sline[10:]
                    scenario = dict(name=scen_name, tags=tags, commands=[])
                    scenarios_list.append(scenario)
                    continue

                if scenario:
                    if sline.startswith('#'):
                        scenario['commands'].append(('comment', sline[1:].strip()))
                        continue

                    if sline == '':
                        scenario['commands'].append(('empty-line', ''))
                        continue

                    step = _find_matching_func(steps, sline)
                    used_modules.add(step[0])
                    cmd = (step, sline)
                    scenario['commands'].append(cmd)
            except:
                print("problem in line %s: '%s'" % (lineno + 1, line))
                raise

    return feature, scenarios_list, used_modules


def generate_py_file(feature, scenarios_list, used_modules, py_file_path):
    with open(py_file_path, 'w') as f:
        f.write('"""%s"""\n' % feature)
        f.write("\n")

        f.write("# pylint: disable=invalid-name,line-too-long\n\n")

        f.write("import pytest\n")

        f.write("\n")

        for mod in used_modules:
            mod = mod.replace('.py', '')
            f.write("from features import %s\n" % mod)
        f.write("\n\n")

        for idx, scen in enumerate(scenarios_list):

            for tag in scen['tags']:
                f.write("@pytest.mark.%s\n" % tag.replace('-', '_'))

            name = scen['name']
            name = name.replace('.', '_')
            name = name.replace('-', '_')
            name = 'test_' + name
            f.write("def %s():\n" % name)

            # count last empty lines
            last_non_empty = 0
            for step, line in reversed(scen['commands']):
                if step == 'empty-line':
                    last_non_empty += 1
                else:
                    break

            # print('!! %s %s/%s' % (name, last_non_empty, len(scen['commands'])))

            if last_non_empty > 0:
                stripped_commands = scen['commands'][:-last_non_empty]
            else:
                stripped_commands = scen['commands']

            was_empty_line = False
            for step, line in stripped_commands:
                if step == 'comment':
                    t = '    # %s' % line.strip('#')
                    f.write(t.rstrip() + '\n')
                    continue

                # if there is more than 1 empty line then print only 1
                if step == 'empty-line':
                    if not was_empty_line:
                        f.write('\n')
                    was_empty_line = True
                    continue
                else:
                    was_empty_line = False

                # print('       %s' % line)

                # f.write('    # %s\n' % line)  # original line in comment
                mod = step[0].replace('.py', '')
                func = step[1]
                args1 = step[2]
                args = []
                for arg in args1:
                    if arg is None:
                        arg = 'None'
                    else:
                        arg = arg.replace("'", "\\'")
                        arg = "'%s'" % arg
                        if r'\[' in arg:
                            arg = 'r' + arg
                    args.append(arg)

                args2 = ", ".join(args)

                # try to build one long line
                new_line = '    %s.%s(%s)\n' % (mod, func, args2)
                # if length not to much then ok
                if len(new_line) < 100 or len(args) <= 1:
                    f.write(new_line)
                    continue

                # if line to long, try to divide it by arguments
                new_line = '    %s.%s(' % (mod, func)
                spaces_num = len(new_line)
                new_line += '%s,\n' % args.pop(0)
                f.write(new_line)

                args_txt = ""
                for arg in args:
                    args_txt += " " * spaces_num
                    args_txt += "%s,\n" % arg
                args_txt = args_txt[:-2] + ')\n'
                f.write(args_txt)

            if idx < len(scenarios_list) - 1:
                f.write("\n")
                f.write("\n")


def main(feature_file_path):
    print("Converting file %s." % feature_file_path)

    steps = load_steps()
    print("Loaded %s step definitions." % len(steps))
    # for s in steps:
    #     print(s)

    feature, scenarios_list, used_modules = parse_feature_file(feature_file_path, steps)

    if feature_file_path.endswith('/logging.feature'):
        feature_file_path = feature_file_path.replace('/logging.feature', '/kea_logging.feature')

    py_file_path = feature_file_path.replace('.feature', '')
    p1, p2 = py_file_path.rsplit('/', 1)
    p2 = p2.replace('.', '_').replace('-', '_')
    p2 = p2.lower()
    p2 = 'test_%s.py' % p2
    py_file_path = os.path.join(p1, p2)

    generate_py_file(feature, scenarios_list, used_modules, py_file_path)
    print('Saved to %s' % py_file_path)

    print('Feature: %s' % feature)
    # for idx, scen in enumerate(scenarios_list):
    #     print('%s. Scenario: %s' % (idx, scen['name']))
    #     print('  Tags: %s' % scen['tags'])
    #     print('  Commands:')
    #     for cmd in scen['commands']:
    #         print('      %s' % str(cmd))
    #     print('')


if __name__ == '__main__':
    main(sys.argv[1])
