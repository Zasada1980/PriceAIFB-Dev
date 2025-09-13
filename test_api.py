#!/usr/bin/env python3
"""
API test script for Market Scout Israel.
"""

import requests
import json
import time
import subprocess
import sys
from threading import Thread


def test_api():
    """Test the API endpoints."""
    base_url = "http://127.0.0.1:8000"
    
    print("=== Testing Market Scout Israel API ===")
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test listings endpoint
        print("\n2. Testing listings endpoint...")
        response = requests.get(f"{base_url}/listings")
        print(f"Status: {response.status_code}")
        listings = response.json()
        print(f"Found {len(listings)} listings")
        if listings:
            print(f"Sample listing: {listings[0]['title']} - {listings[0]['price']} {listings[0]['currency']}")
        
        # Test search endpoint
        print("\n3. Testing search endpoint...")
        response = requests.get(f"{base_url}/search?q=Intel")
        print(f"Status: {response.status_code}")
        search_results = response.json()
        print(f"Found {len(search_results)} results for 'Intel'")
        
        # Test category filter
        print("\n4. Testing category filter...")
        response = requests.get(f"{base_url}/listings?category=cpu")
        print(f"Status: {response.status_code}")
        cpu_listings = response.json()
        print(f"Found {len(cpu_listings)} CPU listings")
        
        # Test city filter
        print("\n5. Testing city filter...")
        response = requests.get(f"{base_url}/listings?city=תל אביב")
        print(f"Status: {response.status_code}")
        city_listings = response.json()
        print(f"Found {len(city_listings)} listings in Tel Aviv")
        
        print("\n✅ All API tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure it's running.")
    except Exception as e:
        print(f"❌ API test failed: {e}")


if __name__ == "__main__":
    test_api()