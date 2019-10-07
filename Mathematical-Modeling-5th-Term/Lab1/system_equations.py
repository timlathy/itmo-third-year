class SystemEquations:
    def __init__(self, ps, busy_sym, device_queues):
        queues = {
            device: (queue_idx, q_len) for queue_idx, (device, q_len)
            in enumerate((i, q_len) for i, q_len in enumerate(device_queues) if q_len != 0)
        }
        self.nodes = [
            StateNode(p, node, queues, busy_sym, device_num=len(device_queues))
            for node, p in ps.items()
        ] 

    def rho(self, i_device=None):
        if i_device is None:
            return sum(n.p for n in self.nodes if n.any_device_busy())

        return sum(n.p for n in self.nodes if n.is_busy(i_device))

    def queue_len(self, i_device=None):
        if i_device is None:
            return sum(n.p * n.enqueued_count() for n in self.nodes)

        return sum(n.p * n.enqueued_count(i_device) for n in self.nodes if n.is_busy(i_device))
    
    def task_count(self, i_device=None):
        if i_device is None:
            return sum(n.p * (n.busy_device_count() + n.enqueued_count()) for n in self.nodes)

        return sum(n.p * (1 + n.enqueued_count(i_device)) for n in self.nodes if n.is_busy(i_device))
    
    def loss_probability(self):
        return sum(n.p for n in self.nodes if n.is_fully_occupied)

    def equation_table_csv(self, l, b, q_1, q_2):
        def r(num):
            return str(round(num, 3))

        output = [
            ['Нагрузка', '', '', ''],
            ['', 'П1', '$$y_1 = \lambda q_1 B$$', r(l * q_1 * b)],
            ['', 'П2', '$$y_1 = \lambda q_2 B$$', r(l * q_2 * b)],
            ['', '$$\sum$$', '$$y = \lambda B$$', r(l * b)],
            ['Загрузка', '', '', ''],
            ['', 'П1', '$$\\rho_1 = \sum_{device_1 = T} p_i$$', r(self.rho(0))],
            ['', 'П2', '$$\\rho_2 = \sum_{device_2 = T} p_i$$', r(self.rho(1))],
            ['', '$$\sum$$', '$$\\rho = \sum_{i = 2}^n p_i$$', r(self.rho())],
            ['Длина очереди', '', '', ''],
            ['', 'П1', '$$l_1 = \sum_{i = 1}^n p_i O_1_i$$', r(self.queue_len(0))],
            ['', 'П2', '$$l_2 = \sum_{i = 2}^n p_i O_2_i$$', r(self.queue_len(1))],
            ['', '$$\sum$$', '$$l = \sum_{i = 1}^n p_i (O_1_i+O_2_i)$$', r(self.queue_len())],
            ['Число заявок', '', '', ''],
            ['', 'П1', '$$m_1 = \sum_{device_1 = T} p_i $$', r(self.task_count(0))],
            ['', 'П2', '$$m_2 = \sum_{device_2 = T} p_i $$', r(self.task_count(1))],
            ['', '$$\sum$$', '$$m = \sum p_i (device_1 + device_2 + O_2)$$', r(self.task_count())],
            ['Время ожидания', '', '', ''],
            ['', 'П1', '$$w_1 = m_1/\lambda$$', r(self.task_count(0) * l)],
            ['', 'П2', '$$w_2 = m_2/\lambda$$', r(self.task_count(1) * l)],
            ['', '$$\sum$$', '$$w = m/\lambda$$', r(self.task_count() * l)],
            ['Время пребывания', '', '', ''],
            ['', 'П1', '$$u_1 = w_1 + B$$', r(self.task_count(0) * l + b)],
            ['', 'П2', '$$u_2 = w_2 + B$$', r(self.task_count(1) * l + b)],
            ['', '$$\sum$$', '$$u = w + B$$', r(self.task_count() * l + b)],
            ['Вероятность потери', '', '', ''],
            ['', '$$\sum$$', '$$\pi = \sum_{device_2 = T \& O_2 = 3 || device_1 = T} p_i$$', r(self.loss_probability())],
            ['Производительность', '', '', ''],
            ['', '$$\sum$$', '$$\lambda\' = (1 - \pi) \lambda$$', r((1 - self.loss_probability()) * l)],
        ]
        return '\n'.join(','.join(line) for line in output)


class StateNode:
    def __init__(self, p, node, queues, busy_sym, device_num):
        self.p = p
        self.node = node
        self.device_occupancy = [node[i] == busy_sym for i in range(device_num)]
        self.device_enqueued = [
            int(node[device_num + queues[i_device][0]]) if i_device in queues else 0
            for i_device in range(device_num)
        ]
        self.is_fully_occupied = all(self.device_occupancy) and all(
            self.device_enqueued[i_device] == queues[i_device][1] if i_device in queues else True
            for i_device in range(device_num)
        )
    
    def is_busy(self, i_device):
        return self.device_occupancy[i_device]
    
    def enqueued_count(self, i_device=None):
        if i_device is None:
            return sum(self.device_enqueued)

        return self.device_enqueued[i_device]

    def busy_device_count(self):
        return len(list(occupied for occupied in self.device_occupancy if occupied))

    def any_device_busy(self):
        return any(self.device_occupancy)

    def __repr__(self):
        return f'p={self.p}, node={self.node}, occupancy={self.device_occupancy}, ' +\
               f'enqueued={self.device_enqueued}, fully_occupied={self.is_fully_occupied}'

