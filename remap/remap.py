import sys, argparse
from interp import *
from args import *
from element import Element


def main():
    args()

    #index = sys.argv[1]
    #LTRcon = sys.argv[2]
    #seqCon = sys.argv[3]
    #allowance = sys.argv[4]
    #output = sys.argv[5]
 #issue with same file name
    list = []

    list = createAllignmentList(toTxt("chr2.sorted.bam"))
    findEndLocation(list)
    con = 4460
    newList = findSolos(list,con,10000)

    for element in list:
        print(element.startLocation)
    print("break")
    for element in newList:
        print(element.startLocation)


if __name__ == '__main__':
    main()
