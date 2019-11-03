class ModelMeasures:
    def __init__(self, model, nodes, lambdas, bs):
        self.model = model
        self.nodes = nodes
        self.lambdas = lambdas
        self.bs = bs

    def measures_table(self):
        def r(num):
            return str(round(num, 3))

        priorities = range(len(self.lambdas))

        ys = [l * b for l, b in zip(self.lambdas, self.bs)]
        occupancies = [self.occupancy(i) for i in priorities]
        queue_lens = [self.queue_len(i) for i in priorities]
        task_counts = [occupancies[i][0] + queue_lens[i][0] for i in priorities]
        loss_probs = [self.loss_probability(i) for i in priorities]
        loss_prob_p_sum, loss_prob_sum_eq = self.loss_probability(priorities)
        throughputs = [l * (1 - pi) for l, (pi, _) in zip(self.lambdas, loss_probs)]

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
            *[['', f'К{i+1}', f'$$u_{i+1} = w_{i+1} + b_{i+1}$$', r(w + b)] for i, (w, b) in enumerate(zip(mean_wait_times, self.bs))],
        ]

    def occupancy(self, priority=None):
        p_sum = sum(n.p for n in self.nodes if n.is_busy(priority))
        eq = ' + '.join(n.p_eq for n in self.nodes if n.is_busy(priority))
        return p_sum, eq

    def queue_len(self, priority=None):
        p_sum = sum(n.p * n.enqueued_count(priority) for n in self.nodes)
        def node_eq(n):
            q = n.enqueued_count(priority)
            return (str(q) + '\\cdot ' if q > 1 else '') + n.p_eq
        eq = ' + '.join(node_eq(n) for n in self.nodes if n.enqueued_count(priority) > 0)
        return p_sum, eq

    def loss_probability(self, priority):
        priorities = priority if hasattr(priority, '__iter__') else [priority]
        nodes = []
        for n in self.nodes:
            loses_task_to = set(p2 for p in priorities for p2 in n.loses_task_to(p, self.model.buf_strategy))
            if len(loses_task_to) > 0:
                nodes.append((n, loses_task_to))
        nodes.sort(key=lambda n: int(n[0].p_eq[3:-1]))
        p_sum = sum(
            n.p * sum(self.lambdas[prio] for prio in priorities) / sum(self.lambdas)
            for n, priorities in nodes
        )
        lambda_terms = lambda priorities: ' + '.join(f'\\lambda_{prio + 1}' for prio in priorities)
        eq = ' + '.join(f'{n.p_eq}\\cdot (({lambda_terms(priorities)}) / \\sum\\lambda)' for n, priorities in nodes)
        return p_sum, eq
