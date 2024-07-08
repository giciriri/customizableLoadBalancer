import hashlib

class ConsistentHashMap:
    def __init__(self, num_servers, num_slots, virtual_servers_per_server):
        self.num_servers = num_servers
        self.num_slots = num_slots
        self.virtual_servers_per_server = virtual_servers_per_server

        self.server_containers = [f'S{i}' for i in range(1, num_servers + 1)]
        self.virtual_servers = self.generate_virtual_servers()

        self.hash_map = [None] * num_slots

        for server_id in range(1, num_servers + 1):
            self.add_server(server_id)

    def generate_virtual_servers(self):
        virtual_servers = []
        for i in range(1, self.num_servers + 1):
            for j in range(self.virtual_servers_per_server):
                virtual_servers.append(f'S{i}_{j}')
        return virtual_servers

    def hash_function(self, key):
        return int(hashlib.sha256(str(key).encode('utf-8')).hexdigest(), 16) % self.num_slots

    def add_server(self, server_id):
        for j in range(self.virtual_servers_per_server):
            slot = self.hash_function(f'S{server_id}_{j}')
            while self.hash_map[slot] is not None:
                slot = (slot + 1) % self.num_slots
            self.hash_map[slot] = f'S{server_id}_{j}'

    def remove_server(self, server_id):
        for j in range(self.virtual_servers_per_server):
            virtual_server = f'S{server_id}_{j}'
            for slot in range(self.num_slots):
                if self.hash_map[slot] == virtual_server:
                    self.hash_map[slot] = None

    def map_request(self, request_id):
        slot = self.hash_function(request_id)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.num_slots
        return self.hash_map[slot]
