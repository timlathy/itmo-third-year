from .model_measures import ModelMeasures
from .model_variations import ModelVariations
from .queue_node import QueueNode
from .state_graph_builder import StateGraphBuilder
from .buffering_strategy import BufferingStrategy

class Model:
    graph = None

    def __init__(self, queues, priorities, buf_strategy):
        """Constructs a model with the specified parameters.

        Parameters
        ----------
        queues : list of ints
            queue sizes for priority classes, e.g. [1, 1, 1]
        priorities : list of row lists
            a matrix of relationships between priority classes.
            Example: an absolute 2-3-1 priority is [[0, 0, 0], [2, 0, 2], [2, 0, 0]]
        buf_stategy : BufferingStrategy
        """
        assert len(queues) == len(priorities), "Each priority class has to have a queue"
        assert isinstance(buf_strategy, BufferingStrategy)
        self.queues = queues
        self.priorities = priorities
        self.buf_strategy = buf_strategy

    def state_graph_builder(self):
        """Returns a state graph builder with a graphviz-like interface"""

        if self.graph is None:
            self.graph = StateGraphBuilder(num_priorities=len(self.priorities))
        return self.graph

    def state_probability_matrix(self, lambdas, bs):
        """Returns a matrix of state probabilities for the model with the given λs and Bs."""
        states = self.graph.solve(lambdas, mus=[1 / b for b in bs])
        return self.graph.probability_table(states)

    def get_measures(self, lambdas, bs):
        """Returns measures for the model with the given λs and Bs."""

        assert len(lambdas) == len(self.priorities), "Specify λ for each priority class"
        assert len(bs) == len(self.priorities), "Specify B for each priority class"

        states = self.graph.solve(lambdas, mus=[1 / b for b in bs])
        nodes = [
            QueueNode(p_indexed, node, self.queues, self.priorities)
            for node, p_indexed in states.items()
        ]
        nodes.sort(key=lambda n: int(n.p_eq[3:-1]))

        return ModelMeasures(self, nodes, lambdas, bs)
