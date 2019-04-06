#WARNING
    #Edit this file at your own risk
    #To change Bowtie search paramters edit only the commandSearch variable
    #See Bowtie2 manual for more information
import os
from interp import toSortedBam

def search (con, index, outputFile):
    #general search method for a local allignments

    try:
        #print("Samtools view -S -b {} ".format(outputFile))
        commandSearch = "bowtie2 -x {} -r {} -a --non-deterministic -S {}".format(index,con,outputFile)
        #samCommand = "Samtools view -S -b {} ".format(outputFile)
        #print("Samtools view -S -b {} ".format(outputFile))
        os.system(commandSearch)
        #os.system(samCommand)
        outputFile = toSortedBam(outputFile)

        return outputFile
        #will run the command and return a samfile
    except FileNotFoundError:
        print("FileNotFoundError at search in search.py")

def makeIndex(name,):
    pass



#runs the search converts to bam files
#comarison methods for searching
