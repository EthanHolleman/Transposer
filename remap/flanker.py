import sys, os, subprocess
from element import Element

#needs to take list of elements and search the blast db for them
#need to create the blastdb
#ideas Flanker object that contains the blast DB and infor for the strands

class Flank():

    def __intit__(self, element, flanks):
        self.element = element #element object
        self.flanks = flanks #tuple

    def __eq__(self):
        pass
        #elements are equal if the flanking sequences are simiilar enough and of same status

def createBLASTDB():
    pass
    #assuming blast DB has already been created for now
    #need database of the old and the new reference sequences

def makeFlankList(elementList, blastdb, flankLength, dict):
    #need to convert chr to assenstion nums
    translationDict = my_dict2 = {y:x for x,y in dict.items()} #swaps keys and values so chr are now values
    flankList = []

    for element in elementList:
        makeRightFlank = "blastdbcmd -db {} -dbtype nucl -range {}-{} -entry {}".format(blastdb,
        element.endLocation,(element.endLocation + flankLength),translationDict[element.name])

        makeLeftFlank = "blastdbcmd -db {} -dbtype nucl -range {}-{} -entry {}".format(blastdb,
        (element.startLocation-flankLength),element.startLocation,translationDict[element.name])

        outputRight = "".join(((str(subprocess.check_output(makeRightFlank, shell=True))).split("\\n")).pop(0))
        outputLeft = "".join(((str(subprocess.check_output(makeLeftFlank, shell=True))).split("\\n")).pop(0))
        #runs subprocess, converts to str, splits on \\n, removes first value, joins back to string

        flankList.append(Flank(element,(outputLeft, outputright)))

    return flankList


def testFlanks(listRemapedElements, listPreviousElements, assenstionNums):
    pass
