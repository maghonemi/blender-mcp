# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Project setup handler for common Blender project configurations

import bpy
from typing import Dict, Any, List, Optional
from handlers.base_handler import BaseHandler
from utils.logger import logger

HANDLER_VERSION = "1.0.0"


class SetupProjectHandler(BaseHandler):
    """Handler for setting up Blender projects with common configurations"""
    
    def get_command_name(self) -> str:
        return "setup_project"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "clear_objects": {
                "type": bool,
                "required": False
            },
            "frame_start": {
                "type": int,
                "required": False
            },
            "frame_end": {
                "type": int,
                "required": False
            },
            "fps": {
                "type": int,
                "required": False
            },
            "resolution_x": {
                "type": int,
                "required": False
            },
            "resolution_y": {
                "type": int,
                "required": False
            },
            "render_engine": {
                "type": str,
                "required": False
            },
            "eevee_settings": {
                "type": dict,
                "required": False
            },
            "collections": {
                "type": list,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Set up a Blender project with specified settings"""
        scene = bpy.context.scene
        results = []
        
        # Clear objects if requested
        if params.get("clear_objects", False):
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
            results.append("Cleared all objects")
        
        # Timeline settings
        if "frame_start" in params:
            scene.frame_start = params["frame_start"]
            results.append(f"Frame start: {scene.frame_start}")
        
        if "frame_end" in params:
            scene.frame_end = params["frame_end"]
            results.append(f"Frame end: {scene.frame_end}")
        
        if "fps" in params:
            scene.render.fps = params["fps"]
            results.append(f"FPS: {scene.render.fps}")
        
        # Resolution settings
        if "resolution_x" in params:
            scene.render.resolution_x = params["resolution_x"]
            results.append(f"Resolution X: {scene.render.resolution_x}")
        
        if "resolution_y" in params:
            scene.render.resolution_y = params["resolution_y"]
            results.append(f"Resolution Y: {scene.render.resolution_y}")
        
        if "resolution_percentage" in params:
            scene.render.resolution_percentage = params["resolution_percentage"]
            results.append(f"Resolution percentage: {scene.render.resolution_percentage}%")
        
        # Render engine
        if "render_engine" in params:
            engine = params["render_engine"]
            # Handle Blender version differences
            if engine == "EEVEE_NEXT" and not hasattr(bpy.types, 'EEVEE_NEXT'):
                engine = "BLENDER_EEVEE"
            elif engine == "EEVEE_NEXT":
                engine = "BLENDER_EEVEE_NEXT"
            scene.render.engine = engine
            results.append(f"Render engine: {scene.render.engine}")
        
        # Eevee settings
        if "eevee_settings" in params and scene.render.engine in ['BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT']:
            try:
                eevee = scene.eevee
                settings = params["eevee_settings"]
                
                # Check if attributes exist before setting (Blender version compatibility)
                if "use_bloom" in settings and hasattr(eevee, 'use_bloom'):
                    eevee.use_bloom = settings["use_bloom"]
                if "bloom_threshold" in settings and hasattr(eevee, 'bloom_threshold'):
                    eevee.bloom_threshold = settings["bloom_threshold"]
                if "bloom_intensity" in settings and hasattr(eevee, 'bloom_intensity'):
                    eevee.bloom_intensity = settings["bloom_intensity"]
                if "bloom_radius" in settings and hasattr(eevee, 'bloom_radius'):
                    eevee.bloom_radius = settings["bloom_radius"]
                if "use_volumetric_lights" in settings and hasattr(eevee, 'use_volumetric_lights'):
                    eevee.use_volumetric_lights = settings["use_volumetric_lights"]
                if "volumetric_tile_size" in settings and hasattr(eevee, 'volumetric_tile_size'):
                    eevee.volumetric_tile_size = settings["volumetric_tile_size"]
                if "volumetric_samples" in settings and hasattr(eevee, 'volumetric_samples'):
                    eevee.volumetric_samples = settings["volumetric_samples"]
                if "volumetric_end" in settings and hasattr(eevee, 'volumetric_end'):
                    eevee.volumetric_end = settings["volumetric_end"]
                
                results.append("Eevee settings applied")
            except Exception as e:
                logger.warning(f"Could not apply all Eevee settings: {str(e)}")
                results.append(f"Eevee settings partially applied (some attributes not available)")
        
        # Create collections
        if "collections" in params:
            collections_created = []
            for col_name in params["collections"]:
                if col_name not in bpy.data.collections:
                    new_col = bpy.data.collections.new(col_name)
                    bpy.context.scene.collection.children.link(new_col)
                    collections_created.append(col_name)
            if collections_created:
                results.append(f"Collections created: {collections_created}")
        
        return {
            "setup_complete": True,
            "settings_applied": results,
            "frame_range": f"{scene.frame_start}-{scene.frame_end}",
            "fps": scene.render.fps,
            "resolution": f"{scene.render.resolution_x}x{scene.render.resolution_y}",
            "render_engine": scene.render.engine
        }
