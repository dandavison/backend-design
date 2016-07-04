import pygraphviz as pgv

from backend_design.graph import Cluster
from backend_design.graph import Transition
from backend_design.graph import State


class StateA(State):
    pass


class StateB(State):
    pass


class StateC(State):
    pass


class Transition1(Transition):
    from_state = StateA
    to_state = StateB


class Transition2(Transition):
    from_state = StateB
    to_state = StateC


class ABCluster(Cluster):
    nodes = [StateA, StateB]
    style = 'filled'
    fillcolor = 'hotpink'
    color = 'invis'


class CCluster(Cluster):
    nodes = [StateC]
    style = 'filled'
    fillcolor = 'skyblue'
    color = 'invis'


transitions = [Transition1, Transition2]
clusters = [ABCluster, CCluster]

graph = pgv.AGraph(directed=True)
for transition in transitions:
    transition.add_to_graph(graph)
for cluster in clusters:
    cluster.add_to_graph(graph)

# output dot format
print(graph.string())

# create image output from python directly
graph.layout()
graph.draw('example_1.png')
