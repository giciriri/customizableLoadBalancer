import requests
import random
import matplotlib.pyplot as plt
import time

# Define the server URLs
servers = [
    'http://localhost:5001/home',  # URL for server 1
    'http://localhost:5002/home',  # URL for server 2
    'http://localhost:5003/home'   # URL for server 3
]

# Initialize counters for each server
request_counts = {
    'http://localhost:5001/home': 0,
    'http://localhost:5002/home': 0,
    'http://localhost:5003/home': 0
}

# Function to check if a server is healthy
def is_server_healthy(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to simulate requests with retries
def simulate_requests(num_requests):
    fixed_request_ids = range(1, num_requests + 1)  # Fixed set of request IDs
    for request_id in fixed_request_ids:
        server_url = random.choice(servers)
        # Retry logic
        retries = 3
        while retries > 0:
            if is_server_healthy(server_url):
                try:
                    response = requests.get(server_url, params={'request_id': request_id})
                    if response.status_code == 200:
                        request_counts[server_url] += 1
                        break
                    else:
                        print(f"Request to {server_url} failed with status {response.status_code}")
                        break
                except requests.RequestException as e:
                    print(f"Request to {server_url} failed: {e}")
                    retries -= 1
                    time.sleep(1)  # Wait before retrying
            else:
                print(f"Server {server_url} is not healthy, trying another server.")
                # Choose another server
                servers.remove(server_url)
                if not servers:
                    print("No servers available")
                    break
                server_url = random.choice(servers)
                retries -= 1

def print_summary():
    print(f"Request counts per server: {request_counts}")

def plot_request_distribution():
    server_names = list(request_counts.keys())
    counts = list(request_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(server_names, counts, color='skyblue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Across Servers')
    plt.show()

if __name__ == '__main__':
    simulate_requests(1000)  # Simulate 1000 requests
    print_summary()  # Print the summary
    plot_request_distribution()  # Plot the distribution
