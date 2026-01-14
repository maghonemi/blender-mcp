# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

"""
Rendering handlers for setting render output and other render settings
"""

from typing import Any, Dict
import bpy
import os
from handlers.base_handler import BaseHandler
from utils.logger import logger


class SetRenderOutputHandler(BaseHandler):
    """Handler for setting render output path and format"""
    
    def get_command_name(self) -> str:
        return "set_render_output"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "filepath": {
                "type": str,
                "required": True
            },
            "file_format": {
                "type": str,
                "required": False
            },
            "color_mode": {
                "type": str,
                "required": False
            },
            "color_depth": {
                "type": str,
                "required": False
            },
            "compression": {
                "type": int,
                "required": False
            },
            "exr_codec": {
                "type": str,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Set render output path and format"""
        filepath = params["filepath"]
        file_format = params.get("file_format", "PNG")
        color_mode = params.get("color_mode", "RGB")
        color_depth = params.get("color_depth", "8")
        compression = params.get("compression", 15)
        exr_codec = params.get("exr_codec", "ZIP")
        
        scene = bpy.context.scene
        
        # Set the filepath (directory for animations, full path for single images)
        # Ensure directory exists
        output_dir = os.path.dirname(filepath) if os.path.dirname(filepath) else filepath
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                logger.warning(f"Could not create output directory {output_dir}: {e}")
        
        # Set render filepath
        scene.render.filepath = filepath
        
        # Set file format
        format_map = {
            "PNG": "PNG",
            "JPEG": "JPEG",
            "OPEN_EXR": "OPEN_EXR",
            "TIFF": "TIFF",
            "EXR": "OPEN_EXR"
        }
        
        render_format = format_map.get(file_format.upper(), "PNG")
        scene.render.image_settings.file_format = render_format
        
        # Set color mode
        color_mode_map = {
            "RGB": "RGB",
            "RGBA": "RGBA",
            "BW": "BW"
        }
        scene.render.image_settings.color_mode = color_mode_map.get(color_mode.upper(), "RGB")
        
        # Set color depth
        if render_format == "PNG":
            depth_map = {"8": 8, "16": 16}
            scene.render.image_settings.color_depth = depth_map.get(color_depth, "8")
        elif render_format == "OPEN_EXR":
            depth_map = {"16": "16", "32": "32"}
            scene.render.image_settings.exr_codec = exr_codec
            scene.render.image_settings.color_depth = depth_map.get(color_depth, "16")
        
        # Set compression for JPEG
        if render_format == "JPEG":
            scene.render.image_settings.quality = compression
        
        return {
            "filepath": scene.render.filepath,
            "file_format": scene.render.image_settings.file_format,
            "color_mode": scene.render.image_settings.color_mode,
            "color_depth": str(scene.render.image_settings.color_depth) if hasattr(scene.render.image_settings, 'color_depth') else None
        }


class GetRenderSettingsHandler(BaseHandler):
    """Handler for getting current render settings"""
    
    def get_command_name(self) -> str:
        return "get_render_settings"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {}
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get current render settings"""
        scene = bpy.context.scene
        render = scene.render
        
        return {
            "engine": render.engine,
            "resolution": [render.resolution_x, render.resolution_y],
            "resolution_percentage": render.resolution_percentage,
            "file_format": render.image_settings.file_format,
            "output_path": render.filepath,
            "color_mode": render.image_settings.color_mode,
            "color_depth": str(render.image_settings.color_depth) if hasattr(render.image_settings, 'color_depth') else None
        }
