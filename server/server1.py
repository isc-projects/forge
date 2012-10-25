#!/usr/bin/python

HOST = ''    

import socket,subprocess,sys,optparse

def option_parser():
    desc="""Sending version number of DHCP server. PORT number need to be the same in client and server. Keep this working in testing time.
    """
    parser = optparse.OptionParser(description=desc)
    parser.add_option('-p', '--port', help='on witch port listetnig for question, default 9999', dest='port', type='int', default=9999, action='store')
    (opts, args) = parser.parse_args()

    detect_version(opts.port)

def detect_version(port):
    s = socket.socket()

    try:
        s.bind((HOST, port))
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + '\n Message ' + msg[1]
        sys.exit()
    print 'Waiting on PORT no. '+ str(port) + ' ....' 
    try:
        s.listen(5)
        while True:
           c, addr = s.accept()
           print 'Got connection from', addr
           run=subprocess.Popen(['dhcpd', '--version'],stderr=subprocess.PIPE)
           version= str(run.communicate()[1])[:-1]
           c.send(version)
           c.close()
    except KeyboardInterrupt:
        print 'Program Interrupted by user'
        sys.exit()

if __name__ == "__main__":
    option_parser()
