import hashlib

class ConsistentHashMap:
    def __init__(self, N, M, K):
        self.N = N
        self.M = M
        self.K = K
        self.ring = {}
        self.servers = []
        self._initialize_ring()

    def _initialize_ring(self):
        # Add virtual servers to the ring
        for server_id in range(1, self.N + 1):
            for i in range(self.K):
                virtual_server_id = f"{server_id}_{i}"
                self.servers.append(virtual_server_id)
                hash_value = self._hash(virtual_server_id)
                self.ring[hash_value] = virtual_server_id

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.M

    def add_server(self, Sid):
        for i in range(self.K):
            virtual_server_id = f"{Sid}_{i}"
            self.servers.append(virtual_server_id)
            hash_value = self._hash(virtual_server_id)
            self.ring[hash_value] = virtual_server_id

    def remove_server(self, Sid):
        for i in range(self.K):
            virtual_server_id = f"{Sid}_{i}"
            hash_value = self._hash(virtual_server_id)
            if hash_value in self.ring:
                del self.ring[hash_value]
            if virtual_server_id in self.servers:
                self.servers.remove(virtual_server_id)

    def map_request(self, Rid):
        hash_value = self._hash(Rid)
        closest_server = min(self.ring.keys(), key=lambda k: (k - hash_value) % self.M)
        return self.ring[closest_server]
