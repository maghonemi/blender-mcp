#!/usr/bin/env python3
"""
Test server that simulates the Blender MCP server
Can be used to test command handling without Blender running
"""

import json
import socket
import threading
import time
from typing import Dict, Any

# Mock bpy for testing
class MockBpy:
    class data:
        class objects:
            _objects = {}
            @classmethod
            def get(cls, name):
                return cls._objects.get(name)
            @classmethod
            def new(cls, name, obj_type):
                obj = MockObject(name)
                cls._objects[name] = obj
                return obj
        
        class actions:
            _actions = {}
            @classmethod
            def new(cls, name):
                action = MockAction(name)
                cls._actions[name] = action
                return action
        
        objects = objects()
        actions = actions()
    
    class context:
        scene = type('Scene', (), {
            'name': 'Scene',
            'objects': [],
            'frame_current': 1,
            'frame_start': 1,
            'frame_end': 250,
            'fps': 24
        })()
        
        @classmethod
        def active_object(cls):
            return None
    
    class app:
        timers = type('Timers', (), {
            'register': lambda func, first_interval: None
        })()
    
    class ops:
        class mesh:
            @staticmethod
            def primitive_cube_add(location=(0, 0, 0)):
                obj = MockBpy.data.objects.new("Cube", "MESH")
                obj.location = list(location)
                return {'FINISHED'}

class MockObject:
    def __init__(self, name):
        self.name = name
        self.type = "MESH"
        self.location = [0, 0, 0]
        self.rotation_euler = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.animation_data = None
        self.visible = True
        self.materials = []
    
    def animation_data_create(self):
        self.animation_data = MockAnimationData()
        return self.animation_data

class MockAnimationData:
    def __init__(self):
        self.action = None

class MockAction:
    def __init__(self, name):
        self.name = name
        self.fcurves = []

class MockFCurve:
    def __init__(self, data_path, array_index=0):
        self.data_path = data_path
        self.array_index = array_index
        self.keyframe_points = []
        self.extrapolation = "CONSTANT"

# Import the command router (will use mocks)
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock bpy before importing handlers
sys.modules['bpy'] = MockBpy()
sys.modules['bpy.data'] = MockBpy.data
sys.modules['bpy.data.objects'] = MockBpy.data.objects
sys.modules['bpy.data.actions'] = MockBpy.data.actions
sys.modules['bpy.context'] = MockBpy.context
sys.modules['bpy.app'] = MockBpy.app
sys.modules['bpy.ops'] = MockBpy.ops
sys.modules['bpy.ops.mesh'] = MockBpy.ops.mesh

# Now import command router
try:
    from core.command_router import command_router
    from handlers.handler_registry import register_all_handlers
    
    # Register handlers
    register_all_handlers()
    print("✓ Handlers registered successfully")
except Exception as e:
    print(f"⚠️  Could not load modular system: {e}")
    print("Using basic command handling")
    command_router = None

class TestMCPServer:
    """Test server that simulates Blender MCP server"""
    
    def __init__(self, host='localhost', port=9877):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None
        self.server_thread = None
    
    def start(self):
        """Start the test server"""
        if self.running:
            print("Server is already running")
            return
        
        self.running = True
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            print(f"✓ Test MCP server started on {self.host}:{self.port}")
            print(f"  This is a simulation - no Blender required")
        except Exception as e:
            print(f"✗ Failed to start server: {e}")
            self.stop()
    
    def stop(self):
        """Stop the test server"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        print("Test server stopped")
    
    def _server_loop(self):
        """Main server loop"""
        self.socket.settimeout(1.0)
        
        while self.running:
            try:
                try:
                    client, address = self.socket.accept()
                    print(f"✓ Client connected: {address}")
                    
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error accepting connection: {e}")
                    time.sleep(0.5)
            except Exception as e:
                if not self.running:
                    break
                time.sleep(0.5)
    
    def _handle_client(self, client, address):
        """Handle client connection"""
        client.settimeout(None)
        buffer = b''
        
        try:
            while self.running:
                try:
                    data = client.recv(8192)
                    if not data:
                        print(f"Client {address} disconnected")
                        break
                    
                    buffer += data
                    try:
                        command = json.loads(buffer.decode('utf-8'))
                        buffer = b''
                        
                        # Execute command
                        response = self.execute_command(command)
                        response_json = json.dumps(response)
                        client.sendall(response_json.encode('utf-8'))
                    except json.JSONDecodeError:
                        # Incomplete data
                        if len(buffer) > 1024 * 1024:  # 1MB limit
                            print(f"Buffer too large from {address}")
                            break
                        continue
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    break
        except Exception as e:
            print(f"Error in client handler: {e}")
        finally:
            try:
                client.close()
            except:
                pass
    
    def execute_command(self, command):
        """Execute a command"""
        try:
            # Validate command
            if not isinstance(command, dict):
                if isinstance(command, str):
                    command = json.loads(command)
                else:
                    return {
                        "status": "error",
                        "error": {
                            "code": "INVALID_COMMAND",
                            "message": f"Command must be a dictionary, got: {type(command).__name__}"
                        }
                    }
            
            command_type = command.get("type")
            if not command_type:
                return {
                    "status": "error",
                    "error": {
                        "code": "INVALID_COMMAND",
                        "message": "Command type is required"
                    }
                }
            
            # Use command router if available
            if command_router:
                return command_router.route_command(command)
            else:
                # Basic fallback
                return {
                    "status": "success",
                    "result": {
                        "message": f"Command '{command_type}' received (simulated)",
                        "command": command_type,
                        "params": command.get("params", {})
                    }
                }
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

def main():
    """Run the test server"""
    print("="*60)
    print("Blender MCP Test Server")
    print("="*60)
    print("\nThis server simulates the Blender MCP server")
    print("Useful for testing command handling without Blender")
    print("\nPress Ctrl+C to stop\n")
    
    server = TestMCPServer(port=9877)  # Different port to avoid conflicts
    server.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping server...")
        server.stop()
        print("Server stopped")

if __name__ == "__main__":
    main()
