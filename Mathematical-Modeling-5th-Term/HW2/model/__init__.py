from .queue_node import QueueNode
from .model_measures import ModelMeasures
from .state_graph_builder import StateGraphBuilder
from .variations import variation_table, variation_plot_to_file

class Model:
    # queues: a list of queue sizes for priority classes.
    # priorities: a matrix (list of row lists) showing relationship between priority classes.
    def __init__(self, queues, priorities):
        """Constructs a model with the specified queues and priority classes.

        Parameters
        ----------
        queues : list of ints
            queue sizes for priority classes, e.g. [1, 1, 1]
        priorities : list of row lists
            a matrix of relationships between priority classes.
            Example: an absolute 2-3-1 priority is [[0, 0, 0], [2, 0, 2], [2, 0, 0]]
        """
        assert len(queues) == len(priorities), "Each priority class has to have a queue"
        self.queues = queues
        self.priorities = priorities

    def state_graph_builder(self):
      """Returns a state graph builder with a graphviz-like interface"""
      return StateGraphBuilder(len(self.priorities))

    def get_measures(self, state_probabilties):
      """Returns measures for the model with the given state probabilities (computed using `StateGraph`)."""
      return ModelMeasures(sorted([
          QueueNode(p_indexed, node, self.queues, self.priorities)
          for node, p_indexed in state_probabilties.items()
      ], key=lambda n: int(n.p_eq[3:-1])))
