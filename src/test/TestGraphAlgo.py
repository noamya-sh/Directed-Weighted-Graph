from unittest import TestCase

from DiGraph import *
from GraphAlgo import GraphAlgo

"""
unittest class to test GraphAlgo functions
"""


class TestGraphAlgo(TestCase):

    def test_get_graph(self):
        d = DiGraph()
        d.add_node(0, (2, 3, 0))
        d.add_node(1, (4, 5, 0))
        d.add_node(2, (5, 6, 0))
        d.add_node(3, (6, 7, 0))
        d.add_node(4, (7, 8, 0))
        d.add_edge(0, 1, 5.0)
        d.add_edge(1, 0, 1.0)
        d.add_edge(0, 2, 0.5)
        d.add_edge(1, 2, 3.0)
        d.add_edge(2, 3, 4.0)
        d.add_edge(3, 4, 4.0)
        g = GraphAlgo(d)
        self.assertEqual(d, g.get_graph())

    def test_load_from_json(self):
        g = GraphAlgo()
        g.load_from_json("src/data/A1.json")
        self.assertEqual(17, g.get_graph().v_size())

    def test_save_to_json(self):
        g = GraphAlgo()
        g.load_from_json("./data/A1.json")
        g.save_to_json('test.json')
        g2 = GraphAlgo()
        g2.load_from_json('test.json')
        self.assertEqual(g2.get_graph().v_size(), g.get_graph().v_size())
        self.assertEqual(g2.get_graph().e_size(), g.get_graph().e_size())
        self.assertEqual(g2.centerPoint(), g.centerPoint())

    def test_shortest_path(self):
        g = GraphAlgo()
        g.load_from_json('data/A0.json')
        self.assertEqual(g.shortest_path(4, 5), (1.9442789961315767, [4, 5]))
        self.assertEqual(g.shortest_path(7, 2), (6.735613078842625, [7, 6, 5, 4, 3, 2]))
        g.load_from_json('src/data/A2.json')
        self.assertEqual(g.shortest_path(7, 2), (3.4260129130072627, [7, 6, 2]))

    def test_tsp(self):
        d = DiGraph()
        d.add_node(0, (2, 3, 0))
        d.add_node(1, (4, 5, 0))
        d.add_node(2, (5, 6, 0))
        d.add_node(3, (6, 7, 0))
        d.add_node(4, (7, 8, 0))
        d.add_edge(0, 1, 5.0)
        d.add_edge(1, 0, 1.0)
        d.add_edge(0, 2, 0.5)
        d.add_edge(1, 2, 3.0)
        d.add_edge(2, 3, 4.0)
        d.add_edge(3, 4, 4.0)
        g = GraphAlgo(d)
        n = [0, 4]
        k = [0, 2, 3, 4]
        path, dis = g.TSP(n)
        self.assertEqual(k, path)
        self.assertEqual(8.5, dis)

    def test_center_point(self):
        g = GraphAlgo()
        g.load_from_json('data/A0.json')
        self.assertEqual(g.centerPoint(), (7, 6.806805834715163))
        g.load_from_json('data/A3.json')
        self.assertEqual(g.centerPoint(), (2, 8.182236568942237))
        g.load_from_json('data/A5.json')
        self.assertEqual(g.centerPoint(), (40, 9.291743173960954))
