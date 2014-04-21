#!/usr/bin/env python
#-*- coding = utf-8 -*-
''' the Parallel batch command running environment'''
'''
    A tool for expend host range expressions
        
    Author      : Wei Lichun<lichun.william@gmail.com>
    Create Date : Thu Apr  3 14:32:30 CST 2014
    Version     : 1.0
'''

'''


This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

'''
import optparse
import random

import expand_range


parser=optparse.OptionParser(
    usage="%prog expr1 [expr2 ...]",version='%prog 1.3',
    epilog="Report any bugs to lichun.william@gmail.com", prog='er')
parser.add_option("-s","--sort",action="store_true",default=False,
    dest="sort", help="sort the out put?")
parser.add_option("-f","--shuffle",action="store_true",default=False,
    dest="shuffle", help="shuffle list?")
parser.add_option("-d","--delimiter",action="store",type="string",default=' ',
    dest="delimiter", help="delimiter of the output, default is space")

if __name__ == '__main__':
    (options,expr)=parser.parse_args()

    if(not expr):
        raise Exception("need at least one expression, example stnd0001-23")

    results=expand_range.expand(",".join(expr))
    if(options.shuffle):
        random.shuffle(results)
    delimiter=options.delimiter.replace('\\t','\t')
    delimiter=delimiter.replace('\\n','\n')

    print delimiter.join(results)

