import os
from element import Element

def makeAllignDict(bamToTxtFile):
    #creates a dictionary with the ket as location and sequence as entry
    dict = {}
    try:
        with open(bamToTxtFile) as txt:
            for line in txt:
                line = line.split("\t") #splits each line into a list
                dict[line[3]] = line[9] #locations of location and sequece alligned
    except FileNotFoundError:
        print("FileNotFoundError at makeAllignDict in samParser.py")

    return dict

def createAllignmentList(elementDict):
    #creates list of Element objects, only adds info immediately known from allignment
    elementList = []
    for key in elementDict:
        elementList.append(Element("UNNAMED", int(key),0,0,"NONE",elementDict[key]))

    return elementList

def toSortedBam(samFile):
    #sends sam file to a sorted bam file
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
    #takes sam or bam file and sends to txt file
    #recommended to sort before this
    outputFile = samFile + ".txt"
    try:
        command = "samtools view {} > {}".format(samFile,outputFile)
        os.system(command)
        return outputFile

    except FileNotFoundError:
        print("FileNotFoundError at toTxt in search.py")

def nameElements():
    #orders the elements along the chromosomes based on relative order
    #adds name based on the order and returns array
    pass

def findEndLocation(elementList):
    #takes list of elements and uses start location and sequece to calculate length
    for element in elementList:
        element.endLocation  = int(element.startLocation) + len(element.seq)
        element.length = int(element.endLocation) - int(element.startLocation)

## TODO: verify working for all possible locations of solo elements
def findSolos(LTRList,completeCon,allowance):
    #create a new list that contains only the solo elements
        #takes first element and "reaches" with con seq to possible 2nd LTR

    soloList = []
    i = 0
    while i < len(LTRList)-1:
        print(i)
        reach = LTRList[i].endLocation + completeCon
        diff = abs(LTRList[i+1].startLocation - reach)

        if(diff > allowance):
            LTRList[i].status = "SOLO"
            soloList.append(LTRList[i])
        else:
            LTRList[i].status = "INTACT"
            LTRList[i+1].status = "INTACT"
            i+=1

        i+=1

    return soloList
