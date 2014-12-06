#!/usr/bin/env python
#-*- coding = utf-8 -*-
''' the Parallel batch command running environment'''
'''
    A tool for expend host range expressions
        
    Author      : Wei Lichun<lichun.william@gmail.com>
    Create Date : Thu Apr  3 14:32:30 CST 2014
    Version     : 1.3
'''

'''


This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

'''
import sys
import argparse
import random

import expand_range

parser =argparse.ArgumentParser(
    description = "Expand host ranges with given expressions",
    usage ="%(prog)s expr1 [expr2 ...]", version='%(prog)s 1.3',
    epilog="Report any bugs to lichun.william@gmail.com", prog='er')
parser.add_argument("-s", "--sort", action="store_true", default=False,
    dest="sort", help="sort the out put?")
parser.add_argument("-f", "--shuffle", action="store_true", default=False,
    dest="shuffle", help="shuffle list?")
parser.add_argument("-c", "--compress", action="store_true", default=False,
    dest="compress", help="Compress host list ?")
parser.add_argument("-d", "--delimiter", action="store", default=' ',
    dest="delimiter", help="delimiter of the output, default is space")
parser.add_argument("-n", "--newline", action="store_const", dest="delimiter",
    const='\n', help="same as --delimiter='\\n'")
parser.add_argument("expr", action="store", nargs='+',
    help="expressions to be expanded")

if __name__ == '__main__':
    options =parser.parse_args()
    expr = options.expr
    results =expand_range.expand(",".join(expr))
    delimiter = options.delimiter.replace('\\t', '\t')
    delimiter = delimiter.replace('\\n', '\n')
    if(options.compress):
        results=expand_range.compress(results)
    if(options.sort):
        results.sort()
    elif(options.shuffle):
        random.shuffle(results)
    print delimiter.join(results)

