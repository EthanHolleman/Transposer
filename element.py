
class Element:

    def __init__(self,name,startLocation,endLocation,length,status,seq,): #defualt contructor change here
        self.name = "NONE"
        self.startLocation = 0
        self.endLocation = 0
        self.length = 0
        self.status = "NONE"
        self.seq = "NONE"


    def __init__(self,name,startLocation,endLocation,length,status,seq,): #contructor for
        self.name = name
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.length = length
        self.status = status
        self.seq = seq
