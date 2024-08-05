import matplotlib.pyplot as plt
import random

# Simulate request distribution
def simulate_requests(num_requests=1000, servers=None):
    if servers is None:
        servers = ['Server1', 'Server2', 'Server3', 'Server4']
    
    distribution = {f"{server}_{i}": 0 for server in servers for i in range(9)}
    
    for _ in range(num_requests):
        request_id = random.randint(1, 100000)
        virtual_server = hash_function(request_id, servers)
        distribution[virtual_server] += 1
    
    return distribution

def hash_function(request_id, servers):
    num_slots = len(servers) * 9
    server_idx = request_id % len(servers)
    virtual_server_idx = (request_id // len(servers)) % 9
    return f"{servers[server_idx]}_{virtual_server_idx}"

def aggregate_by_server(distribution):
    server_counts = {}
    for virtual_server, count in distribution.items():
        real_server = virtual_server.split('_')[0]
        if real_server in server_counts:
            server_counts[real_server] += count
        else:
            server_counts[real_server] = count
    return server_counts

def plot_aggregated_distribution(before, after):
    servers = sorted(set(before.keys()).union(set(after.keys())))
    counts_before = [before.get(server, 0) for server in servers]
    counts_after = [after.get(server, 0) for server in servers]

    x = range(len(servers))
    
    plt.figure(figsize=(10, 6))
    plt.bar(x, counts_before, width=0.4, label='Before Adding Server', align='center')
    plt.bar([p + 0.4 for p in x], counts_after, width=0.4, label='After Adding Server', align='center')

    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Across Real Servers')
    plt.xticks([p + 0.2 for p in x], servers)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    print("Simulating requests before adding new server...")
    servers_before = ['Server1', 'Server2', 'Server3']
    distribution_before = simulate_requests(1000, servers_before)
    print("Distribution before adding new server:", distribution_before)
    
    print("Simulating requests after adding new server...")
    servers_after = ['Server1', 'Server2', 'Server3', 'Server4']
    distribution_after = simulate_requests(1000, servers_after)
    print("Distribution after adding new server:", distribution_after)
    
    # Aggregate counts by real server
    aggregated_before = aggregate_by_server(distribution_before)
    aggregated_after = aggregate_by_server(distribution_after)
    
    # Plot aggregated distribution
    plot_aggregated_distribution(aggregated_before, aggregated_after)
