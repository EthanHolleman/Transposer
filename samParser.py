import os
from search import *

def makeAllignDict(bamToTxtFile):
    #creates a dictionart with the ket as location and sequence as entry
    dict = {}
    try:
        with open(bamToTxtFile, "r") as txt:
            for line in txt:
                line = line.split("\t") #splits each line into a list
                dict[line[3]] = line[9] #locations of location and sequece alligned
    except FileNotFoundError:
        print("FileNotFoundError at makeAllignDict in samParser.py")

    return dict

def toSortedBam(samFile):
    #cultiual legal and political
    try:
        if not ".sam" in samFile:
            samFile = samFile + ".sam"

        commandBam = "samtools -S -b {} > {}".format(samFile,samFile.replace(".sam",".bam"))
        commandSort = "samtools sort {} -o {}".format(samFile,samFile.replace(".sam",".sorted.bam"))
        os.system(commandBam)
        os.system(commandSort) #need to finish this command
    except FileNotFoundError:
        print("FileNotFoundError at toSortedBam in search.py")

def toTxt(samFile):
    outputFile = samFile + ".txt"
    try:
        command = "samtools view {} > {}".format(samFile,outputFile)
        os.system(command)
    except FileNotFoundError:
        print("FileNotFoundError at toTxt in search.py")


#read sam file and extract alligned sequences and location of that sequence to discitonart
