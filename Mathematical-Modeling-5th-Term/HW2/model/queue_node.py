class QueueNode:
    def __init__(self, p_indexed, node, queues, priorities):
        self.p_eq = f'p_{{{p_indexed[0] + 1}}}'
        self.p = p_indexed[1]
        self.node = node
        self.priorities = priorities
        self.device_occupancy = [node[0] == str(i + 1) for i in range(len(priorities))]

    def is_busy(self, priority=None):
        return self.device_occupancy[priority] if priority is not None else any(self.device_occupancy)

    def enqueued_count(self, priority=None):
        if priority is not None:
            return 1 if self.node[1 + priority] == str(priority + 1) else 0
        return sum(self.enqueued_count(priority) for priority in range(len(self.device_occupancy)))

    def loses_task_to(self, priority):
        overriden_by_priorities = set()
        for priority2, rels in enumerate(self.priorities):
            if priority2 == priority: continue
            if rels[priority] == 2: # has absolute priority over our class?
                if self.is_busy(priority) and \
                    self.enqueued_count(priority) > 0 and self.enqueued_count(priority2) > 0:
                    overriden_by_priorities.add(priority2)
        if self.enqueued_count(priority) > 0:
            can_override_other_class = any(rel == 2 for rel in self.priorities[priority])
            if can_override_other_class:
                for priority2, rel in enumerate(self.priorities[priority]):
                    if rel == 2:
                        cannot_override_task = self.is_busy() and not self.is_busy(priority2)
                        if self.enqueued_count(priority) > 0 and cannot_override_task:
                            overriden_by_priorities.add(priority)
            else:
                overriden_by_priorities.add(priority)
        return overriden_by_priorities

    def __repr__(self):
        return f'p_eq={self.p_eq}, p={self.p}, node={self.node}, occupancy={self.device_occupancy}'
