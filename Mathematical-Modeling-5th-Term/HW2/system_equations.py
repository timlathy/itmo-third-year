# Regarding node encoding, the first symbol is interpreted as device
# occupancy (0 = free, 1-3 = occupied by the specified priority class),
# the rest are for queues (0 = empty, 1-3 = occupied by a priority class).

# queues: a list of queue sizes for priority classes #0, #1, #2.
# priorities: a list specifying priority class ordering. For instance,
#   you may see "3-2-1" in your assignment, which means that class #3
#   has higher priority than #2. This translates to priorities=[3, 2, 1].

def priority_queue_eqs(ps, queues, priorities):
    assert len(queues) == len(priorities), \
        "Assignments with number of queues /= number of priorities are not supported"
    return SystemEquations([
        PriorityQueueNode(p_indexed, node, queues, priorities)
        for node, p_indexed in ps.items()
    ])

class PriorityQueueNode:
    def __init__(self, p_indexed, node, queues, priorities):
        self.p_eq = f'p_{{{p_indexed[0] + 1}}}'
        self.p = p_indexed[1]
        self.node = node
        self.device_occupancy = [node[0] == str(i + 1) for i in range(len(priorities))]

    def is_busy(self, priority=None):
        return self.device_occupancy[priority] if priority is not None else any(self.device_occupancy)

    def enqueued_count(self, priority=None):
        if priority is not None:
            return 1 if self.node[1 + priority] == str(priority + 1) else 0
        return sum(self.enqueued_count(priority) for priority in range(len(self.device_occupancy)))

    def __repr__(self):
        return f'p_eq={self.p_eq}, p={self.p}, node={self.node}, occupancy={self.device_occupancy}'

class SystemEquations:
    def __init__(self, nodes):
        self.nodes = nodes

    def occupancy(self, priority=None):
        p_sum = sum(n.p for n in self.nodes if n.is_busy(priority))
        eq = ' + '.join(n.p_eq for n in self.nodes if n.is_busy(priority))
        return p_sum, eq

    def queue_len(self, priority=None):
        p_sum = sum(n.p * n.enqueued_count(priority) for n in self.nodes if n.is_busy(priority))
        eq = ' + '.join(n.p_eq for n in self.nodes if n.is_busy(priority) and n.enqueued_count(priority) > 0)
        return p_sum, eq

    def equation_table_csv(self, lambdas, bs):
        def r(num):
            return str(round(num, 3))

        priorities = range(len(lambdas))

        ys = [l * b for l, b in zip(lambdas, bs)]
        occupancies = [self.occupancy(i) for i in priorities]
        queue_lens = [self.queue_len(i) for i in priorities]
        task_counts = [occupancies[i][0] * queue_lens[i][0] for i in priorities]

        output = [
            ['Нагрузка', '', '', ''],
            *[['', f'К{i+1}', f'$$y_{i+1} = \lambda_{i+1} b_{i+1}$$', r(y)] for i, y in enumerate(ys)],
            ['', '$$\sum$$', f'$$y = \sum y_i$$', r(sum(ys))],

            ['Загрузка', '', '', ''],
            *[['', f'К{i+1}', f'$$\\rho_{i+1} = {eq}$$', r(rho)] for i, (rho, eq) in enumerate(occupancies)],
            ['', '$$\sum$$', f'$$\\rho = {self.occupancy()[1]}$$', r(self.occupancy()[0])],

            ['Длина очереди', '', '', ''],
            *[['', f'К{i+1}', f'$$\\l_{i+1} = {eq}$$', r(l)] for i, (l, eq) in enumerate(queue_lens)],
            ['', '$$\sum$$', f'$$\\l = {self.queue_len()[1]}$$', r(self.queue_len()[0])],

            ['Число заявок', '', '', ''],
            *[['', f'К{i+1}', f'$$\\m_{i+1} = l_{i+1} + \\rho_{i+1}$$', r(t)] for i, t in enumerate(task_counts)],
            ['', '$$\sum$$', f'$$\\m_{i+1} = l + \\rho$$', r(self.occupancy()[0] + self.queue_len()[0])],
        ]

        return '\n'.join(','.join(line) for line in output)
