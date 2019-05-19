import os, time, subprocess
from element import Element
from flanker import *

def toSortedBam(samFile, verbose):
    #takes a sam file and converts to sorted bam using samtools
    try:
        outputFile = samFile
        if not ".sam" in outputFile:
            outputFile = outputFile + ".sam"

        bam = samFile.replace(".sam",".bam")
        sortedBam = samFile.replace(".sam",".sorted.bam")

        commandBam = "samtools view -S -b {} > {}".format(samFile,bam) #commands to be executed
        commandSort = "samtools sort {} -o {}".format(bam,sortedBam)

        if verbose: print("Running command: " + commandBam)
        os.system(commandBam)
        if verbose: print("Running command: " + commandSort)
        os.system(commandSort)

        try: #removes redundant files but leaves the sorted bam for user
            os.system("rm {}".format(samFile))
            os.system("rm {}".format(bam))

        except FileNotFoundError:
            print("FileNotFoundError at toSortedBam when trying to remove files")

        return sortedBam # returns a sorted bam file name corresponding to one created in method

    except FileNotFoundError:
        print("FileNotFoundError at toSortedBam in search.py")

def toTxt(samFile, verbose):
    #takes a sam or bam file and converts to txt using samtools view
    outputFile = samFile + ".txt"

    try:
        command = "samtools view {} > {}".format(samFile,outputFile)
        if verbose: print("Running Command: " + command)
        os.system(command)
        return outputFile #returns txt file name corresponding to txt file created

    except FileNotFoundError:
        print("FileNotFoundError at toTxt in search.py")


def createAllignmentList(bamToTxtFile,dict,verbose,curBlastDB):
    #takes txt file from toTxt method and converts to list of Element objects
    try:
        elementList = []
        with open(bamToTxtFile, "r") as txt:

            for line in txt:
                line = line.split("\t") #splits each line into a list
                name = line[2]
                start = line[3]
                length = line[5] #gives cigar to the length as a temp holder

                elementList.append(Element(name,name,start,0,length,"NONE","ATGC"))


        for element in elementList:
            element.length = cigarParser(element.length)
            element.endLocation = element.startLocation + element.length -1#changed calculation of length using CIGAR
            element.status = "INTACT" #defualy status is INTACT
            element.seq = getElementSeq(curBlastDB, element)

            #to get the element sequence need a blast DB of the new assembly and assencion number

            try:
                element.name = dict[element.name] #uses provided dictionary to set name to chr number

            except KeyError:
                if verbose:
                    print("keyError at createAllignmentList")
                    print("key used was " + element.name)

        os.system("rm {}".format(bamToTxtFile)) # removes txt version as no longer used

        return elementList

    except FileNotFoundError:
        print("FileNotFoundError at makeAllignDict in samParser.py")


def translateName(assenstionNums):
    #reads NCBI accenstion number file to create dictionary to translate number to chrs later on
    try:
        chrs = {}
        with open(assenstionNums) as names:
            for line in names:
                line = line.replace("\n","")
                line = line.split("\t")
                number, CM = line
                chrs.update({CM : number})

        return chrs

    except FileNotFoundError:
        print("FileNotFoundError" + " at translateName")


def mergeLists(soloList, conList, familyName):

    merge = soloList + conList
    mergeDict = {}
    finalList = []

    for element in merge:
        if element.name not in mergeDict:
            mergeDict[element.name] = [element]
        else: mergeDict[element.name].append(element)

    for key in sorted(mergeDict.keys()):
        mergeDict[key] = sorted(mergeDict[key], key = lambda e: e.startLocation)
        for i,element in enumerate(mergeDict[key],1):
            element.name = str(familyName) + " " + str(key) + "-" + str(i)
        finalList += mergeDict[key]

    return finalList


def findSolos(LTRList,completeCon,allowance):
    #takes list of LTR elements and determines if each should be considered a solo element based on allowance

    soloList = []
    i = 0
    completeConLength = 0

    try:
        with open(completeCon) as con:
            completeConLength = len(con.readline())
    except FileNotFoundError:
        return "FileNotFoundError at findSolos opening completeCon file"

    while i < len(LTRList):

        reach = LTRList[i].endLocation + completeConLength
        diff = (LTRList[i+1].startLocation - reach)

        if(diff > -(completeConLength) and diff <= 0): #test for truncated element
            LTRList[i].status = "INTACT"
            LTRList[i+1].status = "INTACT"
            i+=1
            if i==len(LTRList)-1:
                break

        elif (abs(diff) > allowance):
            LTRList[i].status = "SOLO"
            soloList.append(LTRList[i])
            if i == len(LTRList)-2:
                soloList.append(LTRList[i+1])
                break
        else:
            LTRList[i].status = "INTACT"
            LTRList[i+1].status = "INTACT"
            i+=1
            if i == len(LTRList)-1:
                break
        i+=1

    return soloList

def cigarParser(cigar):
    #reads the cigar info from an allignment and translates into the length on the alligned refernce
    length = 0
    temp = ""
    for char in cigar:
        temp = temp + "" + char
        if char == "M" or char == "D":
            temp = temp[:-1]
            length += int(temp)
            temp = ""
        elif char == "I" or char == "H":
            temp = ""

    return length
