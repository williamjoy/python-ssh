#!/usr/bin/env python
#-*- coding = utf-8 -*-
''' the Parallel batch command running environment'''
'''
    Parallel ssh utility
        
    Author      : Wei Lichun<lichun.william@gmail.com>
    Create Date : Thu Sep  8 21:58:04 CST 2011
    Version     : 1.3
    Recent Changes:
        support max parallel thread argument
        support login_name argument
        support regex pattern filter, invert match
'''

'''


This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

'''
import subprocess
import optparse
import sys
import copy
import re
import signal
import getpass
import random

import process_thread
import query_hosts


parser=optparse.OptionParser(
    usage="%prog [ -P <max parallel thread number> ] (-f filename | -r range) \
    [ -l login_name ] command",version='%prog 1.3',
    epilog="Report any bugs to lichun.william@gmail.com", prog='python-ssh')
parser.add_option("-V","--verbose",action="store_true",default=False,
    dest="verbose_mode", help="print more logs")
parser.add_option("-d","--dry-run",action="store_true",default=False,
    dest="dry_run", help="only print command, without really running it")
parser.add_option("-p","--password",action="store_true",default=False,
    dest="use_password", help="use ssh password?")
parser.add_option("-P","--parallel",action="store",type="int",
    dest="parallel",default=10,
    help="max number of parallel threads ,default is 10")
parser.add_option("-r","--range"   ,action="store",type="string",
    dest="range",help="Range of nodes to operate on")
parser.add_option("-s","--shuffle"   ,action="store_true",default=False,
    dest="shuffle",help="Shuffle the server list?")
parser.add_option("-f","--file"   ,action="store",type="string",
    dest="filename",help="the host file which stores the host list")
parser.add_option("-l","--login_name",action="store",type="string",
    dest="login_name", default="root",
    help="Specifies the user to log in as on the remote machine.\
    This also may be specified on a per-host basis in the configuration file")
parser.add_option("-X","--extra-arg",action="store",type="string",
    dest="extra_argument",
    help="Extra command-line argument. for example: -o ConnectTimeOut=10")
parser.add_option("-e","--regexp",metavar="PATTERN",action="store",
    type="string",dest="pattern", help="Use PATTERN as the pattern;\
    useful to protect patterns beginning with -.")
parser.add_option("-v","--invert-match",
    action="store_false",dest="invert",default=True,
    help="Invert the sense of matching, to select non-matching lines.")


(options,command)=parser.parse_args()

filename=options.filename
login_name=options.login_name
pattern=options.pattern
parallel=options.parallel
extra_argument=options.extra_argument

if (not command):
    parser.error ('command argument is required')
if (options.filename):
    hostnames=query_hosts.get_hosts_from_file(options.filename)
elif(options.range):
    hostnames=query_hosts.get_hosts_from_range(options.range)
else:
    parser.error ('one filename or range is required')

if (options.use_password):
    password=getpass.getpass(prompt="%s@$REMOTE's password:" % login_name)

def signal_handler(signal, frame):
        print 'Ctrl+C Caught, Exiting..'
        sys.exit(1)

def insert(l, arg):
    if (isinstance(arg, str)):
        items=arg.split()
    elif (isinstance(arg,list)):
        items=arg
    items.reverse()
    for e in items:
        l.insert(0,e)
    return l

def append(l, arg):
    if (isinstance(arg, str)):
        items=arg.split()
    elif (isinstance(arg,list)):
        items=arg
    for e in items:
            l.append(e)
    return l
        

if __name__ == '__main__':
    tasks=[]
    if(not hostnames):
        print ('No Hosts Returned')
        sys.exit(-3)
    prefix = []
    suffix = []
    if (extra_argument):
        insert(prefix,extra_argument)
    insert(prefix,"-o StrictHostKeyChecking=no")

    if(login_name):
        insert(prefix,'-l %s' % login_name)
    if(options.use_password):
        insert(prefix,'sshpass -p %s' % password)
    insert(prefix,'ssh')
    if(options.dry_run==True):
        insert(prefix,'echo')
    task_group=process_thread.TaskGroup(parallel)
    if(options.shuffle):
        random.shuffle(hostnames)
    for host in hostnames:
        ssh_command=copy.copy(prefix)
        append(ssh_command,host)
        append(ssh_command,command)
        task_group.add_task(host,ssh_command)

    signal.signal(signal.SIGINT, signal_handler)
    task_group.start()
    size=len(hostnames)
    index=0
    if(pattern):
        compiled_pattern=re.compile(pattern)
    while(index<size):
        index=index+1
        task=task_group.done_queue.get()
        if(pattern):
            if(compiled_pattern.search(task.stdout)):
                matched=True
            else:
                matched=False
            if(not(matched ^ options.invert)):
                print task.key 
        else:
            # 1 of 1 : ===============  william-laptop  ===============
            if (options.verbose_mode):
                print task.cmd
            print "\033[0;31;40m",index,"of",size,"\033[0;35;40m: =============== \033[0;36;40m",task.key," \033[0;35;40m===============\033[0m"
            if(task.stdout):
                print task.stdout,
