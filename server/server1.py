#!/usr/bin/python
'''
server               client
  |  <-- connect  ---  |
  |                    |
  |  ---  version -->  |
  |                    |
  |  <--  config  ---  |
  |                    |
  |  --- confirm  -->  |
  |                  tests
  |  <-- turn off ---  |

'''
HOST = ''    
PORT = 9999
import socket,subprocess,sys,optparse,shlex

def option_parser():
    
    desc="Sending version number of DHCP server. PORT number need to be the same in client and server. Keep this working in testing time."
    parser = optparse.OptionParser(description=desc)
    parser.add_option('-p', '--port', help='on witch port listening for question, default 9999', dest='port', type='int', default=9999, action='store')
    (opts, args) = parser.parse_args()

    return opts.port

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
            connection, addr = s.accept()
            print 'Got connection from', addr
            command="dhcpd --version"
            check_version=subprocess.Popen(shlex.split(command),stderr=subprocess.PIPE)
            version= str(check_version.communicate()[1])[:-1]
            connection.send(version)

            DHCP_config=connection.recv(4096)
            config_file=open('config','w')
            config_file.write(DHCP_config)
            
            if DHCP_config: 
                command="dhcpd -6 -f -cf config eth0"
                run_server=subprocess.Popen(shlex.split(command),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                connection.send("DHCP_server_running")
                code=connection.recv(1024)

                if code=='KILL':
                    run_server.kill()
                    print 'server terminated'

            connection.close()
            config_file.close()
            
    except KeyboardInterrupt:
        print 'Program Interrupted by user'
        s.close()
        sys.exit()

if __name__ == "__main__":
    detect_version(option_parser())
