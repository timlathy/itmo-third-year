# Regarding node encoding, the first symbol is interpreted as device
# occupancy (0 = free, 1-3 = occupied by the specified priority class),
# the rest are for queues (0 = empty, 1-3 = occupied by a priority class).

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

    def get_measures(self, state_probabilties):
      """Returns measures for the model with the given state probabilities (computed using `StateGraph`)."""
      return ModelMeasures(sorted([
          PriorityQueueNode(p_indexed, node, self.queues, self.priorities)
          for node, p_indexed in state_probabilties.items()
      ], key=lambda n: int(n.p_eq[3:-1])))

class PriorityQueueNode:
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

class ModelMeasures:
    def __init__(self, nodes):
        self.nodes = nodes

    def occupancy(self, priority=None):
        p_sum = sum(n.p for n in self.nodes if n.is_busy(priority))
        eq = ' + '.join(n.p_eq for n in self.nodes if n.is_busy(priority))
        return p_sum, eq

    def queue_len(self, priority=None):
        p_sum = sum(n.p * n.enqueued_count(priority) for n in self.nodes)
        def node_eq(n):
            q = n.enqueued_count(priority)
            return (str(q) if q > 1 else '') + '\\cdot ' + n.p_eq
        eq = ' + '.join(node_eq(n) for n in self.nodes if n.enqueued_count(priority) > 0)
        return p_sum, eq

    def loss_probability(self, priority, lambdas):
        priorities = priority if hasattr(priority, '__iter__') else [priority]
        lup = { '0000': 'p0', '1000': 'p1', '2000': 'p2', '3000': 'p3', '1100': 'p4', '2100': 'p5',
            '2003': 'p6', '2020': 'p7', '3100': 'p8', '3003': 'p9', '2120': 'p10', '2103': 'p11',
            '2023': 'p12', '3103': 'p13', '2123': 'p14' }
        nodes = []
        for n in self.nodes:
            loses_task_to = set(p2 for p in priorities for p2 in n.loses_task_to(p))
            if len(loses_task_to) > 0:
                nodes.append((n, loses_task_to))
        nodes.sort(key=lambda n: int(n[0].p_eq[3:-1]))
        p_sum = sum(n.p * sum(lambdas[prio] for prio in priorities) / sum(lambdas) for n, priorities in nodes)
        lambda_terms = lambda priorities: ' + '.join(f'\\lambda_{prio + 1}' for prio in priorities)
        eq = ' + '.join(f'{lup[n.node]}\\cdot (({lambda_terms(priorities)}) / \\sum\\lambda)' for n, priorities in nodes)
        return p_sum, eq

    def measures_table(self, lambdas, bs):
        def r(num):
            return str(round(num, 3))

        priorities = range(len(lambdas))

        ys = [l * b for l, b in zip(lambdas, bs)]
        occupancies = [self.occupancy(i) for i in priorities]
        queue_lens = [self.queue_len(i) for i in priorities]
        task_counts = [occupancies[i][0] + queue_lens[i][0] for i in priorities]
        loss_probs = [self.loss_probability(i, lambdas) for i in priorities]
        loss_prob_p_sum, loss_prob_sum_eq = self.loss_probability(priorities, lambdas)
        throughputs = [l * (1 - pi) for l, (pi, _) in zip(lambdas, loss_probs)]

        mean_wait_times = [l / eff for (l, _), eff in zip(queue_lens, throughputs)]
        mean_wait_time_sum = self.queue_len()[0] / sum(throughputs)

        return [
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
            ['', '$$\sum$$', f'$$\\pi = {loss_prob_sum_eq}$$', r(loss_prob_p_sum)],

            ['Пропускная способность', '', '', ''],
            *[['', f'К{i+1}', f'$$\\lambda\'_{i+1} = \\lambda(1 - \\pi_{i+1})$$', r(eff)] for i, eff in enumerate(throughputs)],
            ['', '$$\sum$$', f'$$\\lambda\' = \\sum \\lambda\'_i$$', r(sum(throughputs))],

            ['Среднее время ожидания', '', '', ''],
            *[['', f'К{i+1}', f'$$w_{i+1} = l_{i+1} / \\lambda\'_{i+1}$$', r(w)] for i, w in enumerate(mean_wait_times)],
            ['', '$$\sum$$', f'$$w = l / \\lambda\'$$', r(mean_wait_time_sum)],

            ['Среднее время пребывания', '', '', ''],
            *[['', f'К{i+1}', f'$$u_{i+1} = w_{i+1} + b_{i+1}$$', r(w + b)] for i, (w, b) in enumerate(zip(mean_wait_times, bs))],
        ]
