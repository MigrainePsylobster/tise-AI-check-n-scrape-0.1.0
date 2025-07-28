import requests
import json

print("Testing user API directly...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en,en;q=0.9',
    'sec-ch-ua-platform': '"Windows"',
    'tise-system-os': 'web',
    'Referer': 'https://tise.com/joy_will_be_sparked',
}

url = "https://tise.com/api/users/joy_will_be_sparked"
print(f"Testing URL: {url}")

try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            print(f"User ID: {data.get('id', 'NOT FOUND')}")
        except json.JSONDecodeError:
            print("Response is not valid JSON")
            print(f"Raw response: {response.text[:500]}")
    else:
        print(f"Error response: {response.text[:500]}")
        
except Exception as e:
    print(f"Request failed: {e}")
