#!/usr/bin/python
#-*-coding:utf-8-*-
# 端口扫描
# 2016-6-20:增加多线程支持
# 2016-6-20:增加nmap包

import optparse
import sys
from socket import *
from threading import *
import nmap

screenLock = Semaphore(value=1)
def connScan(targetHost,targetPort):
    try:
        connSkt = socket(AF_INET,SOCK_STREAM)
        connSkt.connect((targetHost,targetPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print '[+]%d/tcp open' % targetPort
        print '[+] '+str(results)
    except:
        screenLock.acquire()
        print '[-]%d/tcp closed' % targetPort
    finally:
        screenLock.release()
        connSkt.close()


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
        t = Thread(target=connScan,args=(targetHost,int(targetPort)))
        t.start()

def nmapScan(targetHost,targetPort):
    nmScan = nmap.PortScanner()
    nmapScan.scan(targetHost,targetPort)
    state = nmScan[targetHost]['tcp'][int(targetPort)]['state']
    print("[*]"+targetHost+" tcp/"+targetPort+" "+state)

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
    for tgtPort in targetPorts:
        nmapScan(targetHost,tgtPort)
    # portScan(targetHost,targetPorts)
if __name__ == '__main__':
    main()