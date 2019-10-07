def separate_queues_eqs(ps, busy_sym, device_queues):
    queues = {
        device: (queue_idx, q_len) for queue_idx, (device, q_len)
        in enumerate((i, q_len) for i, q_len in enumerate(device_queues) if q_len != 0)
    }
    return SystemEquations([
        SeparateQueueNode(p, node, queues, busy_sym, device_num=len(device_queues))
        for node, p in ps.items()
    ])

def shared_queue_eqs(ps, busy_sym, queue_len):
    return SystemEquations([
        SharedQueueNode(p, node, queue_len, busy_sym)
        for node, p in ps.items()
    ])

class SystemEquations:
    def __init__(self, nodes):
        self.nodes = nodes

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

    def equation_table_csv(self, l, b, qs):
        def r(num):
            return str(round(num, 3))

        efficiency = (1 - self.loss_probability()) * l

        output = []
        output.append(['Нагрузка', '', '', ''])
        for i, q in enumerate(qs):
          output.append(['', f'П{i+1}', f'$$y_{i+1} = \lambda q_{i+1} B$$', r(l * q * b)])
        output.append(['', '$$\sum$$', '$$y = \lambda B$$', r(l * b)])
        output.append(['Загрузка', '', '', ''])
        for i, q in enumerate(qs):
          output.append(['', f'П{i+1}', f'$$\\rho_{i+1} = \sum_{{device_{i+1} = T}} p_i$$', r(self.rho(i))])
        output.append(['', '$$\sum$$', '$$\\rho = \sum_{i = 2}^n p_i$$', r(self.rho())])

        output.append(['Длина очереди', '', '', ''])
        for i, q in enumerate(qs):
          output.append(['', f'П{i+1}', f'$$l_{i+1} = \sum_{{i = 1}}^n p_i O_{i+1}_i$$', r(self.queue_len(i))])
        output.append(['', '$$\sum$$', '$$l = \sum_{i = 1}^n p_i (\sum O_j_i)$$', r(self.queue_len())])

        output.append(['Число заявок', '', '', ''])
        for i, q in enumerate(qs):
          output.append(['', f'П{i+1}', f'$$m_{i+1} = \sum_{{device_{i+1} = T}} p_i $$', r(self.task_count(i))])
        output.append(['', '$$\sum$$', '$$m = \sum p_i (\sum device_i + O_i)$$', r(self.task_count())])
        output.append(['Время ожидания', '', '', ''])
        for i, q in enumerate(qs):
          output.append(['', f'П{i+1}', f'$$w_{i+1} = l_{i+1}/\lambda\'$$', r(self.queue_len(i) / efficiency)])
        output.append(['', '$$\sum$$', '$$w = l/\lambda\'$$', r(self.queue_len() / efficiency)])

        output.append(['Время пребывания', '', '', ''])
        for i, q in enumerate(qs):
            output.append(['', f'П{i+1}', f'$$u_{i+1} = m_{i+1}/\lambda\'$$', r(self.task_count(i) / efficiency)])
        output.append(['', '$$\sum$$', '$$u = l/\lambda\'$$', r(self.task_count() / efficiency)])

        output.append(['Вероятность потери', '', '', ''])
        output.append(['', '$$\sum$$', '$$\pi = \sum_{device_1 = T \& O_1 = 1 \& device_2 = T & device_3 = T} p_i$$', r(self.loss_probability())])
        output.append(['Производительность', '', '', ''])
        output.append(['', '$$\sum$$', '$$\lambda\' = (1 - \pi) \lambda$$', r((1 - self.loss_probability()) * l)])

        return '\n'.join(','.join(line) for line in output)


class SeparateQueueNode:
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

class SharedQueueNode:
    def __init__(self, p, node, queue_len, busy_sym):
        device_num = len(node) - 1 # - queue

        self.p = p
        self.node = node
        self.device_occupancy = [node[i] == busy_sym for i in range(device_num)]

        self.is_fully_occupied = all(self.device_occupancy) and self.enqueued_count() == queue_len
    
    def is_busy(self, i_device):
        return self.device_occupancy[i_device]
    
    def enqueued_count(self, i_device=None):
        return int(self.node[-1])

    def busy_device_count(self):
        return len(list(occupied for occupied in self.device_occupancy if occupied))

    def any_device_busy(self):
        return any(self.device_occupancy)

    def __repr__(self):
        return f'p={self.p}, node={self.node}, occupancy={self.device_occupancy}, ' +\
               f'fully_occupied={self.is_fully_occupied}'

