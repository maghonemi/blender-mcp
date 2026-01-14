#!/usr/bin/env python3
"""
Comprehensive test suite for all MCP commands
Tests all available handlers and commands
"""

import json
import socket
import time
import sys
import os

HOST = 'localhost'
PORT = 9876  # Blender MCP server port

def send_command(command_type, params=None):
    """Send a command to the MCP server"""
    if params is None:
        params = {}
    
    command = {
        "type": command_type,
        "params": params
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((HOST, PORT))
        
        command_json = json.dumps(command)
        sock.sendall(command_json.encode('utf-8'))
        
        response_data = b''
        start_time = time.time()
        while time.time() - start_time < 10.0:
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
                "error": {
                    "code": "PARSE_ERROR",
                    "message": f"Failed to parse response: {str(e)}"
                }
            }
    
    except ConnectionRefusedError:
        return {
            "status": "error",
            "error": {
                "code": "CONNECTION_REFUSED",
                "message": f"Connection refused. Is the server running on {HOST}:{PORT}?"
            }
        }
    except socket.timeout:
        return {
            "status": "error",
            "error": {
                "code": "TIMEOUT",
                "message": "Connection timeout"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": {
                "code": "UNKNOWN_ERROR",
                "message": str(e)
            }
        }

def test_command(name, command_type, params=None, expected_status="success"):
    """Test a single command"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"Command: {command_type}")
    if params:
        params_str = json.dumps(params, indent=2)
        if len(params_str) > 200:
            params_str = params_str[:200] + "..."
        print(f"Params: {params_str}")
    print(f"{'='*70}")
    
    response = send_command(command_type, params)
    
    status = response.get("status", "unknown")
    error = response.get("error", {})
    message = response.get("message", "")
    
    if status == "success":
        result = response.get("result", {})
        print(f"✅ SUCCESS")
        if isinstance(result, dict):
            keys = list(result.keys())[:10]
            print(f"   Result keys: {keys}")
            if len(result) > 10:
                print(f"   ... and {len(result) - 10} more")
        elif isinstance(result, str):
            print(f"   Result: {result[:200]}")
        return True
    elif status == "error":
        print(f"❌ ERROR")
        if isinstance(error, dict):
            print(f"   Code: {error.get('code', 'UNKNOWN')}")
            print(f"   Message: {error.get('message', message or str(error))}")
        else:
            print(f"   Error: {error if error else message}")
        return False
    else:
        print(f"⚠️  UNKNOWN STATUS: {status}")
        print(f"   Response: {json.dumps(response, indent=2)[:500]}")
        return False

def main():
    """Run comprehensive test suite"""
    print("="*70)
    print("COMPREHENSIVE MCP COMMAND TEST SUITE")
    print("="*70)
    print(f"\nTesting server at {HOST}:{PORT}")
    print("Make sure Blender is running with the MCP server started!\n")
    
    # Test connection first
    print("Testing connection...")
    test_response = send_command("get_scene_info")
    if test_response.get("status") != "success":
        print(f"\n❌ Cannot connect to server: {test_response.get('error', {}).get('message', 'Unknown error')}")
        print("\nMake sure:")
        print("1. Blender is running")
        print("2. The addon is enabled")
        print("3. The server is started (click 'Connect to MCP server')")
        return 1
    
    print("✅ Server is running and responding!\n")
    
    # Get scene info to find available objects
    scene_info = send_command("get_scene_info")
    available_objects = []
    test_cube_name = None
    
    if scene_info.get("status") == "success":
        objects = scene_info.get("result", {}).get("objects", [])
        available_objects = [obj.get("name") for obj in objects[:10]]
        print(f"Available objects in scene: {available_objects[:5]}")
    
    # Comprehensive test suite
    tests = []
    
    # ========== SCENE COMMANDS ==========
    tests.append(("Get Scene Info", "get_scene_info"))
    tests.append(("Execute Code", "execute_code", {"code": "print('Test from MCP')"}))
    
    # Create test objects
    tests.append(("Create Test Cube", "create_primitive", {
        "type": "MESH_CUBE",
        "name": "MCP_TestCube",
        "location": [0, 0, 0]
    }))
    
    tests.append(("Create Test Sphere", "create_primitive", {
        "type": "MESH_SPHERE",
        "name": "MCP_TestSphere",
        "location": [3, 0, 0]
    }))
    
    # Object operations
    tests.append(("Get Object Info", "get_object_info", {"name": "MCP_TestCube"}))
    
    tests.append(("Get Viewport Screenshot", "get_viewport_screenshot", {
        "filepath": "/tmp/mcp_test_screenshot.png",
        "max_size": 400
    }))
    
    # ========== ANIMATION COMMANDS ==========
    tests.append(("Set Current Frame", "set_current_frame", {"frame": 1}))
    tests.append(("Get Timeline Info", "get_timeline_info"))
    
    tests.append(("Set Frame Range", "set_frame_range", {
        "frame_start": 1,
        "frame_end": 100
    }))
    
    # Keyframe operations
    tests.append(("Create Keyframe - Location", "create_keyframe", {
        "object_name": "MCP_TestCube",
        "data_path": "location",
        "frame": 1,
        "value": [0, 0, 0]
    }))
    
    tests.append(("Create Keyframe - Location X", "create_keyframe", {
        "object_name": "MCP_TestCube",
        "data_path": "location.x",
        "frame": 25,
        "value": 5.0
    }))
    
    tests.append(("Get Keyframes", "get_keyframes", {
        "object_name": "MCP_TestCube",
        "data_path": "location"
    }))
    
    tests.append(("Create Keyframe - Scale", "create_keyframe", {
        "object_name": "MCP_TestCube",
        "data_path": "scale",
        "frame": 50,
        "value": [2.0, 2.0, 2.0]
    }))
    
    # ========== RIGGING COMMANDS ==========
    tests.append(("Create Armature", "create_armature", {
        "name": "MCP_TestArmature",
        "location": [0, 5, 0]
    }))
    
    tests.append(("Get Armature Info", "get_armature_info", {
        "armature_name": "MCP_TestArmature"
    }))
    
    tests.append(("Create Bone", "create_bone", {
        "armature_name": "MCP_TestArmature",
        "bone_name": "Bone",
        "head": [0, 0, 0],
        "tail": [0, 1, 0]
    }))
    
    tests.append(("Get Bone Info", "get_bone_info", {
        "armature_name": "MCP_TestArmature",
        "bone_name": "Bone"
    }))
    
    # ========== MODELING COMMANDS ==========
    tests.append(("Extrude Mesh", "extrude_mesh", {
        "object_name": "MCP_TestCube",
        "mode": "FACE"
    }))
    
    # Run all tests
    results = []
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests, 1):
        if len(test) == 2:
            name, cmd_type = test
            params = None
        else:
            name, cmd_type, params = test
        
        print(f"\n[{i}/{len(tests)}] ", end="")
        success = test_command(name, cmd_type, params)
        results.append((name, success))
        
        if success:
            passed += 1
        else:
            failed += 1
        
        time.sleep(0.3)  # Small delay between tests
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    print(f"\nTotal Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
    
    print("\n" + "-"*70)
    print("Detailed Results:")
    print("-"*70)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    # Group by category
    print("\n" + "-"*70)
    print("Results by Category:")
    print("-"*70)
    
    categories = {
        "Scene": ["Get Scene Info", "Execute Code", "Get Object Info", "Get Viewport Screenshot"],
        "Modeling": ["Create Test Cube", "Create Test Sphere", "Extrude Mesh"],
        "Animation": ["Set Current Frame", "Get Timeline Info", "Set Frame Range", "Create Keyframe", "Get Keyframes"],
        "Rigging": ["Create Armature", "Get Armature Info", "Create Bone", "Get Bone Info"]
    }
    
    for category, command_names in categories.items():
        category_results = [r for r in results if any(name in r[0] for name in command_names)]
        category_passed = sum(1 for _, success in category_results if success)
        category_total = len(category_results)
        print(f"\n{category}: {category_passed}/{category_total} passed")
    
    print("\n" + "="*70)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"⚠️  {failed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
