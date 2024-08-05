import hashlib

class ConsistentHashMap:
    def __init__(self, server_containers, N=3, K=9, M=512):
        self.server_containers = server_containers
        self.unhealthy_servers = set()  # Track unhealthy servers
        self.N = N
        self.K = K
        self.M = M
        self.hash_map = [None] * M
        self.populate_hash_map()

    def default_virtual_server_hash_function(self, server_id, index):
        return int(hashlib.md5(f"{server_id}_{index}".encode()).hexdigest(), 16) % self.M

    def populate_hash_map(self):
        self.hash_map = [None] * self.M
        for server in self.server_containers:
            if server not in self.unhealthy_servers:
                self.add_server(server)
        self.print_hash_map()

    def add_server(self, server_id):
        print(f"Adding server: {server_id}")  # Debugging line
        for j in range(self.K):
            virtual_server = f'{server_id}_{j}'
            slot = self.default_virtual_server_hash_function(server_id, j)
            for probe in range(self.M):
                idx = (slot + probe**2) % self.M
                if self.hash_map[idx] is None:
                    self.hash_map[idx] = virtual_server
                    print(f"Assigned {virtual_server} to slot {idx}")  # Debugging line
                    break
            else:
                print(f"Failed to place {virtual_server}")  # Debugging line

    def mark_server_unhealthy(self, server_id):
        self.unhealthy_servers.add(server_id)
        self.repopulate_hash_map()

    def repopulate_hash_map(self):
        self.hash_map = [None] * self.M
        for server in self.server_containers:
            if server not in self.unhealthy_servers:
                self.add_server(server)
        self.print_hash_map()

    def print_hash_map(self):
        assigned = [slot for slot in self.hash_map if slot is not None]
        unassigned = self.hash_map.count(None)
        print(f"Hash map status:\nAssigned slots: {len(assigned)}\nUnassigned slots: {unassigned}")
        print("Sample hash map content (showing first 20 entries):")
        for i, slot in enumerate(self.hash_map[:20]):
            print(f"Slot {i}: {slot}")

    def visualize_hash_map(self):
        import matplotlib.pyplot as plt
        
        slots = range(self.M)
        counts = [0] * self.M
        for slot in self.hash_map:
            if slot is not None:
                idx = self.default_virtual_server_hash_function(slot.split('_')[0], int(slot.split('_')[1]))
                counts[idx] += 1
        
        plt.bar(slots, counts)
        plt.xlabel('Hash Map Slot')
        plt.ylabel('Number of Virtual Servers')
        plt.title('Virtual Server Distribution in Hash Map')
        plt.show()

    def get_server(self, request_id):
        slot = self.default_virtual_server_hash_function(request_id, 0)  # Example usage
        for probe in range(self.M):
            idx = (slot + probe**2) % self.M
            if self.hash_map[idx] is not None:
                return self.hash_map[idx]
        return None
