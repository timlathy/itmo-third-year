from enum import Enum
class BufferingStrategy(Enum):
    # Occupy the queue of a lower-priority class if it's free, otherwise lose the task
    OCCUPY_LOWER_IF_FREE = 1
