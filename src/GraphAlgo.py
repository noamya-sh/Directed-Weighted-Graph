from src import *
from typing import List
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
from src.Edge import Edge
from src.Node import Node
from src.location import location

class GraphAlgo(GraphAlgoInterface):
    def __init__(self,graph:GraphInterface):
        self._graph = graph

    def get_graph(self) -> GraphInterface:
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        pass

    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        pass
    def centerPoint(self) -> (int, float):
        pass
    def plot_graph(self) -> None:
        pass