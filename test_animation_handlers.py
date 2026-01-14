#!/usr/bin/env python3
"""
Test script for Blender MCP Animation Handlers
Tests animation functionality using MCP handlers instead of raw code execution
"""

import socket
import json
import time

def send_command(command_type, params=None):
    """Send a command to the Blender MCP server"""
    if params is None:
        params = {}
    
    command = {
        "type": command_type,
        "params": params
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect(('localhost', 9876))
        
        # Send command (no newline)
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
            "message": "Connection refused - Is Blender MCP server running?"
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

def test_command(name, command_type, params=None, expected_key=None):
    """Test a single command"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"Command: {command_type}")
    if params:
        print(f"Params: {json.dumps(params, indent=2)}")
    
    response = send_command(command_type, params)
    
    if response.get("status") == "success":
        print(f"✅ PASSED")
        if "result" in response:
            result = response["result"]
            if expected_key and expected_key in result:
                print(f"   {expected_key}: {result[expected_key]}")
            elif isinstance(result, dict):
                # Print first few keys
                keys = list(result.keys())[:5]
                for key in keys:
                    print(f"   {key}: {result[key]}")
        return True
    elif response.get("status") == "error":
        print(f"❌ FAILED")
        error = response.get("error", {})
        message = response.get("message", "")
        if isinstance(error, dict):
            print(f"   Error: {error.get('message', message)}")
        else:
            print(f"   Error: {message or str(error)}")
        return False
    else:
        print(f"⚠️  UNEXPECTED RESPONSE: {json.dumps(response, indent=2)[:200]}")
        return False

def main():
    print("="*60)
    print("BLENDER MCP ANIMATION HANDLERS TEST")
    print("="*60)
    print("\nTesting animation functionality using MCP handlers...")
    
    results = []
    
    # Test 1: Get Scene Info
    results.append(("Get Scene Info", test_command(
        "Get Scene Info",
        "get_scene_info"
    )))
    time.sleep(0.2)
    
    # Get a test object name from scene
    scene_response = send_command("get_scene_info")
    test_object = "Cube"  # Default
    if scene_response.get("status") == "success":
        objects = scene_response.get("result", {}).get("objects", [])
        mesh_objects = [obj for obj in objects if obj.get("type") == "MESH"]
        if mesh_objects:
            test_object = mesh_objects[0].get("name", "Cube")
    
    print(f"\nUsing test object: {test_object}")
    time.sleep(0.2)
    
    # Test 2: Set Timeline
    results.append(("Set Timeline", test_command(
        "Set Timeline",
        "set_frame_range",
        {"frame_start": 1, "frame_end": 120}
    )))
    time.sleep(0.2)
    
    # Test 3: Set Current Frame
    results.append(("Set Current Frame", test_command(
        "Set Current Frame",
        "set_current_frame",
        {"frame": 1}
    )))
    time.sleep(0.2)
    
    # Test 4: Get Timeline Info
    results.append(("Get Timeline Info", test_command(
        "Get Timeline Info",
        "get_timeline_info"
    )))
    time.sleep(0.2)
    
    # Test 5: Create Keyframe (location at frame 1)
    results.append(("Create Keyframe (frame 1)", test_command(
        "Create Keyframe at frame 1",
        "create_keyframe",
        {
            "object_name": test_object,
            "data_path": "location",
            "frame": 1,
            "value": [3, 0, 0]
        }
    )))
    time.sleep(0.2)
    
    # Test 6: Create Keyframe (location at frame 60)
    results.append(("Create Keyframe (frame 60)", test_command(
        "Create Keyframe at frame 60",
        "create_keyframe",
        {
            "object_name": test_object,
            "data_path": "location",
            "frame": 60,
            "value": [3, 3, 2]
        }
    )))
    time.sleep(0.2)
    
    # Test 7: Create Keyframe (location at frame 120)
    results.append(("Create Keyframe (frame 120)", test_command(
        "Create Keyframe at frame 120",
        "create_keyframe",
        {
            "object_name": test_object,
            "data_path": "location",
            "frame": 120,
            "value": [3, 0, 0]
        }
    )))
    time.sleep(0.2)
    
    # Test 8: Get Keyframes
    results.append(("Get Keyframes", test_command(
        "Get Keyframes",
        "get_keyframes",
        {
            "object_name": test_object,
            "data_path": "location"
        },
        expected_key="keyframes"
    )))
    time.sleep(0.2)
    
    # Test 9: Get FCurves
    results.append(("Get FCurves", test_command(
        "Get FCurves",
        "get_fcurves",
        {
            "object_name": test_object
        }
    )))
    time.sleep(0.2)
    
    # Test 10: Get Action Info
    results.append(("Get Action Info", test_command(
        "Get Action Info",
        "get_object_action",
        {
            "object_name": test_object
        }
    )))
    time.sleep(0.2)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All animation handler tests PASSED!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
