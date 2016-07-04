import inspect

from backend_design.utils import classproperty


class _Node(object):
    _private_attribute_names = set()

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
    def get_attributes(cls):
        attrs = {
            'label': cls.label,
        }
        attrs.update({
            key: value
            for key, value in vars(cls).iteritems()
            if cls.is_public_data_attribute(key, value)
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

    @classmethod
    def add_to_graph(cls, graph):
        graph.add_node(cls)
        pgv_node = graph.get_node(cls)
        pgv_node.attr.update(cls.get_attributes())


class State(_Node):
    pass


class Event(_Node):
    from_state = None
    to_state = None

    _private_attribute_names = {'from_state', 'to_state'}

    @classmethod
    def get_edge_data(cls):
        return cls.from_state, cls.to_state, cls.key

    @classmethod
    def add_to_graph(cls, graph):
        cls.from_state.add_to_graph(graph)
        super(Event, cls).add_to_graph(graph)
        cls.to_state.add_to_graph(graph)

        graph.add_edge(cls.from_state, cls)
        graph.add_edge(cls, cls.to_state)
