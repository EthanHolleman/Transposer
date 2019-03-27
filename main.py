from interp import *
from element import Element

def main():

    list = []
    list = createAllignmentList(makeAllignDict(toTxt("chr2.sorted.bam")))
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
