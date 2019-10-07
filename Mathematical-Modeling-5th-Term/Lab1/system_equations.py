class SystemEquations:
    def __init__(self, ps, free_sym, busy_sym, device_queues):
        self.ps = ps
        self.free_sym = free_sym
        self.busy_sym = busy_sym
        self.queues = {device: queue_idx for queue_idx, device
                       in enumerate(i for i, q_len in enumerate(device_queues) if q_len != 0)}
        self.device_num = len(device_queues)

    def ro_device(self, i_device):
        return sum(p for node, p in self.ps.items() if node[i_device] == self.busy_sym)
    
    def ro_system(self):
        return sum(p for node, p in self.ps.items() if not self.all_devices_free(node))

    def queue_len(self, i_device):
        return sum(p * self.enqueued_count(node, i_device)
           for node, p in self.ps.items() if node[i_device] == self.busy_sym)
    
    def task_count(self, i_device):
        return sum(p * (1 + self.enqueued_count(node, i_device))
                   for node, p in self.ps.items() if node[i_device] == self.busy_sym)
    
    # === Node utils
    
    def all_devices_free(self, node):
        for i in range(self.device_num):
            if node[i] == self.busy_sym:
                return False
        return True
    
    def enqueued_count(self, node, i_device):
        if i_device in self.queues:
            return int(node[self.device_num + self.queues[i_device]])
        return 0

