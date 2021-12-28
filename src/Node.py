import random

"""This class represent node/vertical of graph"""


class Node:
    """Each Node contain self location, all out edges and all enter edges"""

    def __init__(self, id: int, pos: str = None):
        self._id = id
        if pos is not None:
            x, y, z = pos.split(",")
            self._pos = (float(x), float(y), float(z))
        else:
            self._pos = (random.uniform(0, 5), random.uniform(0, 5), 0)
        self._out = {}
        self._enter = {}

    def get_id(self) -> int:
        return self._id

    def get_pos(self) -> tuple:
        return self._pos

    def get_out(self) -> dict:
        return self._out

    def get_enter(self) -> dict:
        return self._enter

    """Function for cast to json"""

    def asdict(self) -> dict:
        return {"pos": ",".join([str(v) for v in self._pos]), "id": self._id}

    def __iter__(self):
        """
        run on out Edges.
        """
        return self._out.items().__iter__()

    def __repr__(self):
        return str(self._id) + ": |edges out| " + str(len(self._out)) + " |edges in| " + str(len(self._enter))
