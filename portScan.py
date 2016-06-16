#!/usr/bin/python
#-*-coding:utf-8-*-
# 端口扫描

import optparse
import sys
from socket import *
reload(sys)
sys.setdefaultencoding('utf8')

def connScan(targetHost,targetPort):
    try:
        connSkt = socket(AF_INET,SOCK_STREAM)
        connSkt.connect((targetHost,targetPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        print '[+]%d/tcp open' % targetPort
        print '[+] '+str(results).encode('utf-8').decode('utf-8')
        connSkt.close()
    except:
        print '[-]%d/tcp closed' % targetPort
        
def portScan(targetHost,targetPorts):
    try:
        targetIp = gethostbyname(targetHost)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % targetHost
        return
    
    try:
        targetName = gethostbyaddr(targetIp)
        print '\n[+] Scan Results for: '+targetName[0]
    except:
        print '\n[+] Scan Results for: '+targetIp[0]
    setdefaulttimeout(1)

    for targetPort in targetPorts:
        print 'Scanning port '+ targetPort
        connScan(targetHost,int(targetPort)) 

def main():
    parse = optparse.OptionParser('Usage %prog -H'+'<target host> -p <targe port>')
    parse.add_option('-H',dest='tagHost',type='string',help='specify target host')
    parse.add_option('-p',dest='tagPort',type='string',help='specify target port[s] separated by comma')
    (options,args) = parse.parse_args()

    targetHost = options.tagHost
    targetPorts = str(options.tagPort).split(',')

    if (targetHost == None) | (targetHost == None):
        print '[-] You Must specify a target host and port[s].'
        exit(0)
    
    portScan(targetHost,targetPorts)
if __name__ == '__main__':
    main()