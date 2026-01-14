#!/usr/bin/env python3
"""
Test script to list all registered commands
"""

import socket
import json

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
        return {"status": "error", "error": {"message": str(e)}}

def main():
    print("="*60)
    print("Testing Blender MCP Server Connection")
    print("="*60)
    
    # Test basic connection
    print("\n1. Testing basic connection with get_scene_info...")
    command = {
        "type": "get_scene_info",
        "params": {}
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    if response.get('status') == 'success':
        print("   ✓ Server is responding")
    else:
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown')}")
        return
    
    # Test render output
    print("\n2. Testing get_render_settings...")
    command = {
        "type": "get_render_settings",
        "params": {}
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    if response.get('status') == 'success':
        print("   ✓ Render settings handler is registered")
        result = response.get('result', {})
        print(f"   Current output: {result.get('output_path', 'N/A')}")
    else:
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown')}")
        print(f"   Code: {error.get('code', 'N/A')}")
        if "not found" in error.get('message', '').lower():
            print("\n   ⚠ Handler not registered. Possible reasons:")
            print("   1. Blender needs to be restarted to load new handlers")
            print("   2. Modular system not loaded properly")
            print("   3. Handler registry not called during addon registration")
    
    # Test Sketchfab
    print("\n3. Testing get_sketchfab_status...")
    command = {
        "type": "get_sketchfab_status",
        "params": {}
    }
    response = send_command(command)
    print(f"   Status: {response.get('status', 'unknown')}")
    if response.get('status') == 'success':
        print("   ✓ Sketchfab handler is registered")
        result = response.get('result', {})
        print(f"   Enabled: {result.get('enabled', False)}")
    else:
        error = response.get('error', {})
        print(f"   ✗ Error: {error.get('message', 'Unknown')}")
        print(f"   Code: {error.get('code', 'N/A')}")
        if "not found" in error.get('message', '').lower():
            print("\n   ⚠ Handler not registered. Check:")
            print("   1. handlers/integrations/sketchfab.py exists")
            print("   2. Handler is imported in handlers/handler_registry.py")
            print("   3. Blender was restarted after adding handlers")
    
    print("\n" + "="*60)
    print("Troubleshooting:")
    print("="*60)
    print("If handlers are not found:")
    print("1. Make sure Blender is fully restarted (not just addon reload)")
    print("2. Check Blender console for 'All handlers registered successfully' message")
    print("3. Verify handlers/rendering/render_settings.py exists")
    print("4. Verify handlers/integrations/sketchfab.py exists")
    print("5. Check that handlers/handler_registry.py imports them correctly")

if __name__ == "__main__":
    main()
