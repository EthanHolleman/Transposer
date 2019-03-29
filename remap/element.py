
class Element:

    def __init__(self,name,startLocation,endLocation,length,status,seq,):
        #defualt contructor
        self.name = "NONE"
        self.startLocation = 0
        self.endLocation = 0
        self.length = 0
        self.status = "NONE"
        self.seq = "NONE"


    def __init__(self,name,startLocation,endLocation,length,status,seq,):
        self.name = name
        self.startLocation = int(startLocation)
        self.endLocation = int(endLocation)
        self.length = length
        self.status = status
        self.seq = seq

    def toString(self):
        #takes element and returns values as a string on one line
        string = "{},{},{},{},{},{}".format(name, startLocation,endLocation,length,status,seq)
        return string

    def toStringFasta(self):
        #sends element to 2 line string to be added to fasta file
        fastaLine = ">{},{},{},{},{},{}".format(name,startLocation,endLocation,length,status,
        "\n" + seq)
        return fastaLine
        
