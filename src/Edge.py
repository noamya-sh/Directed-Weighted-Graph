class Edge:
    def __init__(self, src: int, dest: int, weight: float,**d):
        self._src = src
        self._w = weight
        self._dest = dest

    def get_src(self):
        return self._src

    def get_w(self):
        return self._w

    def get_dest(self):
        return self._dest

    def asdict(self):
        return {"src":self._src,"w":self._w,"dest":self._dest}
