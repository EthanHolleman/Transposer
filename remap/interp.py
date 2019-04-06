import os
from element import Element

def toSortedBam(samFile):
    #takes a sam file and converts to sorted bam using samtools
    try:
        outputFile = samFile
        if not ".sam" in outputFile:
            outputFile = outputFile + ".sam"

        bam = samFile.replace(".sam",".bam")
        sortedBam = samFile.replace(".sam",".sorted.bam")

        commandBam = "samtools view -S -b {} > {}".format(samFile,bam) #commands to be executed
        commandSort = "samtools sort {} -o {}".format(bam,sortedBam)

        os.system(commandBam)
        os.system(commandSort)

        try: #removes redundant files but leaves the sorted bam for user
            os.system("rm {}".format(samFile))
            os.system("rm {}".format(bam))

        except FileNotFoundError:
            print("FileNotFoundError at toSortedBam when trying to remove files")

        return sortedBam # returns a sorted bam file name corresponding to one created in method

    except FileNotFoundError:
        print("FileNotFoundError at toSortedBam in search.py")

def toTxt(samFile):
    #takes a sam or bam file and converts to txt using samtools view
    outputFile = samFile + ".txt"

    try:
        command = "samtools view {} > {}".format(samFile,outputFile)
        os.system(command)
        return outputFile #returns txt file name corresponding to txt file created

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
            element.status = "INTACT"

            try:
                element.name = dict[element.name] #uses provided dictionary to set name to chr number

            except KeyError:
                print("keyError at createAllignmentList")
                print("key used was " + element.name)

        os.system("rm {}".format(bamToTxtFile)) # removes txt version as no longer used

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
    print(len(soloList))
    print("This is the same of the solo list")
    ## WARNING: Still requires testing
    #takes the LTR list and complete element list and merges in order
        #order based on chr number first then start location with lowest first
    mergedList = []
    done = "DONE"
    iterCon = iter(conList)
    iterSolo = iter(soloList)
    soloDelta = next(iterSolo, done)
    conDelta = next(iterCon, done)

    while soloDelta != done and conDelta != done:
        print(str(conDelta.startLocation) + " " + conDelta.status)
        if soloDelta.name < conDelta.name: #testing for chr number
            mergedList.append(soloDelta)
            soloDelta = next(iterSolo,done)
        elif soloDelta.name > conDelta.name:
            mergedList.append(conDelta)
            conDelta = next(iterCon,done)
        else:
            if soloDelta.startLocation < conDelta.startLocation:
                mergedList.append(soloDelta)
                soloDelta = next(iterSolo,done)
            else:
                mergedList.append(conDelta)
                conDelta = next(iterCon,done)

    #at this point solo list iter will be complete

    if soloDelta == done:
        print("solo was done first")
        while conDelta != done:
            mergedList.append(conDelta)
            conDelta = next(iterCon,done)

    elif conDelta == done:
        print("con was done first")
        while soloDelta != done:
            mergedList.append(soloDelta)
            soloDelta = next(iterSolo,done)


     #add all remaining elements to the merged list

    return mergedList


def nameElements(mergedList, familyName):
    #orders the elements along the chromosomes and based on order renames
    chrDict = {}
    finalList = []

    for element in mergedList:
        if element.name not in chrDict: #names at this point are only ints
            chrDict[element.name] = [element]
        else:
            chrDict[element.name].append(element) #if already present adds to a list corresponding to chr number

    for key in chrDict:
        list = chrDict[key] #gets list of elements sorted into a given chr number key
        i = 1 #acts as element counter reset at each new key
        for element in list: #loops through elements in chr list
            element.name = str(familyName) + " " + element.name + "-" + str(i)
            finalList.append(element)
            i += 1
    return finalList




def findSolos(LTRList,completeCon,allowance):
    #takes list of LTR elements and determines if each should be considered a solo element based on allowance
    ##TODO need to write method for getting completeCon length
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
