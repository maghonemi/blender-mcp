# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.validation import validate_object_exists
from utils.logger import logger

class CreateBoneHandler(BaseHandler):
    """Handler for creating bones"""
    
    def get_command_name(self) -> str:
        return "create_bone"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "bone_name": {
                "type": str,
                "required": True
            },
            "head": {
                "type": list,
                "required": True
            },
            "tail": {
                "type": list,
                "required": True
            },
            "parent": {
                "type": str,
                "required": False
            },
            "roll": {
                "type": (int, float),
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a bone in an armature"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        head = params["head"]
        tail = params["tail"]
        parent = params.get("parent")
        roll = params.get("roll", 0.0)
        
        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")
        
        # Set active and enter edit mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Create bone
        bone = armature.data.edit_bones.new(bone_name)
        bone.head = head
        bone.tail = tail
        bone.roll = roll
        
        # Set parent if provided
        if parent:
            parent_bone = armature.data.edit_bones.get(parent)
            if parent_bone:
                bone.parent = parent_bone
        
        return {"bone_created": True, "bone_name": bone_name}

class GetBoneInfoHandler(BaseHandler):
    """Handler for getting bone information"""
    
    def get_command_name(self) -> str:
        return "get_bone_info"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "bone_name": {
                "type": str,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get bone information"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        
        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")
        
        # Try to get bone from bones (object mode) or edit_bones (edit mode)
        bone = armature.data.bones.get(bone_name)
        edit_bone = None
        
        if not bone:
            # Try edit_bones if in edit mode
            edit_bone = armature.data.edit_bones.get(bone_name) if armature.data.edit_bones else None
            if not edit_bone:
                raise ValueError(f"Bone '{bone_name}' not found")
        
        # Use bone or edit_bone
        bone_obj = bone if bone else edit_bone
        
        # Get roll - might not be available on all bone types
        try:
            roll = bone_obj.roll if hasattr(bone_obj, 'roll') else 0.0
        except:
            roll = 0.0
        
        # Get matrix - might not be available on edit_bones
        try:
            if hasattr(bone_obj, 'matrix_local'):
                matrix = [list(row) for row in bone_obj.matrix_local]
            else:
                matrix = None
        except:
            matrix = None
        
        return {
            "name": bone_obj.name,
            "parent": bone_obj.parent.name if bone_obj.parent else None,
            "children": [child.name for child in bone_obj.children],
            "head": [bone_obj.head.x, bone_obj.head.y, bone_obj.head.z],
            "tail": [bone_obj.tail.x, bone_obj.tail.y, bone_obj.tail.z],
            "length": bone_obj.length,
            "roll": roll,
            "matrix": matrix
        }
