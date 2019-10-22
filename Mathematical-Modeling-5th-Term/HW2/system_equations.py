# Regarding node encoding, the first symbol is interpreted as device
# occupancy (0 = free, 1-3 = occupied by the specified priority class),
# the rest are for queues (0 = empty, 1-3 = occupied by a priority class).

# queues: a list of queue sizes for priority classes #0, #1, #2.
# priorities: a list specifying priority class ordering. For instance,
#   you may see "3-2-1" in your assignment, which means that class #3
#   has higher priority than #2. This translates to priorities=[3, 2, 1].

# Note that PriorityQueueNode#can_lose_task is assignment-specific.

def priority_queue_eqs(ps, queues, priorities):
    assert len(queues) == len(priorities), \
        "Assignments with number of queues /= number of priorities are not supported"
    return SystemEquations(sorted([
        PriorityQueueNode(p_indexed, node, queues, priorities)
        for node, p_indexed in ps.items()
    ], key=lambda n: int(n.p_eq[3:-1])))

class PriorityQueueNode:
    def __init__(self, p_indexed, node, queues, priorities):
        self.p_eq = f'p_{{{p_indexed[0] + 1}}}'
        self.p = p_indexed[1]
        self.node = node
        self.lowest_priority_i = priorities[-1] - 1
        self.device_occupancy = [node[0] == str(i + 1) for i in range(len(priorities))]

    def is_busy(self, priority=None):
        return self.device_occupancy[priority] if priority is not None else any(self.device_occupancy)

    def enqueued_count(self, priority=None):
        if priority is not None:
            return 1 if self.node[1 + priority] == str(priority + 1) else 0
        return sum(self.enqueued_count(priority) for priority in range(len(self.device_occupancy)))

    # ! Assignment-specific
    def can_lose_task(self, priority):
        lowest_priority = priority == self.lowest_priority_i
        can_override_lower_priority = not lowest_priority \
            and self.device_occupancy[self.lowest_priority_i] \
            and self.enqueued_count(self.lowest_priority_i) == 0
        return self.node[1 + priority] != '0' and not can_override_lower_priority

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

    def loss_probability(self, priority):
        p_sum = sum(n.p for n in self.nodes if n.can_lose_task(priority))
        eq = ' + '.join(n.p_eq for n in self.nodes if n.can_lose_task(priority))
        return p_sum, eq

    def equation_table_csv(self, lambdas, bs):
        def r(num):
            return str(round(num, 3))

        priorities = range(len(lambdas))

        ys = [l * b for l, b in zip(lambdas, bs)]
        occupancies = [self.occupancy(i) for i in priorities]
        queue_lens = [self.queue_len(i) for i in priorities]
        task_counts = [occupancies[i][0] * queue_lens[i][0] for i in priorities]
        loss_probs = [self.loss_probability(i) for i in priorities]
        loss_prob_p_sum = sum(pi for pi, _ in loss_probs)
        loss_prob_eq = ' + '.join(eq for _, eq in loss_probs)
        efficiencies = [l * (1 - pi) for l, (pi, _) in zip(lambdas, loss_probs)]

        mean_wait_times = [l / eff for (l, _), eff in zip(queue_lens, efficiencies)] 
        mean_wait_time_sum = self.queue_len()[0] / sum(efficiencies)

        output = [
            ['Нагрузка', '', '', ''],
            *[['', f'К{i+1}', f'$$y_{i+1} = \lambda_{i+1} b_{i+1}$$', r(y)] for i, y in enumerate(ys)],
            ['', '$$\sum$$', f'$$y = \sum y_i$$', r(sum(ys))],

            ['Загрузка', '', '', ''],
            *[['', f'К{i+1}', f'$$\\rho_{i+1} = {eq}$$', r(rho)] for i, (rho, eq) in enumerate(occupancies)],
            ['', '$$\sum$$', f'$$\\rho = {self.occupancy()[1]}$$', r(self.occupancy()[0])],

            ['Длина очереди', '', '', ''],
            *[['', f'К{i+1}', f'$$l_{i+1} = {eq}$$', r(l)] for i, (l, eq) in enumerate(queue_lens)],
            ['', '$$\sum$$', f'$$l = {self.queue_len()[1]}$$', r(self.queue_len()[0])],

            ['Число заявок', '', '', ''],
            *[['', f'К{i+1}', f'$$m_{i+1} = l_{i+1} + \\rho_{i+1}$$', r(t)] for i, t in enumerate(task_counts)],
            ['', '$$\sum$$', f'$$m_ = l + \\rho$$', r(self.occupancy()[0] + self.queue_len()[0])],

            ['Вероятность потери', '', '', ''],
            *[['', f'К{i+1}', f'$$\\pi_{i+1} = {eq}$$', r(pi)] for i, (pi, eq) in enumerate(loss_probs)],
            ['', '$$\sum$$', f'$$\\pi = {loss_prob_eq}$$', r(loss_prob_p_sum)],

            ['Производительность', '', '', ''],
            *[['', f'К{i+1}', f'$$\\lambda\'_{i+1} = \\lambda(1 - \\pi_{i+1})$$', r(eff)] for i, eff in enumerate(efficiencies)],
            ['', '$$\sum$$', f'$$\\lambda\' = \\sum \\lambda\'_i$$', r(sum(efficiencies))],

            ['Среднее время ожидания', '', '', ''],
            *[['', f'К{i+1}', f'$$w_{i+1} = l_{i+1} / \\lambda\'_{i+1}$$', r(w)] for i, w in enumerate(mean_wait_times)],
            ['', '$$\sum$$', f'$$w = l / \\lambda\'$$', r(mean_wait_time_sum)],

            ['Среднее время пребывания', '', '', ''],
            *[['', f'К{i+1}', f'$$u_{i+1} = w_{i+1} + b_{i+1}$$', r(w + b)] for i, (w, b) in enumerate(zip(mean_wait_times, bs))],
        ]

        return '\n'.join(','.join(line) for line in output)
