import os
from element import Element

def toSortedBam(samFile):
    #takes a sam file and covernts to sorted bam using samtools
    try:
        outputFile = samFile
        if not ".sam" in outputFile:
            outputFile = outputFile + ".sam"

        commandBam = "samtools view -S -b {} > {}".format(samFile,samFile.replace(".sam",".bam"))
        commandSort = "samtools sort {} -o {}".format(samFile,samFile.replace(".sam",".sorted.bam"))
        os.system(commandBam)
        os.system(commandSort)

        return outputFile.replace(".sam", ".sorted.bam")

    except FileNotFoundError:
        print("FileNotFoundError at toSortedBam in search.py")

def toTxt(samFile):
    #takes a sam or bam file and converts to txt using samtools view
    outputFile = str(samFile) + ".txt"
    print(outputFile + " " + "to txt working")
    try:
        command = "samtools view {} > {}".format(samFile,outputFile)
        print(command)
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

        for element in elementList:
            element.endLocation = element.startLocation + len(element.seq) #sets end endLocation
            element.length = element.endLocation - element.startLocation #sets length

            try:
                element.name = dict[element.name]

            except KeyError:
                print("keyError at createAllignmentList")
                print("key used was " + element.name)

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


def mergeLists(soloList, conList): #not getting the sololist for some reason

    ## WARNING: Still requires testing
    #takes the LTR list and complete element list and merges in order
        #order based on chr number first then start location with lowest first
    mergedList = []
    done = "DONE"
    print(conList)

    iterCon = iter(conList,done)
    iterSolo = iter(soloList,done)

    while next(iterSolo )!= done:
        soloDelta = next(iterSolo)
        conDelta = next(iterCon)

        if soloDelta.name < conDelta.name: #testing for chr number
            mergedList.append(soloDelta)
            next(soloDelta)
        elif soloDelta.name > conDelta.name:
            mergedList.append(soloDelta)
            next(conDelta)
        else:
            if soloDelta.startLocation < conDelta.startLocation:
                mergedList.append(soloDelta)
                next(soloDelta)
            else:
                mergedList.append(conDelta)
                next(mergedList)

    #at this point solo list iter will be complete
    mergedList.extend(iterCon) #add all remaining elements to the merged list
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
        ## TODO: not returning list correctly is empty
    soloList = []
    i = 0
    print(len(LTRList))

    while i < len(LTRList):
        print(i)
        print("solos")

        print(i)
        reach = LTRList[i].endLocation + completeCon
        diff = (LTRList[i+1].startLocation - reach) #need to make sure this is enough
        print(diff)
        #print(diff)

        if(diff > -(completeCon) and diff <= 0): #test for truncated element
            LTRList[i].status = "INTACT"
            LTRList[i+1].status = "INTACT"
            i+=1
            if i==len(LTRList)-1: # breaks if next element is the last in the list
                break
        elif (abs(diff) > allowance):
            LTRList[i].status = "SOLO"
            soloList.append(LTRList[i])
            if i == len(LTRList)-2: #breaks if second to last LTR is a solo, b/c next LTR must also be a solo
                soloList.append(LTRList[i+1])
                break
        else:
            LTRList[i].status = "INTACT"
            LTRList[i+1].status = "INTACT"
            i+=1
            if i == len(LTRList)-1: # breaks if next element is the last in the list
                break

        i+=1

    return soloList
