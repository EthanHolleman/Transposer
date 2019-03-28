import sys, argparse
from interp import *
from argsRemap import *
from element import Element


def main():
    args = argsRemap()

    '''
    list = createAllignmentList(toTxt("chr2.sorted.bam"))
    print(list)
    findEndLocation(list)
    con = 4460
    newList = findSolos(list,con,10000)
    '''

if __name__ == '__main__':
    main()
