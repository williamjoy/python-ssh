#!/usr/local/bin/python
''' The List Host Library Python Version'''

'''
Author      : Wei Lichun<lichun.william@gmail.com>
Create Date : Sat Sep 10 18:58:31 CST 2011
Version     : 0.2

This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report bugs to lichun.william@gmail.com
'''
import subprocess
import expand_range

def get_hosts_from_file(filename=''):
  """This function parses the contents of a stream to generate a list of lines.
  This function removes comments delimited by '#', ingores empty
  lines, and leading and trailing whitespace.
  Returns:
     a list of hosts
  """
    f=open(filename)
    result=[]
    while(True):
        line=f.readline().replace('\n','')
        if line:
            idx = line.find('#')
            if idx >= 0:
                line = line[:idx]
            if line:
                result.append( line.strip())
        else:
            break
    return result
    
def get_hosts_from_range(range=''):
    if(range):
        return expand_range.expand(range)
    else:
        return []
