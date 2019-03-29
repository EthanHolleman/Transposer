import sys, argparse
from interp import *
from argsRemap import *
from element import Element


def main():
    args = argsRemap()

    '''
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
