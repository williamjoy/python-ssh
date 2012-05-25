#!/usr/local/bin/python
''' The List Host Library Python Version'''

'''
Author      : Wei Lichun<lichun.william@gmail.com>
Create Date : Sat Sep 10 18:58:31 CST 2011
Version     : 0.1

This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report bugs to lichun.william@gmail.com
'''
import subprocess

def get_hosts_from_file(filename=''):
    f=open(filename)
    result=[]
    while(True):
        host=f.readline().replace('\n','')
        if host:
            result.append( host.strip())
        else:
            break
    return result

def get_hosts_from_range(range=''):
    if(range):
        p=subprocess.Popen(['er','-e',range],stdout=subprocess.PIPE,stdin=None,shell=False)    
        arr=p.communicate()[0].split('\n')
        if (arr[-1]):
            return arr
        else:
            return arr[:-1] 
    else:
        return []

#oh, really? can't you reuse any code?
def get_hosts_from_igor(range=''):
    if(range):
        p=subprocess.Popen(['yinst','range','-ir',range],stdout=subprocess.PIPE,stdin=None,shell=False)    
        arr=p.communicate()[0].split('\n')
        if (arr[-1]):
            return arr
        else:
            return arr[:-1] 
    else:
        return []

if (__name__ == '__main__'):
	print get_hosts_from_range("@WATCHER")
	print get_hosts_from_igor("@ug.set.ac2-prod.ssol2_server")
