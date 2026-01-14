# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Version: 2.1.0 - Added transform/delete bone handlers for movie production workflow

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.logger import logger

HANDLER_VERSION = "2.1.0"


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


class TransformBoneHandler(BaseHandler):
    """Handler for transforming bones in edit mode"""

    def get_command_name(self) -> str:
        return "transform_bone"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "head": {"type": list, "required": False},
            "tail": {"type": list, "required": False},
            "roll": {"type": (int, float), "required": False},
            "length": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Transform a bone in edit mode"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        head = params.get("head")
        tail = params.get("tail")
        roll = params.get("roll")
        length = params.get("length")

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Enter edit mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        try:
            edit_bone = armature.data.edit_bones.get(bone_name)
            if not edit_bone:
                raise ValueError(f"Bone '{bone_name}' not found")

            # Apply transforms
            if head:
                edit_bone.head = head
            if tail:
                edit_bone.tail = tail
            if roll is not None:
                edit_bone.roll = roll
            if length is not None:
                # Adjust tail to match length while keeping direction
                direction = (edit_bone.tail - edit_bone.head).normalized()
                edit_bone.tail = edit_bone.head + direction * length

            logger.info(f"Transformed bone '{bone_name}'")

            return {
                "transformed": True,
                "armature_name": armature_name,
                "bone_name": bone_name,
                "head": list(edit_bone.head),
                "tail": list(edit_bone.tail),
                "roll": edit_bone.roll,
                "length": edit_bone.length
            }

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')


class DeleteBoneHandler(BaseHandler):
    """Handler for deleting bones"""

    def get_command_name(self) -> str:
        return "delete_bone"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "delete_children": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Delete a bone from an armature"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        delete_children = params.get("delete_children", False)

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Enter edit mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        try:
            edit_bone = armature.data.edit_bones.get(bone_name)
            if not edit_bone:
                raise ValueError(f"Bone '{bone_name}' not found")

            deleted_bones = [bone_name]

            # Get children if needed
            if delete_children:
                children = list(edit_bone.children_recursive)
                deleted_bones.extend([c.name for c in children])

            # Delete the bone (children are automatically deleted if parent is deleted)
            armature.data.edit_bones.remove(edit_bone)

            logger.info(f"Deleted bone(s): {deleted_bones}")

            return {
                "deleted": True,
                "armature_name": armature_name,
                "bones_deleted": deleted_bones,
                "count": len(deleted_bones)
            }

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')


class SetBoneParentHandler(BaseHandler):
    """Handler for setting bone parent relationships"""

    def get_command_name(self) -> str:
        return "set_bone_parent"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "parent_name": {"type": str, "required": False},
            "use_connect": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set or change bone parent"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        parent_name = params.get("parent_name")  # None to unparent
        use_connect = params.get("use_connect", False)

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Enter edit mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        try:
            edit_bone = armature.data.edit_bones.get(bone_name)
            if not edit_bone:
                raise ValueError(f"Bone '{bone_name}' not found")

            if parent_name:
                parent_bone = armature.data.edit_bones.get(parent_name)
                if not parent_bone:
                    raise ValueError(f"Parent bone '{parent_name}' not found")
                edit_bone.parent = parent_bone
                edit_bone.use_connect = use_connect
            else:
                edit_bone.parent = None

            logger.info(f"Set parent of '{bone_name}' to '{parent_name}'")

            return {
                "parent_set": True,
                "armature_name": armature_name,
                "bone_name": bone_name,
                "parent_name": parent_name,
                "use_connect": use_connect
            }

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')


class DuplicateBoneHandler(BaseHandler):
    """Handler for duplicating bones"""

    def get_command_name(self) -> str:
        return "duplicate_bone"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "new_name": {"type": str, "required": True},
            "offset": {"type": list, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Duplicate a bone"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        new_name = params["new_name"]
        offset = params.get("offset", [0, 0, 0])

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Enter edit mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        try:
            source_bone = armature.data.edit_bones.get(bone_name)
            if not source_bone:
                raise ValueError(f"Bone '{bone_name}' not found")

            # Create new bone
            new_bone = armature.data.edit_bones.new(new_name)
            new_bone.head = [source_bone.head[i] + offset[i] for i in range(3)]
            new_bone.tail = [source_bone.tail[i] + offset[i] for i in range(3)]
            new_bone.roll = source_bone.roll

            # Copy properties
            new_bone.use_deform = source_bone.use_deform
            new_bone.use_connect = False

            logger.info(f"Duplicated bone '{bone_name}' as '{new_name}'")

            return {
                "duplicated": True,
                "armature_name": armature_name,
                "source_bone": bone_name,
                "new_bone": new_bone.name,
                "head": list(new_bone.head),
                "tail": list(new_bone.tail)
            }

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')
