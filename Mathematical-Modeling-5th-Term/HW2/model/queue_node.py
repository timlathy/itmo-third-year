from .buffering_strategy import BufferingStrategy

class QueueNode:
    def __init__(self, p_indexed, node, queues, priorities):
        self.p_eq = f'p_{{{p_indexed[0] + 1}}}'
        self.p = p_indexed[1]
        self.node = node
        self.priorities = priorities
        self.device_occupancy = [node[0] == str(i + 1) for i in range(len(priorities))]

    def is_busy(self, priority=None):
        return self.device_occupancy[priority] if priority is not None else any(self.device_occupancy)

    def queue_occupancy(self, priority):
        return 1 if self.node[1 + priority] != '0' else 0

    def enqueued_count(self, priority=None):
        if priority is not None:
            return sum(1 if q == str(priority + 1) else 0 for q in self.node[1:])
        return sum(self.enqueued_count(priority) for priority in range(len(self.device_occupancy)))

    def loses_task_to(self, priority, buf_strategy):
        assert isinstance(buf_strategy, BufferingStrategy)

        overriden_by_priorities = set()
        for priority2, rels in enumerate(self.priorities):
            if priority2 == priority: continue
            if rels[priority] == 2: # has absolute priority over our class?
                if self.is_busy(priority) and \
                    self.queue_occupancy(priority) > 0 and self.queue_occupancy(priority2) > 0:
                    overriden_by_priorities.add(priority2)
        if self.queue_occupancy(priority) > 0:
            can_override_other_class = any(rel == 2 for rel in self.priorities[priority])
            if can_override_other_class:
                for priority2, rel in enumerate(self.priorities[priority]):
                    if rel == 2:
                        cannot_override_task = self.is_busy() and not self.is_busy(priority2)
                        if not cannot_override_task:
                            continue
                        if buf_strategy == BufferingStrategy.OCCUPY_LOWER_IF_FREE:
                            if self.queue_occupancy(priority) > 0 and self.queue_occupancy(priority2) > 0:
                                overriden_by_priorities.add(priority)
                        else:
                            raise "Unknown buffering strategy"
            else:
                overriden_by_priorities.add(priority)
        return overriden_by_priorities

    def __repr__(self):
        return f'{self.p_eq} ({self.node}): p={self.p}, occupancy={self.device_occupancy}'
