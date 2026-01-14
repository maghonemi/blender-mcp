# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.validation import OBJECT_NAME_SCHEMA
from utils.logger import logger

class CreateShapeKeyHandler(BaseHandler):
    """Handler for creating shape keys"""
    
    def get_command_name(self) -> str:
        return "create_shape_key"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            "shape_key_name": {
                "type": str,
                "required": True
            },
            "value": {
                "type": (int, float),
                "required": False
            },
            "relative_to": {
                "type": str,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a shape key"""
        object_name = params["object_name"]
        shape_key_name = params["shape_key_name"]
        value = params.get("value", 0.0)
        relative_to = params.get("relative_to", "Basis")
        
        obj = bpy.data.objects.get(object_name)
        if not obj or obj.type != 'MESH':
            raise ValueError(f"Mesh object '{object_name}' not found")
        
        # Ensure shape keys exist
        if not obj.data.shape_keys:
            obj.shape_key_add(name="Basis")
        
        # Add shape key
        shape_key = obj.shape_key_add(name=shape_key_name, from_mix=False)
        shape_key.value = value
        
        return {
            "shape_key_created": True,
            "shape_key_name": shape_key_name,
            "value": value
        }

class SetShapeKeyValueHandler(BaseHandler):
    """Handler for setting shape key value"""
    
    def get_command_name(self) -> str:
        return "set_shape_key_value"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            "shape_key_name": {
                "type": str,
                "required": True
            },
            "value": {
                "type": (int, float),
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Set shape key value"""
        object_name = params["object_name"]
        shape_key_name = params["shape_key_name"]
        value = params["value"]
        
        obj = bpy.data.objects.get(object_name)
        if not obj or not obj.data.shape_keys:
            raise ValueError(f"Object '{object_name}' has no shape keys")
        
        shape_key = obj.data.shape_keys.key_blocks.get(shape_key_name)
        if not shape_key:
            raise ValueError(f"Shape key '{shape_key_name}' not found")
        
        shape_key.value = value
        return {"value_set": True, "shape_key_name": shape_key_name, "value": value}

class GetShapeKeysHandler(BaseHandler):
    """Handler for getting shape keys"""
    
    def get_command_name(self) -> str:
        return "get_shape_keys"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return OBJECT_NAME_SCHEMA
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get all shape keys for an object"""
        object_name = params["object_name"]
        
        obj = bpy.data.objects.get(object_name)
        if not obj or not obj.data.shape_keys:
            return {"shape_keys": []}
        
        shape_keys = []
        for key_block in obj.data.shape_keys.key_blocks:
            # Count keyframes if animated
            keyframe_count = 0
            if obj.data.shape_keys.animation_data and obj.data.shape_keys.animation_data.action:
                for fcurve in obj.data.shape_keys.animation_data.action.fcurves:
                    if fcurve.data_path.endswith(f'["{key_block.name}"].value'):
                        keyframe_count = len(fcurve.keyframe_points)
                        break
            
            shape_keys.append({
                "name": key_block.name,
                "value": key_block.value,
                "keyframe_count": keyframe_count
            })
        
        return {"shape_keys": shape_keys}
