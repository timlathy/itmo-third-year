class SystemEquations:
    # ps: a dict of {'0000': 0.xxxx}, where
    #     '0000' is a state node, 0.xxx is the probability of this state.
    def __init__(self, ps, busy_sym, device_queues):
        queues = {
            device: queue_idx for queue_idx, device
            in enumerate(i for i, q_len in enumerate(device_queues) if q_len != 0)
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

class StateNode:
    def __init__(self, p, node, queues, busy_sym, device_num):
        self.p = p
        self.device_occupancy = [node[i] == busy_sym for i in range(device_num)]
        self.device_enqueued = [
            int(node[device_num + queues[i_device]]) if i_device in queues else 0
            for i_device in range(device_num)
        ]
    
    def is_busy(self, i_device):
        return self.device_occupancy[i_device]
    
    def enqueued_count(self, i_device):
        return self.device_enqueued[i_device]
    
    def any_device_busy(self):
        return any(self.device_occupancy)

