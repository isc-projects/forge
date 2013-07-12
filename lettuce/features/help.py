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

import os
import sys

class UserHelp ():
    def __init__(self):
        self.tags = ''
        self.all_tags = ''

    def check_tags(self, line):
        """
        Add only unique tags to list
        """
        global tags
        global all_tags
        tag_list = line.strip() 
        tag_list = tag_list.split('@')
        tag_list = [x.strip(' ') for x in tag_list]
        for tag in tag_list:
            if tag is not None:
                if tag in tags:
                    pass
                else:
                    tags += tag + ', '
        
    def test(self, number, more):
        global tags
        #make for each in number because it starts in two points: in run_test.py by using -l option, then it create list only for one IP version, 
        #and in help.py generating whole test list.
        print "Test tree schema:\nroot directory\n\ttest set (available by option -s in run_test.py)\n\t\ttest feature"
        if more: print "\t\t\ttest name (available by option -n in run_test.py)"
        for each_number in number: 
            tags = ''
            print "\nIPv" + each_number + " Tests:"
            print "features/tests_v" + each_number + "/"
            for path, dirs, files in os.walk("features/tests_v" + each_number + "/"):
                if len(path[18:]) > 1: print "\t" + path[18:] 
                for each_file in files:
                    print "\t\t", each_file[:-8]
                    names = open(path +'/'+ each_file, 'r')
                    for line in names:
                        if line[0] == '@':
                            self.check_tags(line)
                        elif "Scenario:" in line:
                            if more: print "\t\t\t" + line.strip()[10:]
                    names.close()
                    
            print "\nTest tags you can use: \n", tags[:-2], "\n"
        
if __name__ == '__main__':
    #orginal_stdout = sys.stdout
    help_file = file('UserHelp.txt', 'w')
    sys.stdout = help_file
    generate_help = UserHelp()
    generate_help.test(["4","6"], 1)
    help_file.flush()
    
    help_file.close()
    #sys.stdout = orginal_stdout