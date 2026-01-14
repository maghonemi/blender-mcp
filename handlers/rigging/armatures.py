# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.validation import validate_object_exists
from utils.logger import logger

class CreateArmatureHandler(BaseHandler):
    """Handler for creating armatures"""
    
    def get_command_name(self) -> str:
        return "create_armature"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "name": {
                "type": str,
                "required": True
            },
            "location": {
                "type": list,
                "required": False
            },
            "add_bones": {
                "type": bool,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Create an armature"""
        name = params["name"]
        location = params.get("location", [0, 0, 0])
        add_bones = params.get("add_bones", False)
        
        # Create armature
        bpy.ops.object.armature_add(location=location)
        armature = bpy.context.active_object
        armature.name = name
        
        if add_bones:
            # Enter edit mode and add a bone
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')
            # Default bone is already created
        
        return {
            "armature_name": name,
            "bone_count": len(armature.data.bones),
            "mode": "EDIT" if add_bones else "OBJECT"
        }

class GetArmatureInfoHandler(BaseHandler):
    """Handler for getting armature information"""
    
    def get_command_name(self) -> str:
        return "get_armature_info"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get armature information"""
        armature_name = params["armature_name"]
        armature = bpy.data.objects.get(armature_name)
        
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")
        
        bones = []
        for bone in armature.data.bones:
            bones.append({
                "name": bone.name,
                "parent": bone.parent.name if bone.parent else None,
                "head": [bone.head.x, bone.head.y, bone.head.z],
                "tail": [bone.tail.x, bone.tail.y, bone.tail.z],
                "length": bone.length
            })
        
        return {
            "name": armature_name,
            "bone_count": len(armature.data.bones),
            "mode": armature.mode,
            "bones": bones
        }
