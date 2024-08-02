import hashlib

class ConsistentHashMap:
    def __init__(self, N, M, K, hash_function=None, virtual_server_hash_function=None):
        """
        Initializes a ConsistentHashMap object.

        Args:
            N: Number of server containers managed by the load balancer.
            M: Total number of slots in the consistent hash map.
            K: Number of virtual servers for each server container.
            hash_function: Optional custom hash function for mapping requests to slots.
            virtual_server_hash_function: Optional custom hash function for mapping virtual servers to slots.
        """
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
        """
        Default hash function for mapping requests to slots.
        """
        md5 = hashlib.md5(str(Rid).encode())
        return int(md5.hexdigest(), 16) % self.M

    def default_virtual_server_hash_function(self, Sid, j):
        """
        Default hash function for mapping virtual servers to slots.
        """
        md5 = hashlib.md5(f"{Sid}{j}".encode())
        return int(md5.hexdigest(), 16) % self.M

    def generate_virtual_servers(self):
        """
        Generates virtual servers for each server container.
        """
        virtual_servers = []
        for i in range(1, self.N + 1):
            for j in range(self.K):
                virtual_servers.append(f'S{i}_{j}')
        return virtual_servers

    def populate_hash_map(self):
        """
        Populates the hash map with virtual servers.
        """
        self.hash_map = [None] * self.M
        for server in self.server_containers:
            self.add_server(server)

    def add_server(self, Sid):
        """
        Adds a server container and its virtual servers to the hash map.
        """
        for j in range(self.K):
            slot = self.virtual_server_hash_function(Sid, j)
            while self.hash_map[slot] is not None:
                slot = (slot + 1) % self.M
            self.hash_map[slot] = f'{Sid}_{j}'

    def remove_server(self, Sid):
        """
        Removes a server container and its virtual servers from the hash map.
        """
        for j in range(self.K):
            virtual_server = f'{Sid}_{j}'
            for slot, value in enumerate(self.hash_map):
                if value == virtual_server:
                    self.hash_map[slot] = None
                    break

    def map_request(self, Rid):
        """
        Maps a request to a server container based on its virtual server.
        """
        slot = self.hash_function(Rid)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.M
        server_id = self.hash_map[slot]
        return server_id

    def get_server(self, Rid):
        """
        Returns the server container assigned to a request.
        """
        return self.map_request(Rid)

    def debug_hash_map(self):
        """
        Prints the contents of the hash map for debugging purposes.
        """
        for slot, value in enumerate(self.hash_map):
            if value:
                print(f"Slot {slot}: {value}")

    def update_servers(self, new_servers):
        """
        Updates the list of server containers and re-populates the hash map.
        """
        self.server_containers = new_servers
        self.virtual_servers = self.generate_virtual_servers()
        self.populate_hash_map()
