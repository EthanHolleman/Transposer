import os
from element import Element

def makeAllignDict(bamToTxtFile):
    #creates a dictionart with the ket as location and sequence as entry
    dict = {}
    try:
        with open(bamToTxtFile) as txt:
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
        return outputFile

    except FileNotFoundError:
        print("FileNotFoundError at toTxt in search.py")

def createAllignmentList(elementDict):
    elementList = []
    for key in elementDict:
        elementList.append(Element("UNNAMED", key,0,0,"NONE",elementDict[key]))

    return elementList


def nameElements():
    #orders the elements along the chromosomes based on relative order
    #adds name based on the order and returns array
    pass

def findEndLocation(elementList):
    #takes list of elements and uses start location and sequece to calculate length
    for element in elementArray:
        element.endLocation  = element.startLocation + len(element.seq)
        elemet.length = element.endLocation - element.startLocation

def matchLTRPairs(elementList, LTRList,completeCon,range):
        #searched to see if lone element
        #list should be ordered at this point
        #least to greatest going on
    for i in range(0,len(LTRList)):
        current = LTRList[i]
        next = LTRList[i+1]


            #want to say they are linked if LTR is within +- 100 base
            # of the length of complete LTR
