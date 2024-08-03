import requests
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Configuration
load_balancer_url = 'http://localhost:4001/forward'  # Update if necessary
num_requests = 1000

# Variables to store the results
responses = []

def send_requests(num):
    for _ in range(num):
        try:
            response = requests.get(load_balancer_url)
            data = response.json()
            server_id = data.get('server_id', 'Unknown')
            responses.append(server_id)
        except requests.RequestException as e:
            print(f"Request failed: {e}")

def analyze_results():
    # Count the occurrences of each server ID
    counter = Counter(responses)
    
    # Create a DataFrame for better handling
    df = pd.DataFrame(counter.items(), columns=['Server', 'Count'])
    df = df.sort_values(by='Count', ascending=False)
    
    return df

def plot_results(df):
    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.bar(df['Server'], df['Count'], color='skyblue')
    plt.xlabel('Server ID')
    plt.ylabel('Request Count')
    plt.title('Request Distribution Across Servers')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Starting load balancer testing...")
    send_requests(num_requests)
    
    print("Analyzing results...")
    results_df = analyze_results()
    
    print("Summary of request distribution:")
    print(results_df)
    
    print("Generating visualization...")
    plot_results(results_df)
