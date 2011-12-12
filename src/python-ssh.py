#!/usr/bin/env python
#-*- coding = utf-8 -*-
''' the Parallel batch command running environment'''
'''
    Parallel LHCK utility
        
    Author      : Wei Lichun<weilichun@baidu.com>
    Create Date : Thu Sep  8 21:58:04 CST 2011
    Version     : 0.9
	Recent Changes:
		support max parallel thread argument
		support login_name argument
		support regex pattern filter, invert match
'''

'''
Usage: plhck (-f filename|-q string) command

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        the host file which stores the host list
  -q QSTRING, --qstring=QSTRING
                        the qstring to list host

Report any bugs to weilichun@baidu.com


This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report any bugs to weilichun@baidu.com
'''
import subprocess
import optparse
import sys
import getpass
import copy
import re
import signal

import process_thread
import get_host_list


parser=optparse.OptionParser(usage="%prog [ -p <max parallel thread number> ] (-f filename|-q string) [ -l login_name ] command",version='%prog 1.2',epilog="Report any bugs to weilichun@baidu.com", prog='plhck')
parser.add_option("-p","--parallel"   ,action="store",type="int",dest="parallel",default=10,help="max number of parallel threads ,default is 10")
parser.add_option("-f","--file"   ,action="store",type="string",dest="filename",help="the host file which stores the host list")
parser.add_option("-q","--qstring",action="store",type="string",dest="qstring",help="the qstring to list host")
parser.add_option("-l","--login_name",action="store",type="string",dest="login_name",help="Specifies the user to log in as on the remote machine.  This also may be specified on a per-host basis in the configuration file")
parser.add_option("-e","--regexp",metavar="PATTERN",action="store",type="string",dest="pattern",help="Use PATTERN as the pattern; useful to protect patterns beginning with -.")
parser.add_option("-v","--invert-match",action="store_false",dest="invert",default=True,help="Invert the sense of matching, to select non-matching lines.")


(options,command)=parser.parse_args()

qstring=options.qstring
filename=options.filename
login_name=options.login_name
pattern=options.pattern
parallel=options.parallel
sshpass_cmd='sshpass'

if (not qstring and not filename):
    print ('Error:QString argument or filename is required')
    parser.print_help()
    sys.exit(-2)

if (not command):
    print ('Error:command argument is required')
    parser.print_help()
    sys.exit(-2)

if(qstring):
    hostnames=list_host.list_host(qstring)
elif(filename):
	hostnames=list_host.list_host_from_file(filename)

if(login_name):
	password=getpass.getpass()	

def signal_handler(signal, frame):
        print 'Ctrl+C Caught, Exiting..'
        sys.exit(0)

if __name__ == '__main__':
    tasks=[]
    if(not hostnames):
        print ('No Host found from lh util')
        sys.exit(-3)
    command.insert(0,'ssh')
    if(login_name):
        command.insert(1,login_name)
        command.insert(1,'-l')
        command.insert(0,password)
        command.insert(0,'-p')
        command.insert(0,sshpass_cmd)
        host_insert_index=4
    else:
        host_insert_index=1
    task_group=process_thread.TaskGroup(parallel)
    for host in hostnames:
        #print command
        ssh_command=copy.copy(command)
        ssh_command.insert(host_insert_index,host)
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
                print "\033[0;36;40m",index,"of",size,"\033[0;32;40m: =============== \033[0;33;40m",task.key," \033[0;32;40m===============\033[0m"
                if(task.stdout):
                        print task.stdout,
