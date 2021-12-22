import math
import random


class location:
    def __init__(self, xyz: str) -> None:
        if xyz is not None:
            x, y, z = xyz.split(",")
            self.x, self.y, self.z = float(x), float(y), float(z)
        else:
            self.x = random.uniform(0, 5)
            self.y = random.uniform(0, 5)
            self.z = 0

    def __repr__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

    def distance(self, other):
        a = math.pow(self.x - other.x, 2)
        b = math.pow(self.y - other.y, 2)
        c = math.pow(self.z - other.z, 2)
        return math.sqrt(a + b + c)
