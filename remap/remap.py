import sys, argparse
from interp import *
from argsRemap import *
from element import Element
from tier import *


def main():

    args = argsRemap()


    sortedTxtLTR = toTxt(search(args.LTRcon, args.index, "TestRunLTR.sam" ))
    sortedTxtCon = toTxt(search(args.seqCon, args.index, "TestRunCon.sam" ))


    chrDict = translateName(args.chrKeys)

    ElementListLTR = createAllignmentList(sortedTxtLTR, chrDict)
    ElementListCon = createAllignmentList(sortedTxtCon, chrDict)

    print(len(ElementListLTR))
    print(len(ElementListCon))
    print("consecond")



    soloList = findSolos(ElementListLTR, args.seqCon, args.allowance)
    print(len(soloList))

    mergedList = mergeLists(soloList, ElementListCon)

    finalList = nameElements(mergedList, "GMR30")
    for element in finalList:
        print(element.name + " " + str(element.startLocation)+ " " + element.status)
if __name__ == "__main__":
    main()
