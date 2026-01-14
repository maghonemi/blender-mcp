# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Version: 2.0.2 - Fixed bone handler for Blender 5.0

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.logger import logger

HANDLER_VERSION = "2.0.2"


class CreateBoneHandler(BaseHandler):
    """Handler for creating bones"""
    
    def get_command_name(self) -> str:
        return "create_bone"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "head": {"type": list, "required": True},
            "tail": {"type": list, "required": True},
            "parent": {"type": str, "required": False},
            "roll": {"type": float, "required": False}
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
        
        # Enter edit mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            bone = armature.data.edit_bones.new(bone_name)
            bone.head = head
            bone.tail = tail
            bone.roll = roll
            
            if parent:
                parent_bone = armature.data.edit_bones.get(parent)
                if parent_bone:
                    bone.parent = parent_bone
        finally:
            bpy.ops.object.mode_set(mode='OBJECT')
        
        return {"bone_created": True, "bone_name": bone_name}


class GetBoneInfoHandler(BaseHandler):
    """Handler for getting bone information - works in object mode"""
    
    def get_command_name(self) -> str:
        return "get_bone_info"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True}
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get bone information safely"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        
        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")
        
        # Get bone from armature data
        bone = armature.data.bones.get(bone_name)
        if not bone:
            raise ValueError(f"Bone '{bone_name}' not found")
        
        # Get basic info that's always available
        result = {
            "name": bone.name,
            "parent": bone.parent.name if bone.parent else None,
            "children": [c.name for c in bone.children],
            "length": bone.length
        }
        
        # Get head/tail - use head_local/tail_local which are always available
        try:
            result["head"] = [bone.head_local.x, bone.head_local.y, bone.head_local.z]
            result["tail"] = [bone.tail_local.x, bone.tail_local.y, bone.tail_local.z]
        except Exception as e:
            logger.warning(f"Could not get head/tail: {e}")
            result["head"] = [0, 0, 0]
            result["tail"] = [0, 1, 0]
        
        # Get roll - need to enter edit mode briefly
        result["roll"] = 0.0
        try:
            current_active = bpy.context.view_layer.objects.active
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')
            
            try:
                edit_bone = armature.data.edit_bones.get(bone_name)
                if edit_bone:
                    result["roll"] = edit_bone.roll
            finally:
                bpy.ops.object.mode_set(mode='OBJECT')
                if current_active:
                    bpy.context.view_layer.objects.active = current_active
        except Exception as e:
            logger.warning(f"Could not get roll: {e}")
        
        # Get matrix if available
        try:
            if hasattr(bone, 'matrix_local'):
                result["matrix"] = [list(row) for row in bone.matrix_local]
            else:
                result["matrix"] = None
        except:
            result["matrix"] = None
        
        return result
