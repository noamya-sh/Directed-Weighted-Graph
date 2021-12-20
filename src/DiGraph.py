from GraphInterface import *
from Edge import *
from Node import *
from location import *


class DiGraph(GraphInterface):
    def __init__(self):
        self.dicNodes = {}
        self.dicEdges = {}
        self.MC = 0

    def v_size(self) -> int:
        return len(self.dicNodes)

    def e_size(self) -> int:
        return len(self.dicEdges)

    def get_mc(self) -> int:
        return self.MC

    def get_all_v(self) -> dict:
        return self.dicNodes.values()

    def all_in_edges_of_node(self, id1: int) -> dict:
        return dict([(k[0],v.w) for k,v in self.dicEdges.items() if k[1] == id1])

    def all_out_edges_of_node(self, id1: int) -> dict:
        return dict([(k[1],v.w) for k,v in self.dicEdges.items() if k[0] == id1])

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        e = Edge(id1, id2, weight)
        self.dicEdges[(id1,id2)] = e
        self.dicNodes.get(id1).out[id2] = e
        self.dicNodes.get(id2).enter[id1] = id2
        self.MC += 1
        return True

    def add_node(self, node_id: int, pos: str = None) -> bool:
        l = pos(pos)
        n = Node(pos, node_id)
        self.dicNodes[node_id] = n
        self.MC += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        n = self.dicNodes[node_id]
        for i in n.enter.keys():
            del self.dicEdges[(i ,node_id)]
            del self.dicNodes.get(i).out[node_id]
        for i in n.out.keys():
            del self.dicEdges[(node_id,i)]
        del self.dicNodes[node_id]
        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        n1 = self.dicNodes[node_id1]
        n2 = self.dicNodes[node_id2]
        del n1.out[node_id2]
        del n2.enter[node_id1]
        del self.dicEdges[(node_id1,node_id2)]
        self.MC += 1
        return True

    def __repr__(self):
        return f"Edges:{self.dicEdges}, Nodes:{self.dicNodes}"
