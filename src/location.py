import math


class location:
    def __init__(self, xyz:str) -> None:
        x,y,z = xyz.split(",")
        self.x,self.y,self.z= float(x),float(y),float(z)

    def __repr__(self):
        return str(self.x)+","+str(self.y)+","+str(self.z)

    def distance(self, other):
        a = math.pow(self.x - other.x, 2)
        b = math.pow(self.y - other.y, 2)
        c = math.pow(self.z - other.z, 2)
        return math.sqrt(a + b + c)
