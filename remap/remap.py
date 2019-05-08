#!/usr/bin/python
import sys, argparse
from interp import *
from argsRemap import *
from element import Element
from tier import *
from flanker import *

def main():

    args = argsRemap()
    chrDict = translateName(args.chrKeys)

    sortedTxtLTR = toTxt(search(args.LTRcon, args.index, "TestRunLTR.sam", args.verbose ),args.verbose)
    sortedTxtCon = toTxt(search(args.seqCon, args.index, "TestRunCon.sam",args.verbose ),args.verbose)


    ElementListLTR = createAllignmentList(sortedTxtLTR, chrDict, args.verbose, args.currBlastDB)
    ElementListCon = createAllignmentList(sortedTxtCon, chrDict, args.verbose, args.curBlastDB)
    '''
    LTRFlanks = makeFlankList(ElementListLTR, "TestChr1", 20, chrDict)
    print(LTRFlanks)
    need to create the flanklists using the blast dbs
        do this using the create flank list for each of the database provided

        oldFlanks = makeFlankList() #using old blast db
        newFlanks = makeFlankList() #using new blast db

    '''
    soloList = findSolos(ElementListLTR, args.seqCon, args.allowance)

    finalList = mergeLists(soloList, ElementListCon, args.name)


    if args.outputFile == True:
        for element in finalList:
            print(element.toStringFasta())
    else:
        with open(args.outputFile, "w") as out:
            for element in finalList:
                out.write(element.toStringFasta)
#'''

if __name__ == "__main__":
    main()
