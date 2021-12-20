import math
import heapq

from gui import *
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
            dic = {'Edges': list(self._graph.dicEdges.values()), 'Nodes': list(self._graph.get_all_v())}
            json.dump(dic, file, default=self.toJson, indent=2)
            return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        return self.dijkstra(id1, id2)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        temp = [i for i in node_lst]
        n = temp[0]
        ans = [n]
        temp.remove(n)

        while len(temp) >= 1:
            dist, prev = self.dijkstra(n)
            t = min(dist, key=dist.get)
            if t is None:
                return None, math.inf
            f = t
            path = []
            if prev[t] is not None or t == n:
                while prev[t]:
                    path.insert(0, t)
                    t = prev[t]
            n = f
            temp.remove(f)
            ans += path

        return ans

    # def _bfs(self, graph: GraphInterface) -> bool:
    #     test = {i.id: False for i in graph.get_all_v()}
    #     test2 = {i.id: False for i in graph.get_all_v()}
    #     first = next(iter(test))
    #     test[first] = True
    #     queue = [first]
    #     while queue:
    #         n = queue.pop()
    #         enter = graph.all_out_edges_of_node(n)
    #         for id in enter.keys():
    #             if test[id]:
    #                 continue
    #             test[id] = True
    #             queue.append(id)
    #     queueReverse = [first]
    #     while queueReverse:
    #         n = queueReverse.pop()
    #         enter = graph.all_in_edges_of_node(n)
    #         for id in enter.keys():
    #             if test2[id]:
    #                 continue
    #             test2[id] = True
    #             queueReverse.append(id)
    #     return all(v == True for v in test.values()) and all(v == True for v in test2.values())

    def _isConnected(self):
        graph = self._graph
        test = {i.id: False for i in graph.get_all_v()}
        test2 = {i.id: False for i in graph.get_all_v()}
        first = next(iter(test))
        test[first] = True
        queue = [first]
        while queue:
            n = queue.pop()
            enter = graph.all_out_edges_of_node(n)
            for id in enter.keys():
                if test[id]:
                    continue
                test[id] = True
                queue.append(id)
        queueReverse = [first]
        while queueReverse:
            n = queueReverse.pop()
            enter = graph.all_in_edges_of_node(n)
            for id in enter.keys():
                if test2[id]:
                    continue
                test2[id] = True
                queueReverse.append(id)
        return all(v == True for v in test.values()) and all(v == True for v in test2.values())

    def centerPoint(self) -> (int, float):
        if not self._isConnected():
            return -1, math.inf
        minMax = math.inf
        ans = None
        for v in self._graph.get_all_v():
            dist, prev = self.dijkstra(v.id)
            temp = dist[max(dist, key=dist.get)]
            if temp < minMax:
                ans = v.id
                minMax = temp
        return ans, minMax

    def plot_graph(self) -> None:
        gui(self)

    def dijkstra(self, src: int, dest: int = None):
        prev = {i.id: None for i in self._graph.get_all_v()}
        dist = {i.id: math.inf for i in self._graph.get_all_v()}
        dist[src] = 0
        queue = [self._graph.dicNodes.get(src)]
        while queue:
            v = queue[0]
            queue.remove(v)

            if dest is not None and v.id == dest:
                d = dist[v.id]
                path = []
                if prev[v.id] is not None or v.id == src:
                    while prev[v.id] is not None:
                        path.insert(0, v.id)
                        v = prev[v.id]
                path.insert(0, self._graph.dicNodes.get(src))
                return d, path

            for i in v:
                alt = dist[v.id] + i.w
                if alt < dist[i.dest]:
                    dist[i.dest] = alt
                    prev[i.dest] = v
                    queue.append(self._graph.dicNodes.get(i.dest))
                    queue.sort(key=lambda x: dist[x.id])

        if dest is None:
            return dist, prev

        return math.inf, []


if __name__ == '__main__':
    g = GraphAlgo()
    g.load_from_json("./data/A0.json")
    edges = g.get_graph().dicEdges
    print(max(edges, key=lambda x: edges.get(x).w))
    g.save_to_json("test.json")
    print(g.centerPoint())
    g.load_from_json("./data/A1.json")
    print(g.centerPoint())
    g.load_from_json("./data/A2.json")
    print(g.centerPoint())
    g.load_from_json("./data/A1.json")
    print(g.centerPoint())
    print(g._isConnected())
    g.save_to_json("test.json")
    g.plot_graph()
