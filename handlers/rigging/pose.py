# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Pose mode handlers for character animation workflow

import bpy
import mathutils
from typing import Dict, Any, List
from handlers.base_handler import BaseHandler
from utils.logger import logger


class SetBonePoseHandler(BaseHandler):
    """Handler for setting bone pose in pose mode"""

    def get_command_name(self) -> str:
        return "set_bone_pose"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "location": {"type": list, "required": False},
            "rotation": {"type": list, "required": False},
            "rotation_mode": {"type": str, "required": False},
            "scale": {"type": list, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set bone pose transforms"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        location = params.get("location")
        rotation = params.get("rotation")
        rotation_mode = params.get("rotation_mode", "XYZ")
        scale = params.get("scale")

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Make armature active and enter pose mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')

        try:
            pose_bone = armature.pose.bones.get(bone_name)
            if not pose_bone:
                raise ValueError(f"Bone '{bone_name}' not found in armature")

            # Set rotation mode
            pose_bone.rotation_mode = rotation_mode

            # Apply transforms
            if location:
                pose_bone.location = location

            if rotation:
                if rotation_mode == 'QUATERNION':
                    pose_bone.rotation_quaternion = rotation
                elif rotation_mode == 'AXIS_ANGLE':
                    pose_bone.rotation_axis_angle = rotation
                else:
                    pose_bone.rotation_euler = rotation

            if scale:
                pose_bone.scale = scale

            logger.info(f"Set pose for bone '{bone_name}'")

            return {
                "pose_set": True,
                "armature_name": armature_name,
                "bone_name": bone_name,
                "location": list(pose_bone.location) if location else None,
                "rotation": list(pose_bone.rotation_euler) if rotation and rotation_mode not in ['QUATERNION', 'AXIS_ANGLE'] else None,
                "scale": list(pose_bone.scale) if scale else None
            }

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')


class GetBonePoseHandler(BaseHandler):
    """Handler for getting bone pose information"""

    def get_command_name(self) -> str:
        return "get_bone_pose"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get bone pose information"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            raise ValueError(f"Bone '{bone_name}' not found in armature")

        # Get world-space matrix
        world_matrix = armature.matrix_world @ pose_bone.matrix

        return {
            "armature_name": armature_name,
            "bone_name": bone_name,
            "location": list(pose_bone.location),
            "rotation_euler": list(pose_bone.rotation_euler),
            "rotation_quaternion": list(pose_bone.rotation_quaternion),
            "rotation_mode": pose_bone.rotation_mode,
            "scale": list(pose_bone.scale),
            "matrix": [list(row) for row in pose_bone.matrix],
            "matrix_basis": [list(row) for row in pose_bone.matrix_basis],
            "head": list(pose_bone.head),
            "tail": list(pose_bone.tail),
            "world_location": list(world_matrix.translation)
        }


class ClearPoseHandler(BaseHandler):
    """Handler for clearing bone poses"""

    def get_command_name(self) -> str:
        return "clear_pose"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_names": {"type": list, "required": False},
            "clear_location": {"type": bool, "required": False},
            "clear_rotation": {"type": bool, "required": False},
            "clear_scale": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Clear bone poses"""
        armature_name = params["armature_name"]
        bone_names = params.get("bone_names")  # None = all bones
        clear_location = params.get("clear_location", True)
        clear_rotation = params.get("clear_rotation", True)
        clear_scale = params.get("clear_scale", True)

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Make armature active and enter pose mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')

        try:
            # Get bones to clear
            if bone_names:
                bones = [armature.pose.bones.get(name) for name in bone_names]
                bones = [b for b in bones if b is not None]
            else:
                bones = armature.pose.bones

            cleared_bones = []

            for pose_bone in bones:
                if clear_location:
                    pose_bone.location = (0, 0, 0)
                if clear_rotation:
                    pose_bone.rotation_euler = (0, 0, 0)
                    pose_bone.rotation_quaternion = (1, 0, 0, 0)
                if clear_scale:
                    pose_bone.scale = (1, 1, 1)
                cleared_bones.append(pose_bone.name)

            logger.info(f"Cleared pose for {len(cleared_bones)} bones")

            return {
                "cleared": True,
                "armature_name": armature_name,
                "bones_cleared": cleared_bones,
                "clear_location": clear_location,
                "clear_rotation": clear_rotation,
                "clear_scale": clear_scale
            }

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')


class ApplyPoseAsRestHandler(BaseHandler):
    """Handler for applying current pose as rest pose"""

    def get_command_name(self) -> str:
        return "apply_pose_as_rest"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Apply current pose as rest pose"""
        armature_name = params["armature_name"]

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Make armature active and enter pose mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')

        try:
            # Select all pose bones
            bpy.ops.pose.select_all(action='SELECT')

            # Apply as rest pose
            bpy.ops.pose.armature_apply()

            logger.info(f"Applied pose as rest for {armature_name}")

            return {
                "applied": True,
                "armature_name": armature_name
            }

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')


class CopyPoseHandler(BaseHandler):
    """Handler for copying pose between bones or armatures"""

    def get_command_name(self) -> str:
        return "copy_pose"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "source_armature": {"type": str, "required": True},
            "target_armature": {"type": str, "required": False},
            "bone_mapping": {"type": dict, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Copy pose from source to target"""
        source_name = params["source_armature"]
        target_name = params.get("target_armature", source_name)
        bone_mapping = params.get("bone_mapping")  # {source_bone: target_bone}

        source_armature = bpy.data.objects.get(source_name)
        if not source_armature or source_armature.type != 'ARMATURE':
            raise ValueError(f"Source armature '{source_name}' not found")

        target_armature = bpy.data.objects.get(target_name)
        if not target_armature or target_armature.type != 'ARMATURE':
            raise ValueError(f"Target armature '{target_name}' not found")

        # If no mapping, use same bone names
        if not bone_mapping:
            bone_mapping = {b.name: b.name for b in source_armature.pose.bones}

        copied_bones = []

        for source_bone_name, target_bone_name in bone_mapping.items():
            source_bone = source_armature.pose.bones.get(source_bone_name)
            target_bone = target_armature.pose.bones.get(target_bone_name)

            if source_bone and target_bone:
                target_bone.location = source_bone.location.copy()
                target_bone.rotation_euler = source_bone.rotation_euler.copy()
                target_bone.rotation_quaternion = source_bone.rotation_quaternion.copy()
                target_bone.scale = source_bone.scale.copy()
                copied_bones.append({
                    "source": source_bone_name,
                    "target": target_bone_name
                })

        logger.info(f"Copied pose for {len(copied_bones)} bones")

        return {
            "copied": True,
            "source_armature": source_name,
            "target_armature": target_name,
            "bones_copied": copied_bones
        }


class GetAllBonePosesHandler(BaseHandler):
    """Handler for getting all bone poses in an armature"""

    def get_command_name(self) -> str:
        return "get_all_bone_poses"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get all bone poses"""
        armature_name = params["armature_name"]

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        poses = {}

        for pose_bone in armature.pose.bones:
            poses[pose_bone.name] = {
                "location": list(pose_bone.location),
                "rotation_euler": list(pose_bone.rotation_euler),
                "rotation_quaternion": list(pose_bone.rotation_quaternion),
                "rotation_mode": pose_bone.rotation_mode,
                "scale": list(pose_bone.scale)
            }

        return {
            "armature_name": armature_name,
            "poses": poses,
            "bone_count": len(poses)
        }
