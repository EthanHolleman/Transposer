import sys, os, subprocess, re
from element import Element

def readPreviousElements(allignFile, accNums):
    #takes list of previously ided elements and reads into an element list
    #will read in the format given by soybase
    #will be given in a fasta file
    prevList = []
    words = []
    elementInfo = ()
    transDict = {}

    with open(accNums) as nums:
        for line in nums:
            if line != "\n":
                l = line.strip()
                l = line.split("\t")

                transDict[l[0]] = l[1].strip()

            #dict is chromosome number to assenstion num

    with open(allignFile) as elements:

        for i,line in enumerate(elements):
            if i % 2 == 0:
                line = line.strip()
                line = line.split(" ")
                words = line

                acc = words[15].replace("chromosome=Gm", "")
                if acc[0] == "0": acc = acc[1:]


                names = words[0].split("_")
                name = names[2]
                print(name)


                elementInfo = (name,transDict[acc],
                words[14].replace("description=", ""),
                words[16].replace("start=", ""),
                words[17].replace("end=", ""))


            else:
                (name,acc,status, start, end) = elementInfo
                print(elementInfo)
                #prevList.append(new Element(name, start, end, 100, status, line))
                prevList.append(Element(name, acc, start,end,(int(end)- int(start)),status,line))

    return prevList
    #names come out as the accension numbers so they can be taken directly to get ElementSeq

def getElementSeq(blastdb, element):
    #takes list of elements and uses blastDB to get the sequences should be passed into the createAllignmentList
    #blast db should be the latest version of the reference

    #translationDict = {y:x for x,y in dict.items()}
    seqCommand = "blastdbcmd -db {} -dbtype nucl -range {}-{} -entry {}".format(blastdb, element.startLocation,
    element.endLocation, element.accession) #name is the current entry

    seq = "".join(((str(subprocess.check_output(seqCommand, shell=True))).split("\\n"))[1:])
    re.sub('[^0-9]','', seq)

    return seq

def getAccNumbersFromTxt(accFile):
    accNums = []
    with open(accFile) as acc:
        for line in acc:
            line = line.split("\t")
            if len(line) >1: accNums.append(line[1].strip())

    return accNums


def backMapElements(prevElements, curElements, prevBlastDB, curBlastDB, prevAcc, curAcc):
    #lots of shit to d owith element comparisons
    pass
    #get elements of each type and sort by the chromsome they are at

    prevIntacts = {}
    prevSolos = {}
    accTranslate = {}

    for cur, prev in zip(getAccNumbersFromTxt(curAcc), getAccNumbersFromTxt(prevAcc)):
        accTranslate[cur] = prev
        print(cur + " " + prev )


    for element in prevElements:

        if element.status == "INTACT":

            if element.accession in prevIntacts:
                prevIntacts[element.accession].append(element)
            else:
                prevIntacts[element.accession] = [element]

        elif element.status == "SOLO":

            if element.accession in prevSolos:
                prevSolos[element.accession].append(element)
            else:
                prevSolos[element.accession] = [element]

    #start of the actual comparison loop
    for curElement in curElements:
        #not getting the ID of the last tested element for some reason
        transAcc = accTranslate[curElement.accession]
        curL, curR = getFlanks(curElement, curBlastDB)
        print("Testing " + curElement.name + " " + curElement.status + " " + curElement.accession +  " This is the test")
        if curElement.status == "INTACT":

            for prevIntact in prevIntacts[transAcc]: #looping through only elements of same type and chr
                print(prevIntact.name)
                prevL, prevR = getFlanks(prevIntact,prevBlastDB)

                if(testFlanks(curL, prevL)):

                    print("______found match_________ to ")
                    print(curL)
                    print(prevL)
                    break



        elif curElement.status == "SOLO":

            for prevSolo in prevSolos[transAcc]: #looping through only elements of same type and chr

                prevL, prevR = getFlanks(prevSolo,prevBlastDB)

                if(testFlanks(curL, prevL)):
                    print("______found match_________")


def getFlanks(element, blastdb):
    n = 25
    left = element.startLocation - n
    right = element.endLocation + n

    seqCommandLeft = "blastdbcmd -db {} -dbtype nucl -range {}-{} -entry {}".format(blastdb, left,
    element.startLocation, element.accession)
    seqCommandRight = "blastdbcmd -db {} -dbtype nucl -range {}-{} -entry {}".format(blastdb, element.endLocation,
    right, element.accession)

    leftFlank = "".join(((str(subprocess.check_output(seqCommandLeft, shell=True))).split("\\n"))[1:])
    rightFlank = "".join(((str(subprocess.check_output(seqCommandRight, shell=True))).split("\\n"))[1:])


    re.sub('[^0-9]','', leftFlank)
    re.sub('[^0-9]','', rightFlank)
    flanks = (leftFlank, rightFlank)

    return flanks


def testFlanks(flankA, flankB):

    count = 0
    for a, b in zip(flankA, flankB):

        if str(a) == str(b):
             count = count + 1 #counts number of equals between flanks

    #could also return the percent identity with true or false as a tuple
    if count / len(flankA) >= 0.95: return True
    else: return False
