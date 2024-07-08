import hashlib

class ConsistentHashMap:
    def __init__(self, num_servers, num_slots, virtual_servers_per_server):
        self.num_servers = num_servers  # Number of server containers managed by the load balancer
        self.num_slots = num_slots  # Total number of slots in the consistent hash map
        self.virtual_servers_per_server = virtual_servers_per_server  # Number of virtual servers for each server container

        self.server_containers = [f'S{i}' for i in range(1, num_servers + 1)]
        self.virtual_servers = self.generate_virtual_servers()

        # Initialize the hash map
        self.hash_map = [None] * num_slots

        # Add the initial servers
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

def main():
    # Initialize Consistent Hash Map
    num_servers = 3  # Number of server containers managed by the load balancer
    num_slots = 512  # Total number of slots in the consistent hash map
    virtual_servers_per_server = 5  # Number of virtual servers for each server container

    chm = ConsistentHashMap(num_servers, num_slots, virtual_servers_per_server)

    # Map requests to servers
    requests = [132574, 237891, 982345, 674512, 876234, 543289]
    for request_id in requests:
        server = chm.map_request(request_id)
        print(f"Request {request_id} mapped to server {server}")

    # Simulate server failure
    failed_server = 1
    chm.remove_server(failed_server)
    print(f"Server {failed_server} failed")

    # Map requests again after server failure
    for request_id in requests:
        server = chm.map_request(request_id)
        print(f"Request {request_id} mapped to server {server}")

if __name__ == "__main__":
    main()
