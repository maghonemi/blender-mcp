#!/usr/bin/env python3
"""
Test script to verify all MCP actions at port 9876
Tests all available commands to ensure they work correctly
"""

import json
import socket
import time
import sys

HOST = 'localhost'
PORT = 9876

def send_command(command_type, params=None):
    """Send a command to the MCP server and return the response"""
    if params is None:
        params = {}
    
    command = {
        "type": command_type,
        "params": params
    }
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((HOST, PORT))
        
        # Send command
        command_json = json.dumps(command)
        sock.sendall(command_json.encode('utf-8'))
        
        # Receive response
        response_data = b''
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            response_data += chunk
            # Try to parse - if successful, we're done
            try:
                json.loads(response_data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                # Incomplete JSON, wait for more
                time.sleep(0.1)
                continue
        
        sock.close()
        
        # Parse response
        try:
            response = json.loads(response_data.decode('utf-8'))
            return response
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Failed to parse response: {str(e)}",
                "raw_response": response_data.decode('utf-8', errors='ignore')
            }
    
    except ConnectionRefusedError:
        return {
            "status": "error",
            "message": f"Connection refused. Is the server running on {HOST}:{PORT}?"
        }
    except socket.timeout:
        return {
            "status": "error",
            "message": "Connection timeout"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }

def test_command(name, command_type, params=None):
    """Test a single command and print results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Command: {command_type}")
    if params:
        print(f"Params: {json.dumps(params, indent=2)}")
    print(f"{'='*60}")
    
    response = send_command(command_type, params)
    
    if response.get("status") == "success":
        print(f"✅ SUCCESS")
        result = response.get("result", {})
        if isinstance(result, dict) and result:
            print(f"Result keys: {list(result.keys())[:10]}")  # Show first 10 keys
        elif isinstance(result, str):
            print(f"Result: {result[:200]}")  # First 200 chars
    elif response.get("status") == "error":
        print(f"❌ ERROR")
        error = response.get("error", {})
        message = response.get("message", "")
        
        if isinstance(error, dict):
            print(f"Error code: {error.get('code', 'UNKNOWN')}")
            print(f"Error message: {error.get('message', message or str(error))}")
        elif message:
            print(f"Error message: {message}")
        else:
            print(f"Error: {error if error else 'No error details provided'}")
            print(f"Full response: {json.dumps(response, indent=2)[:500]}")
    else:
        print(f"⚠️  UNKNOWN STATUS: {response.get('status')}")
        print(f"Response: {json.dumps(response, indent=2)[:500]}")
    
    return response.get("status") == "success"

def main():
    """Run all tests"""
    print("="*60)
    print("MCP Server Action Tests")
    print(f"Testing server at {HOST}:{PORT}")
    print("="*60)
    
    # Test connection first
    print("\nTesting connection...")
    test_response = send_command("get_scene_info")
    if test_response.get("status") != "success":
        print(f"❌ Cannot connect to server: {test_response.get('message')}")
        print("\nMake sure:")
        print("1. Blender is running")
        print("2. The addon is enabled")
        print("3. The server is started (click 'Connect to MCP server')")
        return 1
    
    print("✅ Server is running and responding!")
    
    # First, get scene info to find available objects
    scene_info = send_command("get_scene_info")
    available_objects = []
    if scene_info.get("status") == "success":
        objects = scene_info.get("result", {}).get("objects", [])
        available_objects = [obj.get("name") for obj in objects[:5]]  # Get first 5 object names
        print(f"\nAvailable objects in scene: {available_objects}")
    
    # Use first available object, or create one if none exist
    test_object_name = available_objects[0] if available_objects else None
    
    # List of commands to test
    tests = [
        # Scene commands
        ("Get Scene Info", "get_scene_info"),
        ("Execute Code", "execute_code", {"code": "print('Hello from MCP!')"}),
        
        # Create a test object first if needed
        ("Create Test Cube", "create_primitive", {
            "type": "MESH_CUBE",
            "name": "TestCube",
            "location": [0, 0, 0]
        }),
        
        # Now test with the created object
        ("Get Object Info", "get_object_info", {"name": "TestCube"}),
        ("Get Viewport Screenshot", "get_viewport_screenshot", {
            "filepath": "/tmp/blender_screenshot.png",
            "max_size": 400
        }),
        
        # Animation commands (use TestCube)
        ("Create Keyframe", "create_keyframe", {
            "object_name": "TestCube",
            "data_path": "location",
            "frame": 1,
            "value": [0, 0, 0]
        }),
        ("Get Keyframes", "get_keyframes", {
            "object_name": "TestCube",
            "data_path": "location"
        }),
        ("Set Current Frame", "set_current_frame", {"frame": 10}),
        ("Get Timeline Info", "get_timeline_info"),
        
        # Rigging commands
        ("Create Armature", "create_armature", {
            "name": "TestArmature",
            "location": [0, 0, 0]
        }),
        ("Get Armature Info", "get_armature_info", {"armature_name": "TestArmature"}),
    ]
    
    results = []
    for test in tests:
        if len(test) == 2:
            name, cmd_type = test
            params = None
        else:
            name, cmd_type, params = test
        
        success = test_command(name, cmd_type, params)
        results.append((name, success))
        time.sleep(0.2)  # Small delay between tests
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
