#!/usr/bin/env python3
"""
Test client to connect to the test server and run commands
"""

import json
import socket
import sys
import time

HOST = 'localhost'
PORT = 9877  # Test server port

def send_command(command_type, params=None, port=9877):
    """Send a command to the test server"""
    if params is None:
        params = {}
    
    command = {
        "type": command_type,
        "params": params
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((HOST, port))
        
        command_json = json.dumps(command)
        sock.sendall(command_json.encode('utf-8'))
        
        response_data = b''
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            response_data += chunk
            try:
                json.loads(response_data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                time.sleep(0.1)
                continue
        
        sock.close()
        
        try:
            response = json.loads(response_data.decode('utf-8'))
            return response
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Failed to parse response: {str(e)}"
            }
    
    except ConnectionRefusedError:
        return {
            "status": "error",
            "message": f"Connection refused. Is the test server running on port {port}?"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }

def main():
    """Test various commands"""
    print("="*60)
    print("Test Client - Connecting to Test Server")
    print("="*60)
    
    # Test connection
    print("\n1. Testing connection...")
    response = send_command("get_scene_info")
    print(f"   Response: {json.dumps(response, indent=2)[:200]}")
    
    if response.get("status") != "success":
        print(f"\n❌ Cannot connect: {response.get('message')}")
        print("\nMake sure test_server.py is running:")
        print("  python3 test_server.py")
        return 1
    
    print("✅ Connected successfully!\n")
    
    # Test commands
    tests = [
        ("get_scene_info", {}),
        ("get_timeline_info", {}),
        ("create_primitive", {"type": "MESH_CUBE", "name": "TestCube", "location": [0, 0, 0]}),
        ("get_object_info", {"name": "TestCube"}),
    ]
    
    print("2. Testing commands:\n")
    for i, (cmd, params) in enumerate(tests, 1):
        print(f"   {i}. {cmd}")
        response = send_command(cmd, params)
        status = response.get("status", "unknown")
        if status == "success":
            print(f"      ✅ Success")
        else:
            error = response.get("error", {})
            if isinstance(error, dict):
                print(f"      ❌ Error: {error.get('code', 'UNKNOWN')} - {error.get('message', str(error))}")
            else:
                print(f"      ❌ Error: {error}")
        time.sleep(0.2)
    
    print("\n" + "="*60)
    print("Test complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
