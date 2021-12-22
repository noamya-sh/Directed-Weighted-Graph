from location import location


class Node:
    def __init__(self, id:int, pos: str=None):
        self._id = id
        self._pos = location(pos)#location(pos)
        self._out = {}
        self._enter = {}

    def get_id(self):
        return self._id
    def get_pos(self):
        return self._pos
    def get_out(self):
        return self._out
    def get_enter(self):
        return self._enter
    def asdict(self):
        return {"pos":str(self._pos.x)+","+str(self._pos.y)+","+str(self._pos.z),"id":self._id}
    def __iter__(self):
        return self._out.values().__iter__()
    def __repr__(self):
        return {"pos":str(self._pos),"id":self._id}.__repr__()

