import random
import matplotlib.pyplot as plt

# Define the number of servers and users
num_servers = 3
num_users = 500

# Define the server IDs
server_ids = [f"S{i+1}_{j}" for i in range(num_servers) for j in range(2)]

# Create a dictionary to store the user IDs assigned to each server
server_user_ids = {server_id: [] for server_id in server_ids}

# Assign user IDs to servers using consistent hashing
for user_id in range(num_users):
  # Generate a random hash value for the user ID
  hash_value = random.random()

  # Find the server ID corresponding to the hash value
  server_id = server_ids[int(hash_value * len(server_ids))]

  # Assign the user ID to the server
  server_user_ids[server_id].append(user_id)

# Plot the distribution of user IDs across servers
plt.figure(figsize=(8, 6))
plt.bar(server_ids, [len(server_user_ids[server_id]) for server_id in server_ids])
plt.xlabel("Server ID")
plt.ylabel("Number of User IDs")
plt.title("Consistent Hashing Distribution")
plt.show()