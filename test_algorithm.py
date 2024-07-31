import random
import matplotlib.pyplot as plt

from consistent_hashing import ConsistentHashMap  # Import your consistent hashing implementation

# Create a consistent hash map with 3 servers and 512 slots
hash_map = ConsistentHashMap(N=3, M=512, K=3)

# Generate 10,00 random user IDs (or requests)
user_ids = [f"user_{random.randint(1, 10000)}" for _ in range(1000)]

# Hash each user ID and store the server ID
server_ids = [hash_map.get_server(user_id) for user_id in user_ids]

# Count the number of user IDs assigned to each server
server_counts = {}
for server_id in server_ids:
    if server_id not in server_counts:
        server_counts[server_id] = 0
    server_counts[server_id] += 1

# Plot the distribution of user IDs across servers
plt.bar(server_counts.keys(), server_counts.values())
plt.xlabel('Server ID')
plt.ylabel('Number of User IDs')
plt.title('Consistent Hashing Distribution')
plt.show()