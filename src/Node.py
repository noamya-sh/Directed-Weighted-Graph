import location
class Node:
    def __init__(self, id:int, location: location):
        self.id = id
        self.pos = location
        self.out = {}
        self.enter = {}

    def __iter__(self):
        return self.out.values().__iter__()

    def __str__(self):
        return "pos:"+self.location+","+"id:"+self.id
