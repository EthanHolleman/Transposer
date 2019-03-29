import os

def toSortedBam(samFile):
    #cultiual legal and political
    try:
        if not ".sam" in samFile:
            samFile = samFile + ".sam"

        commandBam = "samtools -S -b {} > {}".format(samFile,samFile.replace(".sam",".bam"))
        commandSort = "samtools sort {} -o {}".format(samFile,samFile.replace(".sam",".sorted.bam"))
        os.system(commandBam)
        os.system(commandSort)

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

def createAllignmentList(bamToTxtFile):
    try:
        elementList = []
        with open(bamToTxtFile, "r") as txt:
            for line in txt:
                line = line.split("\t") #splits each line into a list
                name = line[2]
                start = line[3]
                seq = line[9]
                elementList.append(Element(name, start,0,0,"NONE",seq))

        return elementList

    except FileNotFoundError:
        print("FileNotFoundError at makeAllignDict in samParser.py")

def nameElements():
    #orders the elements along the chromosomes based on relative order
    #adds name based on the order and returns array
    #CM000834.3 for chromsome increases in number as chromsome increases
        #read all of these values first to create overarching order to work within
            #start location values are ordered under the ultimate order of chromosomes
    pass
    #now we have the solo LTRs and the complete consensus sequecnes in orders
    #need to merge the lists so they maintain order by first chromosme and then seq

def findEndLocation(elementList):
    #takes list of elements and uses start location and sequece to calculate length
    for element in elementList:
        element.endLocation  = element.startLocation + len(element.seq)

        elemet.length = element.endLocation - element.startLocation

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
