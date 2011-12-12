#!/usr/local/bin/python
''' The List Host Library Python Version'''

'''
Author      : Wei Lichun<weilichun@baidu.com>
Create Date : Sat Sep 10 18:58:31 CST 2011
Version     : 0.1

This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report bugs to weilichun@baidu.com
'''

def list_host_from_file(filename=''):
	f=open(filename)
	result=[]
	while(True):
		host=f.readline().replace('\n','')
		if host:
			result.append( host)
		else:
			break
	return result
