from samParser import *
from reallign import Element
def main():
    dict = {}
    dict = makeAllignDict("chr2.sorted.bam.txt")


    print(Element.createAllignmentList(dict))


if __name__ == '__main__':
    main()
