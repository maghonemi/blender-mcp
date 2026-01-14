#!/usr/bin/env python3
"""Quick script to check if MCP server is running"""

import socket

def check_server(host='localhost', port=9876):
    """Check if server is running"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

if __name__ == "__main__":
    print("Checking MCP server status...")
    if check_server():
        print("✅ Server is running on port 9876")
        print("\nYou can now run:")
        print("  python3 test_all_commands.py")
    else:
        print("❌ Server is NOT running")
        print("\nTo start the server:")
        print("1. Open Blender")
        print("2. Enable the 'Blender MCP' addon")
        print("3. Open the 3D Viewport sidebar (N key)")
        print("4. Click the 'BlenderMCP' tab")
        print("5. Click 'Connect to MCP server'")
        print("\nThen run the test again:")
