#!/usr/bin/env python3
"""
Test suite that runs against the test server (port 9877)
instead of the real Blender server (port 9876)
"""

import json
import socket
import time
import sys

HOST = 'localhost'
PORT = 9877  # Test server port

def send_command(command_type, params=None):
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
        sock.connect((HOST, PORT))
        
        command_json = json.dumps(command)
        sock.sendall(command_json.encode('utf-8'))
        
        response_data = b''
        start_time = time.time()
        while time.time() - start_time < 5.0:
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
                "message": f"Connection refused. Is the test server running on {HOST}:{PORT}?"
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

def test_command(name, command_type, params=None):
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
        return False

def main():
    """Run test suite against test server"""
    print("="*70)
    print("TEST SUITE - Testing Against Test Server (Port 9877)")
    print("="*70)
    print(f"\nTesting server at {HOST}:{PORT}")
    print("This is a simulated server - no Blender required!\n")
    
    # Test connection
    print("Testing connection...")
    test_response = send_command("get_scene_info")
    if test_response.get("status") != "success":
        print(f"\n❌ Cannot connect: {test_response.get('error', {}).get('message', 'Unknown error')}")
        print("\nMake sure test_server.py is running:")
        print("  python3 test_server.py")
        return 1
    
    print("✅ Test server is running and responding!\n")
    
    # Test commands
    tests = [
        ("Get Scene Info", "get_scene_info"),
        ("Execute Code", "execute_code", {"code": "print('Test')"}),
        ("Get Timeline Info", "get_timeline_info"),
        ("Set Current Frame", "set_current_frame", {"frame": 10}),
        ("Create Primitive", "create_primitive", {
            "type": "MESH_CUBE",
            "name": "TestCube",
            "location": [0, 0, 0]
        }),
        ("Get Object Info", "get_object_info", {"name": "TestCube"}),
        ("Create Armature", "create_armature", {
            "name": "TestArmature",
            "location": [0, 0, 0]
        }),
        ("Get Armature Info", "get_armature_info", {"armature_name": "TestArmature"}),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests, 1):
        if len(test) == 2:
            name, cmd_type = test
            params = None
        else:
            name, cmd_type, params = test
        
        print(f"[{i}/{len(tests)}] ", end="")
        success = test_command(name, cmd_type, params)
        results.append((name, success))
        
        if success:
            passed += 1
        else:
            failed += 1
        
        time.sleep(0.2)
    
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
    
    print("\n" + "="*70)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"⚠️  {failed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
