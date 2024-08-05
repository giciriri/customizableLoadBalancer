import requests
import matplotlib.pyplot as plt
import numpy as np

def get_available_servers(server_urls):
    """ Check which servers are currently available. """
    available_servers = {}
    for label, url in server_urls.items():
        print(f"Checking {label} at {url}")  # Debugging line
        try:
            response = requests.get(f"{url}/home", timeout=10)
            if response.status_code == 200:
                available_servers[label] = url
            else:
                print(f"{label} responded with status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"{label} is currently unavailable. Error: {e}")
    return available_servers

def simulate_requests(servers, num_requests=1000):
    """ Simulate requests and count distribution to available servers. """
    request_counts = {server: 0 for server in servers}
    
    for _ in range(num_requests):
        server = np.random.choice(list(servers.values()))
        try:
            response = requests.get(f"{server}/home", timeout=5)
            if response.ok:
                server_label = response.json().get('message', 'Unknown').split()[1]
                request_counts[server_label] += 1
        except requests.RequestException as e:
            print(f"Request to {server} failed. Error: {e}")
    
    return request_counts

def plot_distribution(distribution):
    """ Plot the distribution of requests. """
    labels = distribution.keys()
    counts = distribution.values()

    plt.bar(labels, counts)
    plt.xlabel('Server')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution')
    plt.show()

def main():
    server_urls = {
        'Server1': 'http://localhost:5001',
        'Server2': 'http://localhost:5002',
        'Server3': 'http://localhost:5003'
    }
    
    print("Testing with all servers up...")
    available_servers = get_available_servers(server_urls)
    
    if available_servers:
        request_counts = simulate_requests(available_servers)
        print("Request Distribution Summary:")
        for server, count in request_counts.items():
            print(f"{server}: {count} requests")
        plot_distribution(request_counts)
    else:
        print("No servers are available. Test cannot proceed.")
    
    input("Stop a server and press Enter to continue...")

    print("Testing after stopping one server...")
    available_servers = get_available_servers(server_urls)
    
    if available_servers:
        request_counts = simulate_requests(available_servers)
        print("Request Distribution Summary:")
        for server, count in request_counts.items():
            print(f"{server}: {count} requests")
        plot_distribution(request_counts)
    else:
        print("No servers are available. Test cannot proceed.")

if __name__ == "__main__":
    main()
