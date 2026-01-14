# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.cache import cache
from utils.logger import logger

class GetSceneInfoHandler(BaseHandler):
    """Handler for getting scene information"""
    
    def get_command_name(self) -> str:
        return "get_scene_info"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {}  # No parameters required
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get information about the current Blender scene"""
        try:
            # Check cache first
            cache_key = f"scene_info_{bpy.context.scene.name}"
            cached = cache.get(cache_key)
            if cached:
                return cached
            
            logger.info("Getting scene info...")
            scene = bpy.context.scene
            
            # Simplify the scene info to reduce data size
            scene_info = {
                "name": scene.name,
                "object_count": len(scene.objects),
                "objects": [],
                "materials_count": len(bpy.data.materials),
                "collections_count": len(bpy.data.collections),
                "frame_current": scene.frame_current,
                "frame_start": scene.frame_start,
                "frame_end": scene.frame_end,
                "fps": scene.render.fps,
            }
            
            # Collect minimal object information (limit to first 20 objects)
            for i, obj in enumerate(scene.objects):
                if i >= 20:
                    break
                
                obj_info = {
                    "name": obj.name,
                    "type": obj.type,
                    "location": [
                        round(float(obj.location.x), 2),
                        round(float(obj.location.y), 2),
                        round(float(obj.location.z), 2)
                    ],
                    "visible": obj.visible_get(),
                }
                scene_info["objects"].append(obj_info)
            
            # Cache the result
            cache.set(cache_key, scene_info, ttl=5)  # 5 second cache
            
            logger.info(f"Scene info collected: {len(scene_info['objects'])} objects")
            return scene_info
        except Exception as e:
            logger.exception(f"Error in get_scene_info: {str(e)}")
            raise
