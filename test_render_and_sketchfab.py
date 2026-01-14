#!/usr/bin/env python3
"""
Test script for render output and Sketchfab handlers
"""

import socket
import json
import time

HOST = 'localhost'
PORT = 9876

def send_command(command):
    """Send a command to the Blender MCP server"""
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((HOST, PORT))
        
        # Send command
        command_json = json.dumps(command)
        sock.sendall(command_json.encode('utf-8'))
        
        # Receive response
        response_data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
            try:
                # Try to parse JSON to see if we have complete response
                json.loads(response_data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                continue
        
        sock.close()
        
        # Parse response
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

def test_render_output():
    """Test render output handler"""
    print("\n" + "="*60)
    print("Testing Render Output Handler")
    print("="*60)
    
    # Test 1: Get current render settings
    print("\n1. Getting current render settings...")
    command = {
        "type": "get_render_settings",
        "params": {}
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    if response.get('status') == 'success':
        result = response.get('result', {})
        print(f"   Current output path: {result.get('output_path', 'N/A')}")
        print(f"   Current format: {result.get('file_format', 'N/A')}")
        print(f"   Engine: {result.get('engine', 'N/A')}")
        print(f"   Resolution: {result.get('resolution', 'N/A')}")
    else:
        error = response.get('error', {})
        print(f"   Error: {error.get('message', 'Unknown error')}")
        return False
    
    # Test 2: Set render output to a writable location
    print("\n2. Setting render output to /tmp/blender_test_renders/...")
    command = {
        "type": "set_render_output",
        "params": {
            "filepath": "/tmp/blender_test_renders/",
            "file_format": "PNG",
            "color_mode": "RGB",
            "color_depth": "8"
        }
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    if response.get('status') == 'success':
        result = response.get('result', {})
        print(f"   ✓ Render output set successfully")
        print(f"   New output path: {result.get('filepath', 'N/A')}")
        print(f"   New format: {result.get('file_format', 'N/A')}")
        return True
    else:
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown error')}")
        if error.get('code'):
            print(f"   Error code: {error.get('code')}")
        return False

def test_sketchfab_status():
    """Test Sketchfab status handler"""
    print("\n" + "="*60)
    print("Testing Sketchfab Integration")
    print("="*60)
    
    # Test 1: Get Sketchfab status
    print("\n1. Getting Sketchfab status...")
    command = {
        "type": "get_sketchfab_status",
        "params": {}
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    
    if response.get('status') == 'success':
        result = response.get('result', {})
        enabled = result.get('enabled', False)
        message = result.get('message', 'No message')
        print(f"   Enabled: {enabled}")
        print(f"   Message: {message}")
        
        if not enabled:
            print("\n   ⚠ Sketchfab is not enabled or API key not configured")
            print("   To enable:")
            print("   1. Open BlenderMCP panel in Blender (N key)")
            print("   2. Check 'Use assets from Sketchfab'")
            print("   3. Enter your Sketchfab API key")
            print("   4. Restart Blender")
            return False
        else:
            print("   ✓ Sketchfab is enabled and ready")
            return True
    else:
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown error')}")
        if error.get('code'):
            print(f"   Error code: {error.get('code')}")
        
        # Check if handler is registered
        if "not found" in error.get('message', '').lower() or "not registered" in error.get('message', '').lower():
            print("\n   ⚠ Sketchfab handler may not be registered")
            print("   Make sure handlers/integrations/sketchfab.py exists")
            print("   and is imported in handlers/handler_registry.py")
        
        return False

def test_sketchfab_search():
    """Test Sketchfab search (only if enabled)"""
    print("\n2. Testing Sketchfab search (if enabled)...")
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
        results = result.get('results', [])
        print(f"   ✓ Found {len(results)} models")
        if results:
            print(f"   First result: {results[0].get('name', 'N/A')}")
            print(f"   UID: {results[0].get('uid', 'N/A')}")
        return True
    else:
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown error')}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Blender MCP - Render Output & Sketchfab Test")
    print("="*60)
    print(f"\nConnecting to Blender MCP server at {HOST}:{PORT}")
    print("Make sure Blender is running with the addon enabled!")
    
    # Wait a moment for connection
    time.sleep(1)
    
    results = []
    
    # Test render output
    results.append(("Render Output", test_render_output()))
    
    # Test Sketchfab
    status_ok = test_sketchfab_status()
    results.append(("Sketchfab Status", status_ok))
    
    if status_ok:
        results.append(("Sketchfab Search", test_sketchfab_search()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:30} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check the output above for details.")

if __name__ == "__main__":
    main()
