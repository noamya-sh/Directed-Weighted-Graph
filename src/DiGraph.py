from GraphInterface import *
from Edge import *
from Node import *
from location import *
class DiGreaph(GraphInterface):
    def __init__(self):
        self.dicNode = {}
        self.dicEdges = {}
        self.MC = 0

    def v_size(self) -> int:
        return len(self.dicNode)

    def e_size(self) -> int:
        return len(self.dicEdges)

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        e = Edge(id1,id2,weight)
        self.dicEdges[id1+'_'+id2] = e
        self.dicNode.get(id1).out[id2] = e
        self.dicNode.get(id2).enter[id1] = id2
        self.MC += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        l = location(pos.index(0),pos.index(1),pos.index(2))
        n = Node(node_id,l)
        self.dicNode[node_id] = n
        self.MC += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        n = self.dicNode[node_id]
        for i in n.enter.keys():
            del self.dicEdges[i+"_"+node_id]
            del self.dicNode.get(i).out[node_id]
        for i in n.out.keys():
            del self.dicEdges[node_id+"_"+i]
        del self.dicNode[node_id]
        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        n1 = self.dicNode[node_id1]
        n2 = self.dicNode[node_id2]
        del n1.out[node_id2]
        del n2.enter[node_id1]
        del self.dicEdges[node_id1+"_"+node_id2]
        self.MC +=1
        return True