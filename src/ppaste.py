#!/usr/bin/env python
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
import socket

import process_thread
import get_host_list

parser=optparse.OptionParser(usage='%prog --template filename1 filename2',
    version='%prog 1.2',
    epilog="Report any bugs to lichun.william@gmail.com", prog='plhck')
parser.add_option("-t","--template"   ,action="store",type="string",
    dest="template",help="the template")
parser.add_option("-i","--hostname-to-ip",action="store_true",
    default=False,dest="to_ip",help="change host  name to ip address")

def host_to_ip(hostname=""):
    return socket.gethostbyaddr(hostname)[2][0]

(options,filenames)=parser.parse_args()

if (not options.template):
    print ('no template specified')
    parser.print_help()
    sys.exit(-2)

if (not filenames):
    print ('no filename specified')
    parser.print_help()
    sys.exit(-2)



if __name__ == '__main__':
    array1=get_host_list.list_host_from_file(filenames[0])
    array2=get_host_list.list_host_from_file(filenames[1])
    for line in zip( array1,array2):
        if(options.to_ip):
            print options.template % (host_to_ip(line[0]),host_to_ip(line[1]))
        else:
            print options.template % (line[0],line[1])
