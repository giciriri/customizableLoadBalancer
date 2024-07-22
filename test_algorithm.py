import requests
import collections
import matplotlib.pyplot as plt
import time

# Test that the algorithm is working
print("Testing algorithm...")

# Send a large number of requests to the load balancer
requests_sent = 10

rid_values = [i for i in range(requests_sent)]
server_counts = collections.defaultdict(int)

for rid in rid_values:
    print(f"Sending request {rid}...")
    start_time = time.time()
    response = requests.post('http://localhost:4001/route', json={'Rid': rid})
    end_time = time.time()
    print(f"Request {rid} took {end_time - start_time:.2f} seconds")
    server = response.json()['server']
    server_counts[server] += 1

# Print the distribution of requests across virtual servers
print("Distribution of requests across virtual servers:")
for server, count in server_counts.items():
    print(f"Server {server}: {count} requests ({count/requests_sent*100:.2f}%)")

# Create a bar chart showing the distribution of requests
servers = list(server_counts.keys())
request_counts = list(server_counts.values())
plt.bar(servers, request_counts)
plt.xlabel('Server ID')
plt.ylabel('Number of Requests')
plt.title('Distribution of Requests Across Virtual Servers')
plt.show()

# Verify that the distribution is relatively even
max_deviation = 0.1  # 10% deviation from uniform distribution
uniform_distribution = requests_sent / len(server_counts)
for server, count in server_counts.items():
    deviation = abs(count - uniform_distribution) / uniform_distribution
    assert deviation < max_deviation, f"Server {server} has a deviation of {deviation:.2f} from uniform distribution"

print("Algorithm test passed!")