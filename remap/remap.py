import sys, argparse
from interp import *
from argsRemap import *
from element import Element


def main():

    conList = []
    LTRList = []
    soloList = []
    remapedList = []
    outputTempCon = "searchOutCon.sam"
    outputTempLTR = "searcOutLTR.sam"
    #variable declarations

    args = argsRemap()
    sortedBamCon = search(args.seqCon,args.index,outputTempCon) # need to make output file variable in argsCon can make this defualt arg
    sortedTxtCon = toTxt(sortedBamCon)
    #outputfile names are going to be made in program no input from user

    sortedBamLTR = search(args.LTRcon, args.index, outputTempCon) #need to add something to output here to differntiate
    sortedTxtLTR = toTxt(sortedBamLTR)

    ##CHECK 1
    #At this point Bowtie results should be in txt format

    conList = createAllignmentList(sortedTxtCon, translateName(assenstionNums))
    LTRList = createAllignmentList(sortedTxtLTR, translateName(assenstionNums)) #need this variable in params args

    ##Check 2
    #LTR and complete consensus lists should be renamed with chr number, and have all other infor (seq, length, start, end) except LTR status

    soloList = findSolos[LTRList]

    ##CHECK 3
    #soloList should contain only Solo LTR elements

    remapedList = nameElements(mergeLists(soloList, conList),args.name) #need family name variable

    ##CHECK 4
    #remapedList should have the finished product to be outputted to a fasta
        #need to write rename function and within it make sure to change name to chromosome 1 instead of 1

    
    '''
    need to look for a range in the LTRS less than the reach of the consensus sequence


    Basic structure of a run
        con LTR and index files location are read in through the argsRemap
        search done on both con and LTR to produce sam files
        sam files through 2 methods converted to sorted txt files
            allows for easy reading and parsing information
        allignments in list are converted to Element objects and added to new
        various methods add additional information such as seq length
        LTR search file is sent to findSolos method and returns a list of
        only the solo LTRs
        nameElements methods will take both the consensus search files and the solos
        from the finds solos method and merge them
            merge first based on chromosome number then by order in chromosome
            elements are named based on their chromsome number and order in the
            chromosoem
        convert elements list to a fasta file and return to the user

    '''

    '''
    list = createAllignmentList(toTxt("chr2.sorted.bam"))
    print(list)
    findEndLocation(list)
    con = 4460
    newList = findSolos(list,con,10000)
    '''

if __name__ == '__main__':
    main()
