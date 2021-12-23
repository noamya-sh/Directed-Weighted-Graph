import math
import time
from queue import PriorityQueue

from heapdict import heapdict

from gui import *
from typing import List
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from Node import Node
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
                new_node = Node(**n)
                g.get_dicNodes()[new_node.get_id()] = new_node

            for e in dict_graph['Edges']:
                g.add_edge(e['src'], e['dest'], e['w'])
            g._MC = 0
            self._graph = g
            return True
        return False

    def _toJson(self, object):
        if type(object) == Node:
            return object.asdict()
        else:
            return object.__dict__

    def save_to_json(self, file_name: str) -> bool:
        with open(file_name, 'w') as file:
            dic = {'Edges': [{'src': k[0], 'w': v, 'dest': k[1]} for k, v in self._graph.get_dicEdges().items()],
                   'Nodes': list(self._graph.get_all_v().values())}
            json.dump(dic, file, default=self._toJson, indent=2)
            return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        return self._dijkstra(id1, id2)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
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

    def _isConnected(self):
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
        return all(v == True for v in test.values()) and all(v == True for v in test2.values())

    def centerPoint(self) -> (int, float):
        start = time.time()
        if not self._isConnected():
            return -1, math.inf
        min_max = math.inf
        ans = None
        for v in self._graph.get_all_v().values():
            start = time.time()
            dist, prev = self._dijkstra(v.get_id())
            temp = dist[max(dist, key=dist.get)]

            if temp < min_max:
                ans = v.get_id()
                min_max = temp
            end = time.time()
            print(v, end - start)
        return ans, min_max

    def plot_graph(self) -> None:
        gui(self)

    def _dijkstra(self, src: int, dest: int = None):
        prev = {i.get_id(): None for i in self._graph.get_all_v().values()}
        dist = {i.get_id(): math.inf for i in self._graph.get_all_v().values()}
        vis = {i.get_id(): False for i in self._graph.get_all_v().values()}
        dist[src] = 0
        # queue = [self._graph.get_dicNodes().get(src)]
        hd = heapdict()
        hd[self._graph.get_dicNodes().get(src)] = 0
        # pq = PriorityQueue()
        # pq.put((0, self._graph.get_dicNodes().get(src)))
        while hd:
            v, p = hd.popitem()  # pq.get()
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
                    hd[self._graph.get_dicNodes().get(i)] = alt
                    dist[i] = alt
                    prev[i] = v
                    # pq.put((alt, self._graph.get_dicNodes().get(i)))
                    # queue.append(self._graph.get_dicNodes().get(i))
                    # queue.sort(key=lambda x: dist[x.get_id()])

        if dest is None:
            return dist, prev

        return math.inf, []


if __name__ == '__main__':
    g = GraphAlgo()
    g.load_from_json("./data/A0.json")
    # edges = g.get_graph().get_dicEdges()
    # print(max(edges, key=lambda x: edges.get(x).get_w()))
    g.save_to_json("test.json")
    print(g.centerPoint())
    g.load_from_json("./data/A1.json")
    print(g.centerPoint())
    g.load_from_json("./data/A2.json")
    print(g.centerPoint())
    g.load_from_json("./data/A5.json")
    print(g.centerPoint())
    print(g._isConnected())
