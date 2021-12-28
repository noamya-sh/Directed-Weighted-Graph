import math
import time
from heapq import heappop, heappush
from heapdict import heapdict
from typing import List
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from Node import Node
import json
from itertools import count
from gui import *


class GraphAlgo(GraphAlgoInterface):
    """
    This class implement algorithms for direct weighted graph.
    """

    def __init__(self, graph: GraphInterface = None):
        if graph is None:
            self._graph = DiGraph()
        else:
            self._graph = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: This graph.
        """
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        """
        function to load graph from json file.
        :param file_name: path of file
        :return: bool value if success load.
        """
        with open(file_name, 'r') as file:
            g = DiGraph()
            dict_graph = json.load(file)
            for n in dict_graph['Nodes']:
                new_node = Node(**n)
                g.get_dicNodes()[new_node.get_id()] = new_node

            for e in dict_graph['Edges']:
                g.add_edge(e['src'], e['dest'], e['w'])
            g._MC = 0
            self._graph = g
            return True
        return False

    def _toJson(self, object) -> dict:
        """
        cast each object from graph to pattern that fit him.
        :param object: object from graph.
        :return: json format of the object.
        """
        if type(object) == Node:
            return object.asdict()
        else:
            return object.__dict__

    def save_to_json(self, file_name: str) -> bool:
        """
        function to save this graph in json file.
        :param file_name: path to save jason file.
        :return: bool value if success saving.
        """
        with open(file_name, 'w') as file:
            dic = {'Edges': [{'src': k[0], 'w': v, 'dest': k[1]} for k, v in self._graph.get_dicEdges().items()],
                   'Nodes': list(self._graph.get_all_v().values())}
            json.dump(dic, file, default=self._toJson, indent=2)
            return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        function to find shortest path from id to other id.
        :param id1: id of src node.
        :param id2: id of dest node.
        :return: distance of the path and list contain all nodes in path.
        """
        return self._dijkstra(id1, id2)  # run Dijkstra algorithm to find shortest path.

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        function to find path contain all nodes from input.
        :param node_lst: list of nodes to visit them.
        :return: valid path that visit in all nodes from input.
        """
        temp = [i for i in node_lst]
        n = temp[0]
        ans = [n]
        temp.remove(n)
        num = 0
        while len(temp) >= 1:
            dist, prev = self._dijkstra(n)
            new_dist = {k: v for k, v in dist.items() if k in temp}
            t = min(new_dist, key=new_dist.get)
            num += new_dist[t]
            if t is None:
                return None, math.inf
            f = t
            path = []
            if prev[t] is not None or t == n:
                while prev[t]:
                    path.insert(0, t)
                    t = prev[t].get_id()
            n = f
            temp.remove(f)
            ans += path

        return ans, num

    def _isConnected(self) -> bool:
        """
        this function using BFS algorithm to check if graph connected.
        It does this on a source graph and an inverted graph.
        :return: bool value if the graph connected.
        """
        graph = self._graph
        test = {i.get_id(): False for i in graph.get_all_v().values()}
        test2 = {i.get_id(): False for i in graph.get_all_v().values()}
        first = next(iter(test))
        test[first] = True
        queue = [first]
        while queue:
            n = queue.pop()
            enter = graph.all_out_edges_of_node(n)
            for node_id in enter.keys():
                if test[node_id]:
                    continue
                test[node_id] = True
                queue.append(node_id)
        queueReverse = [first]
        while queueReverse:
            n = queueReverse.pop()
            enter = graph.all_in_edges_of_node(n)
            for node_id in enter.keys():
                if test2[node_id]:
                    continue
                test2[node_id] = True
                queueReverse.append(node_id)
        """if visited in all nodes - return true"""
        return all(v == True for v in test.values()) and all(v == True for v in test2.values())

    def _dijkstra(self, src: int, dest: int = None) -> tuple:
        """
        Dijkstra algorithm for find minimal dist from src node.
        We using this function to find shortest path, TSP and center point.
        :param src: src node.
        :param dest: dest node. if None - run on all nodes in graph.
        :return: tuple contain distance and path contain nodes id.
        """
        prev = {i.get_id(): None for i in self._graph.get_all_v().values()}
        dist = {i.get_id(): math.inf for i in self._graph.get_all_v().values()}
        vis = {i.get_id(): False for i in self._graph.get_all_v().values()}
        dist[src] = 0
        heap = []
        c = count()
        heappush(heap, (0, next(c), self._graph.get_dicNodes().get(src)))
        while heap:
            dis, _, v = heappop(heap)
            vis[v.get_id()] = True

            if dest is not None and v.get_id() == dest:
                d = dist[v.get_id()]
                path = []
                if prev[v.get_id()] is not None or v.get_id() == src:
                    while prev[v.get_id()] is not None:
                        path.insert(0, v.get_id())
                        v = prev[v.get_id()]
                path.insert(0, src)
                return d, path

            for i, w in v:
                if vis[i]:
                    continue
                alt = dist[v.get_id()] + w
                if alt < dist[i]:
                    dist[i] = alt
                    prev[i] = v
                    heappush(heap, (alt, next(c), self._graph.get_dicNodes().get(i)))

        if dest is None:
            return dist, prev

        return math.inf, []

    def centerPoint(self) -> (int, float):
        """
        :return: center node of this graph - the node with minimal max distance to rest nodes.
        """
        if not self._isConnected():
            return None, math.inf
        minMax = math.inf
        ans = None
        for v in self._graph.get_all_v().values():
            dist, prev = self._dijkstra(v.get_id())
            temp = dist[max(dist, key=dist.get)]
            if temp < minMax:
                ans = v.get_id()
                minMax = temp
        return ans, minMax

    def plot_graph(self) -> None:
        """
        Draw the graph (using pygame platform).
        """
        gui(self)
