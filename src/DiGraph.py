from GraphInterface import *
from Node import *


class DiGraph(GraphInterface):
    """
    This class implement GraphInteface.
    The graph contain dict of nodes and dict of edges.
    """

    def __init__(self):
        self._dicNodes = {}  # contain all nodes of graph
        self._dicEdges = {}  # contain all edges of graph
        self._MC = 0  # counter for sum changes in graph

    def get_dicEdges(self) -> dict:
        return self._dicEdges

    def get_dicNodes(self) -> dict:
        return self._dicNodes

    def v_size(self) -> int:
        return len(self._dicNodes)

    def e_size(self) -> int:
        return len(self._dicEdges)

    def get_mc(self) -> int:
        return self._MC

    def get_all_v(self) -> dict:
        return self._dicNodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.get_all_v().get(id1).get_enter()

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.get_all_v().get(id1).get_out()

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        # the function add edge to main dict in graph and to src & dest nodes.
        if (id1, id2) in self._dicEdges.keys():
            return False
        self._dicEdges[(id1, id2)] = weight
        self._dicNodes.get(id1).get_out()[id2] = weight
        self._dicNodes.get(id2).get_enter()[id1] = weight
        self._MC += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._dicNodes.keys():
            return False
        """if exist pos - cast it to string format (using in save_to_json)"""
        if pos:
            n = Node(pos=",".join([str(v) for v in pos]), id=node_id)
        else:
            n = Node(pos=pos, id=node_id)
        self._dicNodes[node_id] = n
        self._MC += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._dicNodes.keys():
            return False
        # remove from all dicts contains edges linked to this node
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
        if (node_id1, node_id2) not in self._dicEdges.keys():
            return False
        n1 = self._dicNodes[node_id1]
        n2 = self._dicNodes[node_id2]
        # remove from dic_out of src node, from dic_enter of dest node and from dicEdges.
        del n1.get_out()[node_id2]
        del n2.get_enter()[node_id1]
        del self._dicEdges[(node_id1, node_id2)]
        self._MC += 1
        return True

    def __repr__(self):
        return f"Graph: |V|={self.v_size()}, |E|={len(self._dicEdges)}"
