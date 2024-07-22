import requests
import time

# Base URL for the load balancer
base_url = 'http://localhost:4001'

def test_route_request(rid):
    """ Test routing a request to the load balancer """
    response = requests.post(f'{base_url}/route', json={'Rid': rid})
    if response.ok:
        server = response.json().get('server')
        print(f"Route for Rid {rid}: {server}")
    else:
        print(f"Failed to route Rid {rid}: {response.text}")

def test_add_server(sid):
    """ Test adding a new server """
    response = requests.post(f'{base_url}/add_server/{sid}')
    if response.ok:
        print(f"Added server {sid}: {response.text}")
    else:
        print(f"Failed to add server {sid}: {response.text}")

def test_remove_server(sid):
    """ Test removing an existing server """
    response = requests.delete(f'{base_url}/remove_server/{sid}')
    if response.ok:
        print(f"Removed server {sid}: {response.text}")
    else:
        print(f"Failed to remove server {sid}: {response.text}")

def main():
    # Initial routing test
    print("Initial routing tests:")
    test_route_request(123)
    test_route_request(456)

    # Add a new server and test routing
    print("\nAdding a new server and testing routing:")
    test_add_server(4)
    time.sleep(2)  # Wait for a moment to ensure the server is added
    test_route_request(123)
    test_route_request(456)

    # Remove a server and test routing
    print("\nRemoving an existing server and testing routing:")
    test_remove_server(2)
    time.sleep(2)  # Wait for a moment to ensure the server is removed
    test_route_request(123)
    test_route_request(456)

if __name__ == '__main__':
    main()
