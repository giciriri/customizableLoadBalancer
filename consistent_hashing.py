import hashlib

class ConsistentHashMap:
    def __init__(self, num_slots=512, num_virtual_servers=92):
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.slots = [None] * num_slots
        self.servers = []
        self.virtual_servers = {}

    def add_server(self, server_id):
        self.servers.append(server_id)
        for i in range(self.num_virtual_servers):
            virtual_server_id = self.virtual_server_hash_function(server_id, i) % self.num_slots
            self.virtual_servers[virtual_server_id] = server_id
            self.slots[virtual_server_id] = server_id
        print(f"Added server: {server_id}, Virtual servers: {[self.virtual_server_hash_function(server_id, i) % self.num_slots for i in range(self.num_virtual_servers)]}")

    def remove_server(self, server_id):
        self.servers.remove(server_id)
        for i in range(self.num_virtual_servers):
            virtual_server_id = self.virtual_server_hash_function(server_id, i) % self.num_slots
            del self.virtual_servers[virtual_server_id]
            self.slots[virtual_server_id] = None
        print(f"Removed server: {server_id}")

    def get_server(self, key):
        hash_value = self.hash_function(key) % self.num_slots
        while self.slots[hash_value] is None:
            hash_value = (hash_value + 1) % self.num_slots
        print(f"Key: {key}, Hash Value: {hash_value}, Server: {self.slots[hash_value]}")
        return self.slots[hash_value]

    @staticmethod
    def hash_function(key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def virtual_server_hash_function(self, server_id, i):
        return self.hash_function(f"{server_id}-{i}")
