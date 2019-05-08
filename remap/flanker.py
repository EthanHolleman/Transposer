import sys, os, subprocess, re
from element import Element

def readPreviousElements(allignFile):
    #takes list of previously ided elements and reads into an element list
    #will read in the format given by soybase
    #will be given in a fasta file
    prevList = []
    words = []
    elementInfo = ()
    with open(allignFile) as elements:

        for i,line in enumerate(elements):
            if i % 2 == 0:
                line = line.strip()
                line = line.split(" ")
                words = line

                elementInfo = (words[0],
                words[14].replace("description=", ""),
                 words[16].replace("start=", ""),
                 words[17].replace("end=", ""))


            else:
                (name, status, start, end) = elementInfo
                #prevList.append(new Element(name, start, end, 100, status, line))
                prevList.append(Element(name, start,end,(int(end)- int(start)),status,line))
                
    return prevList


def getElementSeq(blastdb, element):
    #takes list of elements and uses blastDB to get the sequences should be passed into the createAllignmentList
    #blast db should be the latest version of the reference

    #translationDict = {y:x for x,y in dict.items()}
    seqCommand = "blastdbcmd -db {} -dbtype nucl -range {}-{} -entry {}".format(blastdb, element.startLocation,
    element.endLocation, element.name)
    print(seqCommand)
    seq = "".join(((str(subprocess.check_output(seqCommand, shell=True))).split("\\n"))[1:])
    re.sub('[^0-9]','', seq)

    return seq


def matchElements(prevElements, curElements):
    pass

def testFlanks(flankA, flankB):

    count = 0
    for a, b in zip(flankA, flankB):
        print(a + " " + b)
        if str(a) == str(b):
             count = count + 1 #counts number of equals between flanks
             print(count)
    #could also return the percent identity with true or false as a tuple
    if count / len(flankA) >= 0.95: return True
    else: return False
