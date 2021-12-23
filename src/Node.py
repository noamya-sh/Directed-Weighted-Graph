import random

class Node:
    def __init__(self, id: int, pos: str = None):
        self._id = id
        if pos is not None:
            x, y, z = pos.split(",")
            self._pos = (float(x), float(y), float(z))
        else:
            self._pos = (random.uniform(0, 5),random.uniform(0, 5),0)
            #self._pos = location(pos)  # location(pos)
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
        return {"pos": ",".join([str(v) for v in self._pos]), "id": self._id}

    def __iter__(self):
        return self._out.items().__iter__()

    def __repr__(self):
        return {"pos": ",".join([str(v) for v in self._pos]), "id": self._id}.__repr__()
