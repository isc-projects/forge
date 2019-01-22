#!/usr/bin/env python3

# Copyright (C) 2019-2019 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import re


def load_steps():
    #@step('Client requests option (\d+).')
    steps = []
    funcs = set()
    for fname in os.listdir('features'):
        if not fname.endswith('.py'):
            continue
        path = os.path.join('features', fname)
        with open(path) as f:
            regex = None
            for l in f:
                l = l.strip()

                if regex:
                    func = l.split(' ')[1].split('(')[0]
                    if func in funcs:
                        raise Exception("Func '%s' from '%s' already present" % (func, fname))
                    else:
                        funcs.add(func)
                    steps.append((regex, fname, func))
                    regex = None

                if not l.startswith('@step('):
                    continue
                regex = l[7:-2]

    return steps


def _find_matching_func(steps, line):
    if 'Server MUST NOT respond' in line:
        print('  %r' % line)
    for regex, fname, func in steps:
        if 'Server MUST NOT respond' in line:
            print('  %r' % regex)
        m = re.search(regex, line)
        if m:
            print('match %s' % str(m.groups()))
            print('  %r' % line)
            print('  %r' % regex)
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
                    tags = sline.split(' ')
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
        f.write("\n\n")

        f.write("import sys\n")
        f.write("if 'features' not in sys.path:\n")
        f.write("    sys.path.append('features')\n")
        f.write("\n")
        f.write("import lettuce\n")
        f.write("\n")

        for mod in used_modules:
            mod = mod.replace('.py', '')
            f.write("import %s\n" % mod)
        f.write("\n\n")

        #f.write("FEATURE = '%s'\n" % feature)
        #f.write("\n\n")

        for scen in scenarios_list:

            f.write("@lettuce.mark.py_test\n")
            for tag in scen['tags']:
                f.write("@lettuce.mark.%s\n" % tag)

            name = scen['name']
            name = name.replace('.', '_')
            name = name.replace('-', '_')
            name = 'test_' + name
            f.write("def %s(step):\n" % name)
            f.write('    """new-%s"""\n' % scen['name'])

            for step, line in scen['commands']:
                if step == 'comment':
                    f.write('    # %s\n' % line)
                    continue

                if step == 'empty-line':
                    f.write('\n')
                    continue

                #f.write('    # %s\n' % line)  # original line in comment
                mod = step[0].replace('.py', '')
                func = step[1]
                args = step[2]
                args = ['None' if a is None else "'%s'" % a.replace("'", "\\'") for a in args]
                args2 = ", ".join(args)
                if args2:
                    args2 = ', ' + args2

                new_line = '    %s.%s(step%s)\n' % (mod, func, args2)
                if len(new_line) < 100:
                    f.write(new_line)
                    continue

                new_line = '    %s.%s(step,\n' % (mod, func)
                f.write(new_line)

                spaces_num = len(new_line) - 6
                args_txt = ""
                for arg in args:
                    args_txt += " " * spaces_num
                    args_txt += "%s,\n" % arg
                args_txt = args_txt[:-2] + ')\n'
                f.write(args_txt)

            f.write("\n\n")


def main(feature_file_path):
    print("Converting file %s." % feature_file_path)

    steps = load_steps()
    print("Loaded %s step definitions." % len(steps))
    #for s in steps:
    #    print(s)

    feature, scenarios_list, used_modules = parse_feature_file(feature_file_path, steps)

    if feature_file_path.endswith('/logging.feature'):
        feature_file_path = feature_file_path.replace('/logging.feature', '/kea_logging.feature')

    py_file_path = feature_file_path.replace('.feature', '').replace('.', '_') + '.py'

    generate_py_file(feature, scenarios_list, used_modules, py_file_path)

    print('Feature: %s' % feature)
    for idx, scen in enumerate(scenarios_list):
        print('%s. Scenario: %s' % (idx, scen['name']))
        print('  Tags: %s' % scen['tags'])
        print('  Commands:')
        for cmd in scen['commands']:
            print('      %s' % str(cmd))
        print('')



if __name__ == '__main__':
    main(sys.argv[1])
