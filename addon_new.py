# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Enhanced with comprehensive Blender MCP system

# bl_info MUST be defined before any imports that might fail
bl_info = {
    "name": "Blender MCP",
    "author": "BlenderMCP",
    "version": (2, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > BlenderMCP",
    "description": "Connect Blender to Claude via MCP - Comprehensive Edition",
    "category": "Interface",
}

import bpy
from bpy.props import IntProperty, BoolProperty
import os
import sys

# Add current directory and parent directory to path for imports
# This handles both single-file and directory installations
blender_mcp_file = os.path.abspath(__file__)
blender_mcp_dir = os.path.dirname(blender_mcp_file)
blender_mcp_parent = os.path.dirname(blender_mcp_dir)

# Add both current directory and parent directory to path
for path in [blender_mcp_dir, blender_mcp_parent]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Additional imports needed for the server
import json
import threading
import socket
import time
import traceback

# Initialize fallback logger first (always available)
class FallbackLogger:
    @staticmethod
    def info(msg):
        print(f"INFO: {msg}")
    @staticmethod
    def error(msg):
        print(f"ERROR: {msg}")
    @staticmethod
    def warning(msg):
        print(f"WARNING: {msg}")
    @staticmethod
    def debug(msg):
        print(f"DEBUG: {msg}")
    @staticmethod
    def exception(msg):
        print(f"EXCEPTION: {msg}")
        traceback.print_exc()

# Define a WORKING fallback server that doesn't depend on modular imports
# This is based on the original addon.py server
class FallbackBlenderMCPServer:
    """Fallback server that works without modular system"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None
        self.server_thread = None

    def start(self):
        if self.running:
            print("Server is already running")
            return

        self.running = True

        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)

            # Start server thread
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()

            print(f"BlenderMCP server started on {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to start server: {str(e)}")
            self.stop()

    def stop(self):
        self.running = False

        # Close socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        # Wait for thread to finish
        if self.server_thread:
            try:
                if self.server_thread.is_alive():
                    self.server_thread.join(timeout=1.0)
            except:
                pass
            self.server_thread = None

        print("BlenderMCP server stopped")

    def _server_loop(self):
        """Main server loop in a separate thread"""
        print("Server thread started")
        self.socket.settimeout(1.0)

        while self.running:
            try:
                try:
                    client, address = self.socket.accept()
                    print(f"Connected to client: {address}")

                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error accepting connection: {str(e)}")
                    time.sleep(0.5)
            except Exception as e:
                print(f"Error in server loop: {str(e)}")
                if not self.running:
                    break
                time.sleep(0.5)

        print("Server thread stopped")

    def _handle_client(self, client):
        """Handle connected client"""
        print("Client handler started")
        client.settimeout(None)
        buffer = b''

        try:
            while self.running:
                try:
                    data = client.recv(8192)
                    if not data:
                        print("Client disconnected")
                        break

                    buffer += data
                    try:
                        command = json.loads(buffer.decode('utf-8'))
                        buffer = b''

                        def execute_wrapper():
                            try:
                                response = self.execute_command(command)
                                response_json = json.dumps(response)
                                try:
                                    client.sendall(response_json.encode('utf-8'))
                                except:
                                    print("Failed to send response - client disconnected")
                            except Exception as e:
                                print(f"Error executing command: {str(e)}")
                                traceback.print_exc()
                                try:
                                    error_response = {
                                        "status": "error",
                                        "message": str(e)
                                    }
                                    client.sendall(json.dumps(error_response).encode('utf-8'))
                                except:
                                    pass
                            return None

                        bpy.app.timers.register(execute_wrapper, first_interval=0.0)
                    except json.JSONDecodeError:
                        pass
                except Exception as e:
                    print(f"Error receiving data: {str(e)}")
                    break
        except Exception as e:
            print(f"Error in client handler: {str(e)}")
        finally:
            try:
                client.close()
            except:
                pass
            print("Client handler stopped")

    def execute_command(self, command):
        """Execute a command - basic implementation"""
        try:
            # Validate command is a dictionary
            if not isinstance(command, dict):
                if isinstance(command, str):
                    # Try to parse if it's a JSON string
                    try:
                        command = json.loads(command)
                    except json.JSONDecodeError:
                        return {
                            "status": "error",
                            "message": f"Command must be a dictionary or valid JSON, got: {type(command).__name__}"
                        }
                else:
                    return {
                        "status": "error",
                        "message": f"Command must be a dictionary, got: {type(command).__name__}"
                    }
            
            # Now safe to use .get()
            cmd_type = command.get("type")
            params = command.get("params", {})
            
            if not cmd_type:
                return {
                    "status": "error",
                    "message": "Command type is required"
                }
            
            # Basic command handling
            if cmd_type == "get_scene_info":
                return self._get_scene_info()
            elif cmd_type == "execute_code":
                return self._execute_code(params.get("code", ""))
            else:
                # Check if modular system is available
                if MODULAR_SYSTEM_AVAILABLE:
                    # Try to use modular system (shouldn't reach here if router works)
                    return {
                        "status": "error",
                        "error": {
                            "code": "HANDLER_NOT_FOUND",
                            "message": f"Command '{cmd_type}' not found. Modular system loaded but handler not registered."
                        }
                    }
                else:
                    return {
                        "status": "error",
                        "error": {
                            "code": "MODULAR_SYSTEM_NOT_LOADED",
                            "message": f"Command '{cmd_type}' requires the modular system. Please ensure core/, handlers/, and utils/ directories are installed."
                        }
                    }
        except Exception as e:
            print(f"Error executing command: {str(e)}")
            traceback.print_exc()
            return {"status": "error", "message": str(e)}
    
    def _get_scene_info(self):
        """Get basic scene information"""
        scene = bpy.context.scene
        objects = []
        for obj in scene.objects:
            objects.append({
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
            })
        return {
            "status": "success",
            "result": {
                "scene_name": scene.name,
                "object_count": len(scene.objects),
                "objects": objects[:50],  # Limit to 50
            }
        }
    
    def _execute_code(self, code):
        """Execute Python code in Blender"""
        try:
            # Create a namespace for execution
            namespace = {"bpy": bpy}
            exec(code, namespace)
            return {"status": "success", "result": "Code executed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Try to import new modular system
# Handle both single-file and directory installations
MODULAR_SYSTEM_AVAILABLE = False
BlenderMCPServer = FallbackBlenderMCPServer  # Default to fallback
register_all_handlers = lambda: None  # Default to no-op
logger = FallbackLogger()  # Initialize with fallback first

try:
    from core.server import BlenderMCPServer as ModularServer
    from handlers.handler_registry import register_all_handlers as modular_register
    from utils.logger import logger as modular_logger
    BlenderMCPServer = ModularServer
    register_all_handlers = modular_register
    logger = modular_logger
    MODULAR_SYSTEM_AVAILABLE = True
    print("BlenderMCP: Modular system loaded successfully")
except ImportError as import_error:
    print(f"BlenderMCP: Modular system not available ({import_error})")
    print("BlenderMCP: Using fallback server with basic functionality")
    # BlenderMCPServer already set to FallbackBlenderMCPServer above

# Import existing integration code (will be preserved)
# This will be handled by creating wrapper handlers

RODIN_FREE_TRIAL_KEY = "k9TcfFoEhNd9cCPP2guHAHHHkctZHIRhZDywZ1euGUXwihbYLpOjQhofby80NJez"

# Import existing integration handlers
# These will be created as wrapper handlers that use the original methods
# For now, we'll import the original addon methods

# Load original addon methods for integrations
# We'll create a compatibility layer

class IntegrationCompatibility:
    """Compatibility layer for existing integrations"""
    
    @staticmethod
    def load_original_methods():
        """Load methods from original addon.py"""
        # This will be populated with original integration methods
        # For now, we'll create stub handlers
        pass

# Register all new handlers (only if modular system is available)
# This will be done in the register() function to avoid errors during import

# Blender Addon Preferences (preserved from original)
class BLENDERMCP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    telemetry_consent: BoolProperty(
        name="Allow Anonymized Prompt Collection",
        description="Allow collection of anonymized prompts to help improve Blender MCP",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        
        # Telemetry section
        layout.label(text="Telemetry & Privacy:", icon='PREFERENCES')
        
        box = layout.box()
        row = box.row()
        row.prop(self, "telemetry_consent", text="Allow Anonymized Prompt Collection")
        
        # Info text
        box.separator()
        box.label(text="All data is anonymized and helps improve Blender MCP.", icon='INFO')
        box.label(text="You can opt out anytime by unchecking the box above.", icon='INFO')
        
        # Terms and Conditions link
        box.separator()
        row = box.row()
        row.operator("blendermcp.open_terms", text="View Terms and Conditions", icon='TEXT')

# Blender UI Panel (preserved from original)
class BLENDERMCP_PT_Panel(bpy.types.Panel):
    bl_label = "Blender MCP"
    bl_idname = "BLENDERMCP_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlenderMCP'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "blendermcp_port")
        layout.prop(scene, "blendermcp_use_polyhaven", text="Use assets from Poly Haven")

        layout.prop(scene, "blendermcp_use_hyper3d", text="Use Hyper3D Rodin 3D model generation")
        if scene.blendermcp_use_hyper3d:
            layout.prop(scene, "blendermcp_hyper3d_mode", text="Rodin Mode")
            layout.prop(scene, "blendermcp_hyper3d_api_key", text="API Key")
            layout.operator("blendermcp.set_hyper3d_free_trial_api_key", text="Set Free Trial API Key")

        layout.prop(scene, "blendermcp_use_sketchfab", text="Use assets from Sketchfab")
        if scene.blendermcp_use_sketchfab:
            layout.prop(scene, "blendermcp_sketchfab_api_key", text="API Key")

        layout.prop(scene, "blendermcp_use_hunyuan3d", text="Use Tencent Hunyuan 3D model generation")
        if scene.blendermcp_use_hunyuan3d:
            layout.prop(scene, "blendermcp_hunyuan3d_mode", text="Hunyuan3D Mode")
            if scene.blendermcp_hunyuan3d_mode == 'OFFICIAL_API':
                layout.prop(scene, "blendermcp_hunyuan3d_secret_id", text="SecretId")
                layout.prop(scene, "blendermcp_hunyuan3d_secret_key", text="SecretKey")
            if scene.blendermcp_hunyuan3d_mode == 'LOCAL_API':
                layout.prop(scene, "blendermcp_hunyuan3d_api_url", text="API URL")
                layout.prop(scene, "blendermcp_hunyuan3d_octree_resolution", text="Octree Resolution")
                layout.prop(scene, "blendermcp_hunyuan3d_num_inference_steps", text="Number of Inference Steps")
                layout.prop(scene, "blendermcp_hunyuan3d_guidance_scale", text="Guidance Scale")
                layout.prop(scene, "blendermcp_hunyuan3d_texture", text="Generate Texture")
        
        if not scene.blendermcp_server_running:
            layout.operator("blendermcp.start_server", text="Connect to MCP server")
        else:
            layout.operator("blendermcp.stop_server", text="Disconnect from MCP server")
            layout.label(text=f"Running on port {scene.blendermcp_port}")

# Operators (preserved from original)
class BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey(bpy.types.Operator):
    bl_idname = "blendermcp.set_hyper3d_free_trial_api_key"
    bl_label = "Set Free Trial API Key"

    def execute(self, context):
        context.scene.blendermcp_hyper3d_api_key = RODIN_FREE_TRIAL_KEY
        context.scene.blendermcp_hyper3d_mode = 'MAIN_SITE'
        self.report({'INFO'}, "API Key set successfully!")
        return {'FINISHED'}

class BLENDERMCP_OT_StartServer(bpy.types.Operator):
    bl_idname = "blendermcp.start_server"
    bl_label = "Connect to Claude"
    bl_description = "Start the BlenderMCP server to connect with Claude"

    def execute(self, context):
        scene = context.scene

        # Create a new server instance using new modular server
        if not hasattr(bpy.types, "blendermcp_server") or not bpy.types.blendermcp_server:
            bpy.types.blendermcp_server = BlenderMCPServer(port=scene.blendermcp_port)

        # Start the server
        bpy.types.blendermcp_server.start()
        scene.blendermcp_server_running = True

        return {'FINISHED'}

class BLENDERMCP_OT_StopServer(bpy.types.Operator):
    bl_idname = "blendermcp.stop_server"
    bl_label = "Stop the connection to Claude"
    bl_description = "Stop the connection to Claude"

    def execute(self, context):
        scene = context.scene

        # Stop the server if it exists
        if hasattr(bpy.types, "blendermcp_server") and bpy.types.blendermcp_server:
            bpy.types.blendermcp_server.stop()
            del bpy.types.blendermcp_server

        scene.blendermcp_server_running = False

        return {'FINISHED'}

class BLENDERMCP_OT_OpenTerms(bpy.types.Operator):
    bl_idname = "blendermcp.open_terms"
    bl_label = "View Terms and Conditions"
    bl_description = "Open the Terms and Conditions document"

    def execute(self, context):
        terms_url = "https://github.com/ahujasid/blender-mcp/blob/main/TERMS_AND_CONDITIONS.md"
        try:
            import webbrowser
            webbrowser.open(terms_url)
            self.report({'INFO'}, "Terms and Conditions opened in browser")
        except Exception as e:
            self.report({'ERROR'}, f"Could not open Terms and Conditions: {str(e)}")
        
        return {'FINISHED'}

# Registration functions
def register():
    # Register scene properties
    bpy.types.Scene.blendermcp_port = IntProperty(
        name="Port",
        description="Port for the BlenderMCP server",
        default=9876,
        min=1024,
        max=65535
    )

    bpy.types.Scene.blendermcp_server_running = bpy.props.BoolProperty(
        name="Server Running",
        default=False
    )

    bpy.types.Scene.blendermcp_use_polyhaven = bpy.props.BoolProperty(
        name="Use Poly Haven",
        description="Enable Poly Haven asset integration",
        default=False
    )

    bpy.types.Scene.blendermcp_use_hyper3d = bpy.props.BoolProperty(
        name="Use Hyper3D Rodin",
        description="Enable Hyper3D Rodin generation integration",
        default=False
    )

    bpy.types.Scene.blendermcp_hyper3d_mode = bpy.props.EnumProperty(
        name="Rodin Mode",
        description="Choose the platform used to call Rodin APIs",
        items=[
            ("MAIN_SITE", "hyper3d.ai", "hyper3d.ai"),
            ("FAL_AI", "fal.ai", "fal.ai"),
        ],
        default="MAIN_SITE"
    )

    bpy.types.Scene.blendermcp_hyper3d_api_key = bpy.props.StringProperty(
        name="Hyper3D API Key",
        subtype="PASSWORD",
        description="API Key provided by Hyper3D",
        default=""
    )

    bpy.types.Scene.blendermcp_use_hunyuan3d = bpy.props.BoolProperty(
        name="Use Hunyuan 3D",
        description="Enable Hunyuan asset integration",
        default=False
    )

    bpy.types.Scene.blendermcp_hunyuan3d_mode = bpy.props.EnumProperty(
        name="Hunyuan3D Mode",
        description="Choose a local or official APIs",
        items=[
            ("LOCAL_API", "local api", "local api"),
            ("OFFICIAL_API", "official api", "official api"),
        ],
        default="LOCAL_API"
    )

    bpy.types.Scene.blendermcp_hunyuan3d_secret_id = bpy.props.StringProperty(
        name="Hunyuan 3D SecretId",
        description="SecretId provided by Hunyuan 3D",
        default=""
    )

    bpy.types.Scene.blendermcp_hunyuan3d_secret_key = bpy.props.StringProperty(
        name="Hunyuan 3D SecretKey",
        subtype="PASSWORD",
        description="SecretKey provided by Hunyuan 3D",
        default=""
    )

    bpy.types.Scene.blendermcp_hunyuan3d_api_url = bpy.props.StringProperty(
        name="API URL",
        description="URL of the Hunyuan 3D API service",
        default="http://localhost:8081"
    )

    bpy.types.Scene.blendermcp_hunyuan3d_octree_resolution = bpy.props.IntProperty(
        name="Octree Resolution",
        description="Octree resolution for the 3D generation",
        default=256,
        min=128,
        max=512,
    )

    bpy.types.Scene.blendermcp_hunyuan3d_num_inference_steps = bpy.props.IntProperty(
        name="Number of Inference Steps",
        description="Number of inference steps for the 3D generation",
        default=20,
        min=20,
        max=50,
    )

    bpy.types.Scene.blendermcp_hunyuan3d_guidance_scale = bpy.props.FloatProperty(
        name="Guidance Scale",
        description="Guidance scale for the 3D generation",
        default=5.5,
        min=1.0,
        max=10.0,
    )

    bpy.types.Scene.blendermcp_hunyuan3d_texture = bpy.props.BoolProperty(
        name="Generate Texture",
        description="Whether to generate texture for the 3D model",
        default=False,
    )
    
    bpy.types.Scene.blendermcp_use_sketchfab = bpy.props.BoolProperty(
        name="Use Sketchfab",
        description="Enable Sketchfab asset integration",
        default=False
    )

    bpy.types.Scene.blendermcp_sketchfab_api_key = bpy.props.StringProperty(
        name="Sketchfab API Key",
        subtype="PASSWORD",
        description="API Key provided by Sketchfab",
        default=""
    )

    # Register classes
    bpy.utils.register_class(BLENDERMCP_AddonPreferences)
    bpy.utils.register_class(BLENDERMCP_PT_Panel)
    bpy.utils.register_class(BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey)
    bpy.utils.register_class(BLENDERMCP_OT_StartServer)
    bpy.utils.register_class(BLENDERMCP_OT_StopServer)
    bpy.utils.register_class(BLENDERMCP_OT_OpenTerms)

    # Register all new handlers (only if modular system is available)
    if MODULAR_SYSTEM_AVAILABLE and register_all_handlers is not None:
        try:
            register_all_handlers()
            logger.info("All handlers registered successfully")
            print("BlenderMCP: All handlers registered successfully")
        except Exception as e:
            error_msg = f"Error registering handlers: {e}"
            logger.error(error_msg)
            print(f"BlenderMCP: {error_msg}")
            import traceback
            traceback.print_exc()
    else:
        print("BlenderMCP: Modular system not available - using basic functionality")

    logger.info("BlenderMCP addon registered (v2.0)")
    print("BlenderMCP addon registered (v2.0)")

def unregister():
    # Stop the server if it's running
    if hasattr(bpy.types, "blendermcp_server") and bpy.types.blendermcp_server:
        bpy.types.blendermcp_server.stop()
        del bpy.types.blendermcp_server

    bpy.utils.unregister_class(BLENDERMCP_PT_Panel)
    bpy.utils.unregister_class(BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey)
    bpy.utils.unregister_class(BLENDERMCP_OT_StartServer)
    bpy.utils.unregister_class(BLENDERMCP_OT_StopServer)
    bpy.utils.unregister_class(BLENDERMCP_OT_OpenTerms)
    bpy.utils.unregister_class(BLENDERMCP_AddonPreferences)

    # Clean up scene properties
    del bpy.types.Scene.blendermcp_port
    del bpy.types.Scene.blendermcp_server_running
    del bpy.types.Scene.blendermcp_use_polyhaven
    del bpy.types.Scene.blendermcp_use_hyper3d
    del bpy.types.Scene.blendermcp_hyper3d_mode
    del bpy.types.Scene.blendermcp_hyper3d_api_key
    del bpy.types.Scene.blendermcp_use_sketchfab
    del bpy.types.Scene.blendermcp_sketchfab_api_key
    del bpy.types.Scene.blendermcp_use_hunyuan3d
    del bpy.types.Scene.blendermcp_hunyuan3d_mode
    del bpy.types.Scene.blendermcp_hunyuan3d_secret_id
    del bpy.types.Scene.blendermcp_hunyuan3d_secret_key
    del bpy.types.Scene.blendermcp_hunyuan3d_api_url
    del bpy.types.Scene.blendermcp_hunyuan3d_octree_resolution
    del bpy.types.Scene.blendermcp_hunyuan3d_num_inference_steps
    del bpy.types.Scene.blendermcp_hunyuan3d_guidance_scale
    del bpy.types.Scene.blendermcp_hunyuan3d_texture

    logger.info("BlenderMCP addon unregistered")
    print("BlenderMCP addon unregistered")

if __name__ == "__main__":
    register()
