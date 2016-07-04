from tempfile import NamedTemporaryFile
from unittest import TestCase

import pygraphviz as pgv

from backend_design.graph import Event
from backend_design.graph import State


class StateA(State):
    pass


class StateB(State):
    pass


class EventA(Event):
    from_state = StateA
    to_state = StateB


class TestDot(TestCase):

    def test_dot(self):
        graph = pgv.AGraph(directed=True)
        EventA.add_to_graph(graph)

        dot_file = NamedTemporaryFile()
        dot_file.write(graph.string())
        dot_file.flush()

        graph_from_dot = pgv.AGraph(dot_file.name)
        self.assertEqual(graph_from_dot.nodes(),
                         ['StateA', 'EventA', 'StateB'])
        self.assertEqual(graph_from_dot.edges(),
                         [('StateA', 'EventA'), ('EventA', 'StateB')])
