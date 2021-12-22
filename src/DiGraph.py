from GraphInterface import *
from Edge import *
from Node import *
from location import *


class DiGraph(GraphInterface):
    def __init__(self):
        self._dicNodes = {}
        self._dicEdges = {}
        self._MC = 0

    def get_dicEdges(self) -> dict:
        return self._dicEdges

    def get_dicNodes(self)->dict:
        return self._dicNodes

    def v_size(self) -> int:
        return len(self._dicNodes)

    def e_size(self) -> int:
        return len(self._dicEdges)

    def get_mc(self) -> int:
        return self._MC

    def get_all_v(self) -> dict:
        return self._dicNodes.values()

    def all_in_edges_of_node(self, id1: int) -> dict:
        return dict([(k[0], v.get_w()) for k, v in self._dicEdges.items() if k[1] == id1])

    def all_out_edges_of_node(self, id1: int) -> dict:
        return dict([(k[1], v.get_w()) for k, v in self._dicEdges.items() if k[0] == id1])

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        e = Edge(id1, id2, weight)
        self._dicEdges[(id1, id2)] = e
        self._dicNodes.get(id1)._out[id2] = e
        self._dicNodes.get(id2)._enter[id1] = id2
        self._MC += 1
        return True

    def add_node(self, node_id: int, pos: str = None) -> bool:
        n = Node(pos=pos, id=node_id)
        self._dicNodes[node_id] = n
        self._MC += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        n = self._dicNodes[node_id]
        for i in n.get_enter().keys():
            del self._dicEdges[(i, node_id)]
            del self._dicNodes.get(i).get_out()[node_id]
        for i in n.get_out().keys():
            del self._dicEdges[(node_id, i)]
        del self._dicNodes[node_id]
        self._MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        n1 = self._dicNodes[node_id1]
        n2 = self._dicNodes[node_id2]
        del n1.get_out()[node_id2]
        del n2.get_enter()[node_id1]
        del self._dicEdges[(node_id1, node_id2)]
        self._MC += 1
        return True

    def __repr__(self):
        return f"Graph: |V|={self.v_size()}, |E|=:{len(self._dicEdges)}"
