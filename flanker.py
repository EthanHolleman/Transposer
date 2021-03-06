import sys, os, subprocess, re
from element import Element

def readPreviousElements(allignFile, accNums):
    #Takes fasta of outdated elements and reads into list of element objects
    prevList = []
    words = []
    elementInfo = ()
    transDict = {}

    try:
        with open(accNums) as nums:
            for line in nums:
                if line != "\n":
                    l = line.strip()
                    l = line.split("\t")

                    transDict[l[0]] = l[1].strip()
    except FileNotFoundError:
        print(allignFile + " not found")

    try:
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

    except FileNotFoundError:
        print(allignFile + " not found")


def getElementSeq(blastdb, element):
    #takes list of elements and uses blastDB to get the sequences should be passed into the createAllignmentList

    try:
        seqCommand = "blastdbcmd -db {} -dbtype nucl -range {}-{} -entry {}".format(blastdb, element.startLocation,
        element.endLocation, element.accession) #name is the current entry

        seq = "".join(((str(subprocess.check_output(seqCommand, shell=True))).split("\\n"))[1:])
        re.sub('[^0-9]','', seq)

        return seq

    except:
        print(blastdb + " error")


def getAccNumbersFromTxt(accFile):
    #pulls the accession numbers from the GenBank accession files
    accNums = []
    try:
        with open(accFile) as acc:
            for line in acc:
                line = line.split("\t")
                if len(line) >1: accNums.append(line[1].strip())
        return accNums

    except FileNotFoundError:
        print(accFile + " not found")


def backMapElements(prevElements, curElements, prevBlastDB, curBlastDB, prevAcc, curAcc):
    #finds element matches between assemblies using blast databases and flanking sequences
    prevIntacts = {}
    prevSolos = {}
    accTranslate = {}
    matchDict = {}

    for cur, prev in zip(getAccNumbersFromTxt(curAcc), getAccNumbersFromTxt(prevAcc)): #building dictionary
        accTranslate[cur] = prev


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

        transAcc = accTranslate[curElement.accession]
        curL, curR = getFlanks(curElement, curBlastDB)
        print("Now testing " + curElement.name + "\n")

        if curElement.status == "INTACT":

            try:
                for prevIntact in prevIntacts[transAcc]: #looping through only elements of same type and chr

                    prevL, prevR = getFlanks(prevIntact,prevBlastDB)

                    if(testFlanks(curL, prevL) and testFlanks(curR,prevR)):

                        print("______found match_________ to " + prevIntact.name + " " + prevIntact.status)
                        print(prevR + " " + curR)
                        print(prevL + " " + curL + "\n")
                        matchDict[curElement] = prevIntact
                        break
            except KeyError:
                continue
                #prevents key error when a new solo on chromosome which did not have one in previous version

        elif curElement.status == "SOLO":
            #putting a prev accession into the data structure

            try:
                for prevSolo in prevSolos[transAcc]: #looping through only elements of same type and chr

                    prevL, prevR = getFlanks(prevSolo,prevBlastDB)

                    if(testFlanks(curL, prevL) and testFlanks(curR,prevR)):
                        print("______found match_________ to " + prevSolo.name + " " + prevSolo.status)
                        print(prevR + " " + curR)
                        print(prevL + " " + curL + "\n")
                        matchDict[curElement] = prevSolo
                        break
            except KeyError:
                continue

    return matchDict


def getFlanks(element, blastdb):
    #uses element and the corresponding blastdb to get right and let flanks
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
    #test flanks from two different elements and returns true if > 95% identity
    count = 0
    for a, b in zip(flankA, flankB):

        if str(a) == str(b):
             count = count + 1 #counts number of equals between flanks


    if count / len(flankA) >= 0.95: return True
    else: return False

def matchsToTxt(matchDict):
    #takes the dictionary of matches from backMapElements and converts to a txt file
    #sequences are ommitted for readability
    counter = 0;
    with open("matchReport.txt", "w") as match:
        for key in matchDict:
            counter +=1
            prev = matchDict[key]
            match.write(key.name + "\t" + prev.name + "\n")
            match.write(key.accession+ "\t" + prev.accession + "\n")
            match.write(key.status+ "\t" + prev.status + "\n")
            match.write(str(key.startLocation) + "\t" + str(prev.startLocation) + "\n")
            match.write(str(key.endLocation) + "\t" + str(prev.endLocation) + "\n")
            match.write(str(key.length)+ "\t" + str(prev.length) + "\n\n")
        match.write(str(counter) + " total matches")
