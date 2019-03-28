#takes the LTR consensus and the complete and bowties them
import os
from samParser import *

def search (con, index, outputFile):
    #general search for a local allignments
    try:
        commandSearch = "bowtie2 -x {} -r {} -a -non--deterministic -S {}".format(index,con,outputFile)
        samCommand = "Samtools view -S -b {} "
        os.system(command)
        return toSortedBam(outputFile)
        #will run the command and return a samfile
    except FileNotFoundError:
        print("FileNotFoundError at search in search.py")



#runs the search converts to bam files
#comarison methods for searching
