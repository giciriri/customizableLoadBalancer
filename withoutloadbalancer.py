import requests
import random
import matplotlib.pyplot as plt

# Define the server URLs
servers = [
    'http://localhost:5001/home',  # URL for server 1
    'http://localhost:5002/home',  # URL for server 2
    'http://localhost:5003/home'   # URL for server 3
]

# Simulate server failures
failed_servers = set()  # Keep track of failed servers

def simulate_server_failure(server_url):
    if server_url in servers:
        failed_servers.add(server_url)

def restore_server(server_url):
    if server_url in failed_servers:
        failed_servers.remove(server_url)

def is_server_available(server_url):
    return server_url not in failed_servers

# Initialize counters for each server
request_counts = {
    'http://localhost:5001/home': 0,
    'http://localhost:5002/home': 0,
    'http://localhost:5003/home': 0
}

def simulate_requests(num_requests):
    fixed_request_ids = range(1, num_requests + 1)  # Fixed set of request IDs
    for request_id in fixed_request_ids:
        available_servers = [server for server in servers if is_server_available(server)]
        if not available_servers:
            print("No servers available to handle requests.")
            break
        server_url = random.choice(available_servers)
        try:
            response = requests.get(server_url, params={'request_id': request_id})
            request_counts[server_url] += 1
        except requests.RequestException as e:
            print(f"Request to {server_url} failed: {e}")

def print_summary():
    print(f"Request counts per server: {request_counts}")

def plot_request_distribution():
    server_urls = list(request_counts.keys())
    counts = list(request_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(server_urls, counts, color='skyblue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Across Servers')
    plt.show()

if __name__ == '__main__':
    # Example: Simulate server 1 failure
    simulate_server_failure('http://localhost:5001/home')

    simulate_requests(10000)  # Simulate 10000 requests
    print_summary()  # Print the summary
    plot_request_distribution()  # Plot the distribution

    # Restore the failed server for further tests
    restore_server('http://localhost:5001/home')
