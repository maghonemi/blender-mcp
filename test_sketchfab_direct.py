#!/usr/bin/env python3
"""
Direct test of Sketchfab handlers
"""

import socket
import json
import time

HOST = 'localhost'
PORT = 9876

def send_command(command):
    """Send a command to the Blender MCP server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((HOST, PORT))
        
        command_json = json.dumps(command)
        sock.sendall(command_json.encode('utf-8'))
        
        response_data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
            try:
                json.loads(response_data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                continue
        
        sock.close()
        response = json.loads(response_data.decode('utf-8'))
        return response
    except Exception as e:
        return {
            "status": "error",
            "error": {
                "code": "CONNECTION_ERROR",
                "message": str(e)
            }
        }

def main():
    print("="*60)
    print("Testing Sketchfab Handlers")
    print("="*60)
    
    # Test 1: Get Sketchfab status
    print("\n1. Testing get_sketchfab_status...")
    command = {
        "type": "get_sketchfab_status",
        "params": {}
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    
    if response.get('status') == 'success':
        result = response.get('result', {})
        print(f"   ✓ Success!")
        print(f"   Enabled: {result.get('enabled', False)}")
        print(f"   Message: {result.get('message', 'N/A')}")
    elif response.get('status') == 'error':
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown error')}")
        print(f"   Code: {error.get('code', 'N/A')}")
    else:
        print(f"   ✗ Unexpected response: {response}")
    
    # Test 2: Search Sketchfab models
    print("\n2. Testing search_sketchfab_models...")
    command = {
        "type": "search_sketchfab_models",
        "params": {
            "query": "chair",
            "count": 5,
            "downloadable": True
        }
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    
    if response.get('status') == 'success':
        result = response.get('result', {})
        if isinstance(result, dict) and 'error' in result:
            print(f"   ✗ Error in result: {result.get('error')}")
        else:
            results = result.get('results', []) if isinstance(result, dict) else []
            print(f"   ✓ Success! Found {len(results)} models")
            if results:
                print(f"   First result: {results[0].get('name', 'N/A')}")
    elif response.get('status') == 'error':
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown error')}")
        print(f"   Code: {error.get('code', 'N/A')}")
        if error.get('suggestions'):
            print(f"   Suggestions: {', '.join(error.get('suggestions', []))}")
    else:
        print(f"   ✗ Unexpected response: {response}")
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)

if __name__ == "__main__":
    main()
