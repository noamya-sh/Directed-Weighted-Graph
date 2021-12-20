import math
import heapq

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
        return self.dijkstra(id1, id2)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        pass

    def centerPoint(self) -> (int, float):
        dist = math.inf
        ans = None
        for v in self._graph.get_all_v():
            pass
        pass

    def plot_graph(self) -> None:
        pass

    def dijkstra(self, src: int, dest: int = None):
        prev = {i.id: None for i in self._graph.get_all_v()}

        dist = {i.id: math.inf for i in self._graph.get_all_v()}
        dist[src] = 0
        queue = [self._graph.dicNodes.get(src)]
        while queue:
            v = queue[0]
            queue.remove(v)
            if dest != None and v.id == dest:
                d = dist[v.id]
                path = []
                if prev[v.id] != None or v.id == src:
                    while prev[v.id] != None:
                        path.insert(0, v)
                        v = prev[v.id]
                path.insert(0, self._graph.dicNodes.get(src))
                return (d, path)

            for i in v:
                alt = dist[v.id] + i.w
                if alt < dist[i.dest]:
                    dist[i.dest] = alt
                    prev[i.dest] = v
                    queue.append(self._graph.dicNodes.get(i.dest))
                    queue.sort(key=lambda x: dist[x.id])
        if dest == None:
            return max(dist,key=dist.values())

        return (math.inf, [])


if __name__ == '__main__':
    g = GraphAlgo()
    g.load_from_json("A1.json")
    edges =g.get_graph().dicEdges
    print(max(edges,key=lambda x: edges.get(x).w))
    print(g.dijkstra(4, 10))

class dijkstra:
    def __init__(self):
        pass