
class Element:

    def __init__(self,name,startLocation,endLocation,length,seq): #contructor for
        self.name = name
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.length = length
        self.seq = seq


    def createAllignmentList(elementDict):
        elementList = []
        for key in elementDict:
            elementList.append(Element("UNNAMED", key,0,0,elementDict[key]))

        return elementList


    def nameElements():
        #orders the elements along the chromosomes based on relative order
        #adds name based on the order and returns array
        pass

    def findEndLocation(elementArray):
        #takes list of elements and uses start location and sequece to calculate length

        for element in elementArray:
            endLocation = element.startLocation + len(element.seq)
            element.endLocation = endLocation
            elemet.length = element.endLocation - element.startLocation


    def matchLTRPairs():
        #groups the complete LTRs
        #searches location of LTR to end
        pass


    def toFasta():
        #takes an array of the Elements and outputs a fasta formated file
        pass
