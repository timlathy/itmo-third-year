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

    def ro_device(self, i_device):
        return sum(n.p for n in self.nodes if n.is_busy(i_device))
    
    def ro_system(self):
        return sum(n.p for n in self.nodes if n.any_device_busy())

    def queue_len(self, i_device):
        return sum(n.p * n.enqueued_count(i_device) for n in self.nodes if n.is_busy(i_device))
    
    def task_count(self, i_device):
        return sum(n.p * (1 + n.enqueued_count(i_device)) for n in self.nodes if n.is_busy(i_device))
    
    def loss_probability(self):
        return sum(n.p for n in self.nodes if n.is_fully_occupied)


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
    
    def enqueued_count(self, i_device):
        return self.device_enqueued[i_device]
    
    def any_device_busy(self):
        return any(self.device_occupancy)
    
    def __repr__(self):
        return f'p={self.p}, node={self.node}, occupancy={self.device_occupancy}, \
                 enqueued={self.device_enqueued}, fully_occupied={self.is_fully_occupied}'

