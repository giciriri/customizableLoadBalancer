import hashlib

class ConsistentHashMap:
    def __init__(self, N, M, K, hash_function=None, virtual_server_hash_function=None):
        self.N = N
        self.M = M
        self.K = K
        self.hash_function = hash_function or self.default_hash_function
        self.virtual_server_hash_function = virtual_server_hash_function or self.default_virtual_server_hash_function

        self.server_containers = [f'S{i}' for i in range(1, N + 1)]
        self.virtual_servers = self.generate_virtual_servers()
        self.hash_map = [None] * M
        self.populate_hash_map()

    def default_hash_function(self, Rid):
        md5 = hashlib.md5(str(Rid).encode())
        return int(md5.hexdigest(), 16) % self.M

    def default_virtual_server_hash_function(self, Sid, j):
        md5 = hashlib.md5(f"{Sid}{j}".encode())
        return int(md5.hexdigest(), 16) % self.M

    def generate_virtual_servers(self):
        virtual_servers = []
        for i in range(1, self.N + 1):
            for j in range(self.K):
                virtual_servers.append(f'{i}_{j}')
        return virtual_servers

    def populate_hash_map(self):
        self.hash_map = [None] * self.M
        for server in self.server_containers:
            self.add_server(server)

    def add_server(self, Sid):
        for j in range(self.K):
            slot = self.virtual_server_hash_function(Sid, j)
            while self.hash_map[slot] is not None:
                slot = (slot + 1) % self.M
            self.hash_map[slot] = f'{Sid}_{j}'

    def remove_server(self, Sid):
        for j in range(self.K):
            virtual_server = f'{Sid}_{j}'
            for slot, value in enumerate(self.hash_map):
                if value == virtual_server:
                    self.hash_map[slot] = None
                    break

    def map_request(self, Rid):
        slot = self.hash_function(Rid)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.M
        return self.hash_map[slot]

    def get_server(self, Rid):
        virtual_server = self.map_request(Rid)
        # Extract the base server ID from virtual server ID
        server_id = virtual_server.split('_')[0]
        return server_id
    
    def update_servers(self, new_servers):
        self.server_containers = new_servers
        self.virtual_servers = self.generate_virtual_servers()
        self.populate_hash_map()
