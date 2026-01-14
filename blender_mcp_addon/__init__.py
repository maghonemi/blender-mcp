# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Enhanced with comprehensive Blender MCP system
# This is the main addon package - install this directory in Blender

bl_info = {
    "name": "Blender MCP",
    "author": "BlenderMCP",
    "version": (2, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > BlenderMCP",
    "description": "Connect Blender to Claude via MCP - Comprehensive Edition",
    "category": "Interface",
}

# Import from parent directory structure
# When installed, core/, handlers/, utils/ should be in the same directory
import os
import sys

# Get the addon directory
addon_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(addon_dir)

# Add parent directory to path if modules are there
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Also add addon directory itself
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

# Now import the modules
try:
    from core.server import BlenderMCPServer
    from handlers.handler_registry import register_all_handlers
    from utils.logger import logger
except ImportError:
    # Try importing from current directory structure
    import importlib.util
    
    # Try to load from parent directory
    core_path = os.path.join(parent_dir, "core", "server.py")
    if os.path.exists(core_path):
        spec = importlib.util.spec_from_file_location("core.server", core_path)
        core_server = importlib.util.module_from_spec(spec)
        sys.modules["core.server"] = core_server
        spec.loader.exec_module(core_server)
        BlenderMCPServer = core_server.BlenderMCPServer
    
    handlers_path = os.path.join(parent_dir, "handlers", "handler_registry.py")
    if os.path.exists(handlers_path):
        spec = importlib.util.spec_from_file_location("handlers.handler_registry", handlers_path)
        handlers_reg = importlib.util.module_from_spec(spec)
        sys.modules["handlers.handler_registry"] = handlers_reg
        spec.loader.exec_module(handlers_reg)
        register_all_handlers = handlers_reg.register_all_handlers
    
    utils_path = os.path.join(parent_dir, "utils", "logger.py")
    if os.path.exists(utils_path):
        spec = importlib.util.spec_from_file_location("utils.logger", utils_path)
        utils_logger = importlib.util.module_from_spec(spec)
        sys.modules["utils.logger"] = utils_logger
        spec.loader.exec_module(utils_logger)
        logger = utils_logger.logger

# Import the rest of the addon
from . import addon_main

# Re-export everything
RODIN_FREE_TRIAL_KEY = addon_main.RODIN_FREE_TRIAL_KEY
BLENDERMCP_AddonPreferences = addon_main.BLENDERMCP_AddonPreferences
BLENDERMCP_PT_Panel = addon_main.BLENDERMCP_PT_Panel
BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey = addon_main.BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey
BLENDERMCP_OT_StartServer = addon_main.BLENDERMCP_OT_StartServer
BLENDERMCP_OT_StopServer = addon_main.BLENDERMCP_OT_StopServer
BLENDERMCP_OT_OpenTerms = addon_main.BLENDERMCP_OT_OpenTerms

def register():
    # Register handlers first
    if 'register_all_handlers' in globals():
        try:
            register_all_handlers()
            logger.info("All handlers registered successfully")
        except Exception as e:
            logger.error(f"Error registering handlers: {e}")
            import traceback
            traceback.print_exc()
    
    # Register the main addon
    addon_main.register()

def unregister():
    addon_main.unregister()
