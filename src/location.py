import math

class location:
    def __init__(self,x:float, y:float,z:float)->None:
        self.x = x
        self.y = y
        self.z = z

    def distance(self,other):
        a = math.pow(self.x - other.x,2)
        b = math.pow(self.y - other.y,2)
        c = math.pow(self.z - other.z,2)
        return math.sqrt(a+b+c)