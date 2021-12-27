from unittest import TestCase
from Node import *
from DiGraph import *

"""Unittest class for Node class"""
class TestNode(TestCase):

    def test_get_id(self):
        n = Node(1, "5,4,2")
        self.assertEqual(n.get_id(), 1)

    def test_get_pos(self):
        n = Node(1, "5,4,2")
        self.assertEqual(n.get_pos(), (5.0, 4.0, 2.0))

    def test_get_out(self):
        d = DiGraph()
        d.add_node(1, (5.0, 4.0, 2.0))
        d.add_node(2, (4.0, 3.0, 2.0))
        d.add_edge(1, 2, 3)
        self.assertEqual(d.get_all_v().get(1).get_out(), {2: 3.0})

    def test_get_enter(self):
        d = DiGraph()
        d.add_node(1, (5.0, 4.0, 2.0))
        d.add_node(2, (4.0, 3.0, 2.0))
        d.add_edge(1, 2, 3)
        self.assertEqual(d.get_all_v().get(2).get_enter(), {1: 3.0})
