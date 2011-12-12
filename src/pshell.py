#!/bin/env python
#-*- coding = utf-8 -*-

'''
Report any bugs to lichun.william@gmail.com


This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report any bugs to lichun.william@gmail.com
'''
import subprocess
import optparse
import sys
import copy
import shlex

import process_thread
import list_host

parser=optparse.OptionParser(usage="%prog -f filename",version='%prog 1.2',epilog="Report any bugs to lichun.william@gmail.com", prog='pshell')
parser.add_option("-f","--file"   ,action="store",type="string",dest="filename",help="the host file which stores the host list")


(options,command)=parser.parse_args()

filename=options.filename

if(filename):
	lines=list_host.list_host_from_file(filename)
else:
	print ('No Host found from lh util')
	sys.exit(-3)
	

if __name__ == '__main__':
    tasks=[]
    task_group=process_thread.TaskGroup(128)
    print lines
    for line in lines:
        task_group.add_task(line,shlex.split(line))

    task_group.start()
    size=len(lines)
    print size
    index=0
    while(index<size):
        index=index+1
        task=task_group.done_queue.get()
        print "\033[0;36;40m",index,"of",size,"\033[0;32;40m: =============== \033[0;33;40m",task.key," \033[0;32;40m===============\033[0m"
        print task.stdout,