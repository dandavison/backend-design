import inspect

from backend_design.utils import classproperty


class GraphComponent(object):
    _private_attribute_names = set()
    _dynamic_properties_to_include_in_attributes = set()

    @classmethod
    def get_attributes(cls):
        attrs = {}
        for ancestral_cls in reversed(cls.mro()):
            attrs.update({
                key: value
                for key, value in vars(ancestral_cls).iteritems()
                if cls.is_public_data_attribute(key, value)
            })
        attrs.update({
            property_name: getattr(cls, property_name)
            for property_name in cls._dynamic_properties_to_include_in_attributes
        })
        return attrs

    @classmethod
    def is_public_data_attribute(cls, name, value):
        if name in cls._private_attribute_names:
            return False
        elif name.startswith('_'):
            return False
        elif inspect.ismethoddescriptor(value):
            return False
        else:
            return True


class _NodeMetaclass(type):

    def __str__(self):
        return self.key


class _Node(GraphComponent):
    __metaclass__ = _NodeMetaclass

    _dynamic_properties_to_include_in_attributes = set()

    def __init__(self, *args, **kwargs):
        raise TypeError("Node subclasses serve as singletons and "
                        "can not be instantiated.")

    @classproperty
    def label(cls):
        return cls.__name__

    @classproperty
    def key(cls):
        return cls.label

    @classmethod
    def add_to_graph(cls, graph):
        graph.add_node(cls)
        pgv_node = graph.get_node(cls)
        pgv_node.attr.update(cls.get_attributes())


class Service(_Node):
    shape = 'rectangle'
    inputs = []
    outputs = []

    _private_attribute_names = {'inputs', 'outputs'}

    @classmethod
    def add_to_graph(cls, graph):
        super(Service, cls).add_to_graph(graph)

        for node in cls.inputs:
            graph.add_edge(node, cls)

        for node in cls.outputs:
            graph.add_edge(cls, node)


class State(_Node):
    shape = 'oval'


class Transition(_Node):
    from_state = None
    to_state = None
    shape = 'rectangle'

    _private_attribute_names = {'from_state', 'to_state'}

    @classmethod
    def add_to_graph(cls, graph):
        super(Transition, cls).add_to_graph(graph)

        if cls.from_state:
            cls.from_state.add_to_graph(graph)
            graph.add_edge(cls.from_state, cls)

        if cls.to_state:
            cls.to_state.add_to_graph(graph)
            graph.add_edge(cls, cls.to_state)


class Cluster(GraphComponent):
    nodes = []

    _private_attribute_names = ['nodes', 'name']

    @classproperty
    def name(cls):
        return 'cluster_' + cls.__name__

    @classmethod
    def add_to_graph(cls, graph):
        graph.add_subgraph(cls.nodes, name=cls.name, **cls.get_attributes())
