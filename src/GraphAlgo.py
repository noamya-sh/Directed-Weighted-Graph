from src import *
from typing import List

from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from Edge import Edge
from src.Node import Node
from src.location import location
import json


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: GraphInterface = None):
        self._graph = graph

    def get_graph(self) -> GraphInterface:
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        with open(file_name, 'r') as file:
            g = DiGraph()
            dict_graph = json.load(file)
            for n in dict_graph['Nodes']:
                newNode = Node(**n)
                g.dicNodes[newNode.id] = newNode

            for e in dict_graph['Edges']:
                g.add_edge(e['src'], e['dest'], e['w'])
            g.MC = 0
            self._graph = g

    def toJson(self, object):
        if type(object) == Node:
            return object.asdict()
        else:
            return object.__dict__

    def save_to_json(self, file_name: str) -> bool:
        with open(file_name, 'w') as file:
            dic = {}
            dic['Edges'] = list(self._graph.dicEdges.values())
            dic['Nodes'] = list(self._graph.get_all_v())
            json.dump(dic, file, default=self.toJson, indent=2)
            return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        pass

    def centerPoint(self) -> (int, float):
        pass

    def plot_graph(self) -> None:
        pass
