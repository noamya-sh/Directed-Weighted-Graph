from location import location


class Node:
    def __init__(self, pos: str, id:int):
        self.id = id
        self.pos = location(pos)
        self.out = {}
        self.enter = {}
    def asdict(self):
        return {"location":self.pos,"id":self.id}
    def __iter__(self):
        return self.out.values().__iter__()
    def __repr__(self):
        return {"location":str(self.pos),"id":self.id}.__repr__()
    def __str__(self):
        return "location:" + self.pos + "," + "id:" + self.id
