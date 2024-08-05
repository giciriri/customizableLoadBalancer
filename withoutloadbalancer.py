import requests
import matplotlib.pyplot as plt

# Define the server URLs with labels
servers = {
    "Server1": "http://localhost:5001",
    "Server2": "http://localhost:5002",
    "Server3": "http://localhost:5003"
}

# Define the number of requests to send to each server
requests_per_server = {
    "Server1": 1000,
    "Server2": 2000,
    "Server3": 500
}

# Initialize counters
request_counts = {server: 0 for server in servers}

def simulate_requests():
    for server, url in servers.items():
        num_requests = requests_per_server[server]
        for _ in range(num_requests):
            try:
                response = requests.get(f"{url}/home")
                if response.status_code == 200:
                    request_counts[server] += 1
                else:
                    print(f"Request failed for {server}: {response.status_code}")
            except requests.RequestException as e:
                print(f"Request failed for {server}: {e}")

def print_summary():
    print("Simulated Uneven Load Distribution:")
    for server, count in request_counts.items():
        print(f"{server}: {count} requests")

def plot_distribution():
    servers = list(request_counts.keys())
    counts = list(request_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(servers, counts, color=['blue', 'green', 'red'])
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Without Load Balancer')
    plt.show()

if __name__ == "__main__":
    simulate_requests()
    print_summary()
    plot_distribution()
