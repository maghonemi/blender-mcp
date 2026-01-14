#!/usr/bin/env python3
"""
Test to see what commands are registered
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
    print("Testing Registered Commands")
    print("="*60)
    
    # Test commands that should work
    test_commands = [
        "get_scene_info",
        "get_object_info",
        "create_keyframe",
        "get_render_settings",
        "set_render_output",
        "get_sketchfab_status",
        "search_sketchfab_models"
    ]
    
    print("\nTesting which commands are registered:\n")
    
    for cmd in test_commands:
        command = {"type": cmd, "params": {}}
        response = send_command(command)
        status = response.get('status', 'unknown')
        
        if status == 'success':
            print(f"✓ {cmd:30} - REGISTERED")
        elif status == 'error':
            error = response.get('error', {})
            error_code = error.get('code', '')
            if error_code == 'INVALID_COMMAND':
                print(f"✗ {cmd:30} - NOT REGISTERED")
            else:
                print(f"⚠ {cmd:30} - REGISTERED (but error: {error.get('message', '')[:50]})")
        else:
            print(f"? {cmd:30} - UNKNOWN STATUS: {status}")
    
    print("\n" + "="*60)
    print("Summary:")
    print("="*60)
    print("If commands show 'NOT REGISTERED', Blender needs to be restarted")
    print("to load the new handlers.")
    print("\nCheck Blender console for:")
    print("  - 'BlenderMCP: Modular system loaded successfully'")
    print("  - 'All handlers registered successfully'")
    print("  - 'Registered X handlers'")

if __name__ == "__main__":
    main()
