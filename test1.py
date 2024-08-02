import requests
import random
import time
import matplotlib.pyplot as plt

def test_load_balancer(url, num_requests=100):
    counts = {"Server1": 0, "Server2": 0, "Server3": 0}

    for _ in range(num_requests):
        try:
            response = requests.get(f"{url}/forward")
            server_response = response.json().get('message', '')
            # Assume server IDs are included in the response
            if "Server1" in server_response:
                counts["Server1"] += 1
            elif "Server2" in server_response:
                counts["Server2"] += 1
            elif "Server3" in server_response:
                counts["Server3"] += 1
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        time.sleep(random.uniform(0.1, 0.5))  # Random sleep to avoid burst traffic

    return counts

def plot_distribution(counts):
    servers = list(counts.keys())
    request_counts = list(counts.values())

    plt.bar(servers, request_counts, color='skyblue')
    plt.xlabel('Server Instances')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Across Server Instances')
    plt.show()

if __name__ == '__main__':
    url = 'http://localhost:4001'  # Adjust this URL if needed
    results = test_load_balancer(url)
    print(f"Request counts per server: {results}")
    plot_distribution(results)
