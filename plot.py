import requests
import matplotlib.pyplot as plt
from collections import defaultdict

# Base URL for the load balancer
base_url = 'http://localhost:4001'
num_requests = 100  # Number of requests to send

def send_requests():
    """ Send requests to the load balancer and record results """
    server_counts = defaultdict(int)
    for _ in range(num_requests):
        response = requests.post(f'{base_url}/route', json={'Rid': _})
        if response.ok:
            server = response.json().get('server')
            server_counts[server] += 1
        else:
            print(f"Request failed: {response.text}")
    return server_counts

def plot_results(server_counts):
    """ Plot the distribution of requests across servers """
    servers = list(server_counts.keys())
    counts = list(server_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(servers, counts, color='skyblue')
    plt.xlabel('Server')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Across Servers')
    plt.show()

def main():
    # Send requests and collect data
    server_counts = send_requests()

    # Print results
    print("Request distribution:")
    for server, count in server_counts.items():
        print(f"{server}: {count}")

    # Plot results
    plot_results(server_counts)

if __name__ == '__main__':
    main()
