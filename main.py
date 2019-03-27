from interp import *
from element import Element

def main():

    list = []
    list = createAllignmentList(makeAllignDict(toTxt("chr2.sorted.bam")))
    print(list)
    print(len(list))


if __name__ == '__main__':
    main()
