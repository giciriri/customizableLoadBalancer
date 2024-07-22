import requests

# Test the route endpoint
rid = 123
response = requests.post('http://localhost:4001/route', json={'Rid': rid})
print(f"Route for Rid {rid}: {response.json()['server']}")

# Test adding a server
sid = 4
response = requests.post(f'http://localhost:4001/add_server/{sid}')
print(f"Added server {sid}: {response.text}")

# Test removing a server
sid = 2
response = requests.delete(f'http://localhost:4001/remove_server/{sid}')
print(f"Removed server {sid}: {response.text}")

# Test the route endpoint again
rid = 456
response = requests.post('http://localhost:4001/route', json={'Rid': rid})
print(f"Route for Rid {rid}: {response.json()['server']}")