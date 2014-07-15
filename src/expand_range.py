#!/usr/local/bin/python
''' The List Host Library Python Version'''

'''
Author      : William Wei<lichun.william@gmail.com>
Create Date : Thu Apr  3 10:59:29 CST 2014
Version     : 0.1

This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report bugs to lichun.william@gmail.com
'''

''' Example: stnd0001-10,,couria.ash,stnab-ds01-04'''

import re
import sys

NUMBER_RANGE_RE_PATTERN=re.compile("^([_a-z.-]*([0-9_a-z.-]*[_a-z.-]+)?)?([0-9]+)-([0-9]+)((\.[a-z0-9_-]+)*.?)$",re.IGNORECASE)
DELIMETER_RE_PATTERN   =re.compile("[ ,\t]+")
def expand(r):
    ret = set()
    for x in DELIMETER_RE_PATTERN.sub(",",r).split(","):
        if(len(x) == 0):
            continue
        if(is_number_range(x)):
            for y in expand_number_range(x):
                ret.add(y)
        else:
            ret.add(x)
    return list(ret)
        
def is_number_range(r):
    return NUMBER_RANGE_RE_PATTERN.match(r)!= None

'''Example:
input stnd23001-020
output is a list, containing the following items:
    stnd23{001..020}, with leading 0 paddings
'''
def expand_number_range(r):
    m = NUMBER_RANGE_RE_PATTERN.match(r)
    pre =  m.group(1)
    prefix =  m.group(3)
    end =  m.group(4)
    suffix =  m.group(5)
    number_len = len(end)
    if (number_len > len(prefix)):
        raise Exception("Range out of boundary: %s" % r)
    start = prefix[-number_len:]
    prefix = prefix[0:-number_len]
    start=int(start)
    end=int(end)

    if (start >= end):
        raise Exception("Range out of boundary: %s" % r)

    return [ "%s%s%0*d%s" % (pre,prefix,number_len,i,suffix) for i in range(start,end+1)]

if __name__ == '__main__':
    print expand('stnd09-10.com')
    print expand('stnd3001-020.stnd.demonware.net')
    print expand(',,9,stnd03001-3010.stnd.demonware.net,,x,y,x-z,  ,7')
    print expand(',,,ash.demonware.net,ash,demonware,ware,ash,stnd,stnd,ash,ash001-7.ash.demonware.net.')
    print expand(',,,')
    print expand('')
    print expand('--')
    print expand('__009-10')
    print expand('stnab-lsg001-3,stnab-ds001-4')
    print expand('ashdev10001-lsg001-3,stnab-ds001-4')

