import hashlib

class ConsistentHashMap:
    def __init__(self, N, M, K, hash_function=None, virtual_server_hash_function=None):
        self.N = N  # Number of server containers managed by the load balancer
        self.M = M  # Total number of slots in the consistent hash map
        self.K = K  # Number of virtual servers for each server container

        self.hash_function = hash_function or self.default_hash_function
        self.virtual_server_hash_function = virtual_server_hash_function or self.default_virtual_server_hash_function

        self.server_containers = [f'S{i}' for i in range(1, N + 1)]
        self.virtual_servers = self.generate_virtual_servers()
        self.hash_map = {slot: None for slot in range(M)}
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
                virtual_servers.append(f'S{i}_{j}')
        return virtual_servers

    def populate_hash_map(self):
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
            for slot, value in self.hash_map.items():
                if value == virtual_server:
                    self.hash_map[slot] = None
                    break

    def map_request(self, Rid):
        slot = self.hash_function(Rid)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.M
        server_id = self.hash_map[slot]
        return server_id

    def get_server(self, Rid):
        return self.map_request(Rid)

    def debug_hash_map(self):
        for slot, value in self.hash_map.items():
            if value:
                print(f"Slot {slot}: {value}")

# Example usage
if __name__ == "__main__":
    N = 3
    M = 512
    K = 9
    chm = ConsistentHashMap(N, M, K)

    chm.debug_hash_map()

    requests = [132574, 237891, 982345, 674512, 876234, 543289]
    for Rid in requests:
        server = chm.map_request(Rid)
        print(f"Request {Rid} mapped to server {server}")