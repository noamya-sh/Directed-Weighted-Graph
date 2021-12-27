from unittest import TestCase
from DiGraph import DiGraph
from Node import Node

"""
unittest class to test DiGraph functions
"""


class TestDiGraph(TestCase):
    def test_v_size(self):
        g = DiGraph()
        g.add_node(1, (1, 1, 0))
        g.add_node(2, (2, 2, 0))
        g.add_node(3, (3, 3, 0))
        g.add_node(4, (4, 4, 0))
        self.assertTrue(g.v_size(), 4)
        g.add_node(5, (7, 8, 0))
        self.assertTrue(g.v_size(), 5)

    def test_e_size(self):
        g = DiGraph()
        g.add_node(1, (1, 1, 0))
        g.add_node(2, (2, 2, 0))
        g.add_node(3, (3, 3, 0))
        g.add_node(4, (4, 4, 0))
        g.add_edge(3, 2, 7.55)
        g.add_edge(1, 3, 65)
        g.add_edge(1, 4, 75)
        self.assertTrue(g.e_size(), 3)
        g.add_edge(4, 1, 31)
        self.assertTrue(g.e_size(), 4)
        g.remove_edge(1, 3)
        self.assertTrue(g.e_size(), 3)

    def test_get_mc(self):
        g = DiGraph()
        g.add_node(1, (1, 1, 0))
        g.add_node(2, (2, 2, 0))
        g.add_node(3, (3, 3, 0))
        g.add_node(4, (4, 4, 0))
        g.add_edge(3, 2, 7.55)
        g.add_edge(1, 3, 65)
        g.add_edge(1, 4, 75)
        self.assertTrue(g.get_mc(), 7)
        g.add_edge(4, 1, 31)
        self.assertTrue(g.get_mc(), 8)
        g.remove_edge(1, 3)
        self.assertTrue(g.get_mc(), 9)

    def test_add_edge(self):
        g = DiGraph()
        g.add_node(1, (1, 1, 0))
        g.add_node(2, (2, 2, 0))
        g.add_node(3, (3, 3, 0))
        g.add_node(4, (4, 4, 0))
        g.add_edge(3, 2, 7.55)
        g.add_edge(1, 3, 65)
        g.add_edge(1, 4, 75)
        self.assertTrue(g._dicEdges[1, 3], g.get_dicNodes().get(1).get_out()[3])
        g.add_edge(4, 1, 31)
        self.assertTrue(g._dicEdges[4, 1], g.get_dicNodes().get(4).get_out()[1])
        g.add_edge(2, 3, 44)
        self.assertTrue(g._dicEdges[2, 3], g.get_dicNodes().get(2).get_out()[3])

    def test_add_node(self):
        z = (1, 1, 0)
        z2 = ("1,1,0")
        y = (2, 2, 0)
        x = (3, 3, 0)
        w = (4, 4, 0)
        x2 = ("3,3,0")
        w2 = ("4,4,0")
        g = DiGraph()
        g.add_node(1, z)
        g.add_node(2, y)
        g.add_node(3, x)
        g.add_node(4, w)
        self.assertTrue(g._dicNodes[1], Node(2, z2))
        self.assertTrue(g._dicNodes[3], Node(3, x2))
        self.assertTrue(g._dicNodes[4], Node(4, w2))

    def test_remove_node(self):
        g = DiGraph()
        g.add_node(1, (1, 1, 0))
        g.add_node(2, (2, 2, 0))
        g.add_node(3, (3, 3, 0))
        g.add_node(4, (4, 4, 0))
        g.add_edge(3, 2, 7.55)
        g.add_edge(1, 3, 65)
        g.add_edge(1, 4, 75)
        g.remove_node(2)
        self.assertTrue(g.v_size(), 3)
        self.assertTrue(g.e_size(), 2)
        g.remove_node(1)
        self.assertTrue(g.v_size(), 2)
        # self.assertTrue(g.e_size(), 0)

    def test_remove_edge(self):
        z = (1, 1, 0)
        y = (2, 2, 0)
        x = (3, 3, 0)
        w = (4, 4, 0)
        g = DiGraph()
        g.add_node(1, z)
        g.add_node(2, y)
        g.add_node(3, x)
        g.add_node(4, w)
        g.add_edge(3, 2, 7.55)
        g.add_edge(1, 3, 65)
        g.add_edge(1, 4, 75)
        self.assertTrue(g.e_size(), 3)
        g.remove_edge(3, 2)
        self.assertTrue(g.e_size(), 2)
        g.remove_edge(1, 4)
        self.assertTrue(g.e_size(), 1)
