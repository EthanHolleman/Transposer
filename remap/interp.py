import os

def toSortedBam(samFile):
    #takes a sam file and covernts to sorted bam using samtools
    try:
        if not ".sam" in samFile:
            samFile = samFile + ".sam"

        commandBam = "samtools view -S -b {} > {}".format(samFile,samFile.replace(".sam",".bam"))
        commandSort = "samtools sort {} -o {}".format(samFile,samFile.replace(".sam",".sorted.bam"))
        os.system(commandBam)
        os.system(commandSort)

    except FileNotFoundError:
        print("FileNotFoundError at toSortedBam in search.py")

def toTxt(samFile):
    #takes a sam or bam file and converts to txt using samtools view
    outputFile = samFile + ".txt"
    try:
        command = "samtools view {} > {}".format(samFile,outputFile)
        os.system(command)
        return outputFile
    except FileNotFoundError:
        print("FileNotFoundError at toTxt in search.py")


def createAllignmentList(bamToTxtFile,dict):
    #takes txt file from toTxt method and converts to list of Element objects
    try:
        elementList = []
        with open(bamToTxtFile, "r") as txt:
            for line in txt:
                line = line.split("\t") #splits each line into a list
                name = line[2]
                start = line[3]
                seq = line[9]
                elementList.append(Element(name, start,0,0,"NONE",seq))

        for elemet in elementList:
            element.endLocation = element.startLocation + len(element.seq) #sets end endLocation
            elemet.length = element.endLocation - element.startLocation #sets length
            element.name = dict[element.name] #uses the assenfile to rename elements with just chr number

        return elementList

    except FileNotFoundError:
        print("FileNotFoundError at makeAllignDict in samParser.py")


def translateName(assenstionNums):
    #reads NCBI assenstion number file to create dictionary to translate number to chrs later on
    try:
        chrs = {}
        with open(assenstionNums) as names:
            for line in names:
                line = line.replace("\n","")
                line = line.split("\t")
                chrs.update({line[1] : line[0]})
        return chrs

    except FileNotFoundError:
        print("FileNotFoundError" + " at translateName")


def mergeLists(soloList, conList):
    ## WARNING: Still requires testing
    #takes the LTR list and complete element list and merges in order
        #order based on chr number first then start location with lowest first
    mergedList = []
    done = "DONE"

    itrSolo = itr(soloList,done)
    itrCon = itr(conList,done)


    while itrSolo.next() != done:
        soloDelta = itr.next()
        conDelta = itr.next()

        if soloDelta.name < conDelta.name: #testing for chr number
            mergedList.append(soloDelta)
            soloDelta.next()
        elif soloDelta.name > conDelta.name:
            mergedList.append(soloDelta)
            conDelta.next()
        else:
            if soloDelta.startLocation < conDelta.startLocation:
                mergedList.append(soloDelta)
                soloDelta.next()
            else:
                mergedList.append(conDelta)
                mergedList.next()

    #at this point solo list itr will be complete
    mergedList.extend(itrCon) #add all remaining elements to the merged list
    return mergedList


def nameElements(mergedList, familyName):
    #orders the elements along the chromosomes and based on order renames

    chrDict = {}

    for element in mergedList:
        if element.name not in chrDict:
            chrDict[element.name] = [element]
        else:
            chrDict[element.name] = append(element)
    #dictionary key = chr and values are the elements

    for key in chrDict:
        list = chrDict[key]
        i = 1
        for element in list:
            element.name = familyName + " " + element.name + "-" + i
            i += 1


def findSolos(LTRList,completeCon,allowance):
    #create a new list that contains only the solo elements
        #takes first element and "reaches" with con seq to possible 2nd LTR

    soloList = []
    i = 0
    while i < len(LTRList)-1:
        print(i)

        reach = LTRList[i].endLocation + completeCon
        diff = (LTRList[i+1].startLocation - reach) #need to make sure this is enough

        if(diff > allowance):
            LTRList[i].status = "SOLO"
            soloList.append(LTRList[i])
        else:
            LTRList[i].status = "INTACT"
            LTRList[i+1].status = "INTACT"
            i+=1

        i+=1

        return soloList
