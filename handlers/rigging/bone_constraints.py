# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Bone constraint handlers for rigging workflow

import bpy
from typing import Dict, Any, List
from handlers.base_handler import BaseHandler
from utils.logger import logger


class AddBoneConstraintHandler(BaseHandler):
    """Handler for adding constraints to bones in pose mode"""

    def get_command_name(self) -> str:
        return "add_bone_constraint"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "constraint_type": {"type": str, "required": True},
            "constraint_name": {"type": str, "required": True},
            "target": {"type": str, "required": False},
            "subtarget": {"type": str, "required": False},
            "settings": {"type": dict, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Add a constraint to a pose bone"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        constraint_type = params["constraint_type"]
        constraint_name = params["constraint_name"]
        target = params.get("target")
        subtarget = params.get("subtarget")
        settings = params.get("settings", {})

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            raise ValueError(f"Bone '{bone_name}' not found in armature")

        # Add constraint
        constraint = pose_bone.constraints.new(type=constraint_type)
        constraint.name = constraint_name

        # Set target if provided
        if target:
            target_obj = bpy.data.objects.get(target)
            if target_obj:
                constraint.target = target_obj

                # Set subtarget (bone name) if provided
                if subtarget and target_obj.type == 'ARMATURE':
                    constraint.subtarget = subtarget

        # Apply additional settings
        for key, value in settings.items():
            if hasattr(constraint, key):
                setattr(constraint, key, value)

        logger.info(f"Added {constraint_type} constraint to bone '{bone_name}'")

        return {
            "constraint_added": True,
            "armature_name": armature_name,
            "bone_name": bone_name,
            "constraint_name": constraint_name,
            "constraint_type": constraint_type
        }


class SetupIKChainHandler(BaseHandler):
    """Handler for setting up an IK chain with one command"""

    def get_command_name(self) -> str:
        return "setup_ik_chain"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "chain_tip_bone": {"type": str, "required": True},
            "chain_length": {"type": int, "required": True},
            "target_name": {"type": str, "required": False},
            "pole_target_name": {"type": str, "required": False},
            "pole_angle": {"type": (int, float), "required": False},
            "create_targets": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set up an IK chain on a bone"""
        armature_name = params["armature_name"]
        chain_tip_bone = params["chain_tip_bone"]
        chain_length = params["chain_length"]
        target_name = params.get("target_name")
        pole_target_name = params.get("pole_target_name")
        pole_angle = params.get("pole_angle", 0)
        create_targets = params.get("create_targets", True)

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        pose_bone = armature.pose.bones.get(chain_tip_bone)
        if not pose_bone:
            raise ValueError(f"Bone '{chain_tip_bone}' not found")

        # Get world position of the bone tail for target placement
        bone_tail_world = armature.matrix_world @ pose_bone.tail

        # Create IK target if needed
        ik_target = None
        if target_name:
            ik_target = bpy.data.objects.get(target_name)
        elif create_targets:
            # Create an empty as IK target
            bpy.ops.object.empty_add(type='SPHERE', location=bone_tail_world)
            ik_target = bpy.context.active_object
            ik_target.name = f"IK_Target_{chain_tip_bone}"
            ik_target.empty_display_size = 0.2
            target_name = ik_target.name

        # Create pole target if needed
        pole_target = None
        if pole_target_name:
            pole_target = bpy.data.objects.get(pole_target_name)
        elif create_targets and chain_length > 1:
            # Calculate pole position (offset from middle of chain)
            mid_bone = pose_bone
            for _ in range(chain_length // 2):
                if mid_bone.parent:
                    mid_bone = mid_bone.parent
            mid_pos = armature.matrix_world @ mid_bone.head
            pole_pos = mid_pos + mathutils.Vector((0, -1, 0))  # Offset backwards

            bpy.ops.object.empty_add(type='SPHERE', location=pole_pos)
            pole_target = bpy.context.active_object
            pole_target.name = f"IK_Pole_{chain_tip_bone}"
            pole_target.empty_display_size = 0.15
            pole_target_name = pole_target.name

        # Add IK constraint
        ik_constraint = pose_bone.constraints.new(type='IK')
        ik_constraint.name = f"IK_{chain_tip_bone}"
        ik_constraint.chain_count = chain_length

        if ik_target:
            ik_constraint.target = ik_target

        if pole_target:
            ik_constraint.pole_target = pole_target
            ik_constraint.pole_angle = pole_angle

        logger.info(f"Set up IK chain on '{chain_tip_bone}' with length {chain_length}")

        return {
            "ik_setup": True,
            "armature_name": armature_name,
            "chain_tip_bone": chain_tip_bone,
            "chain_length": chain_length,
            "ik_target": target_name,
            "pole_target": pole_target_name,
            "constraint_name": ik_constraint.name
        }


class ModifyBoneConstraintHandler(BaseHandler):
    """Handler for modifying bone constraints"""

    def get_command_name(self) -> str:
        return "modify_bone_constraint"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "constraint_name": {"type": str, "required": True},
            "settings": {"type": dict, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Modify a bone constraint"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        constraint_name = params["constraint_name"]
        settings = params["settings"]

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            raise ValueError(f"Bone '{bone_name}' not found")

        constraint = pose_bone.constraints.get(constraint_name)
        if not constraint:
            raise ValueError(f"Constraint '{constraint_name}' not found on bone")

        # Apply settings
        for key, value in settings.items():
            if hasattr(constraint, key):
                setattr(constraint, key, value)

        logger.info(f"Modified constraint '{constraint_name}' on bone '{bone_name}'")

        return {
            "modified": True,
            "armature_name": armature_name,
            "bone_name": bone_name,
            "constraint_name": constraint_name
        }


class RemoveBoneConstraintHandler(BaseHandler):
    """Handler for removing bone constraints"""

    def get_command_name(self) -> str:
        return "remove_bone_constraint"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True},
            "constraint_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Remove a constraint from a bone"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]
        constraint_name = params["constraint_name"]

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            raise ValueError(f"Bone '{bone_name}' not found")

        constraint = pose_bone.constraints.get(constraint_name)
        if not constraint:
            raise ValueError(f"Constraint '{constraint_name}' not found")

        pose_bone.constraints.remove(constraint)

        logger.info(f"Removed constraint '{constraint_name}' from bone '{bone_name}'")

        return {
            "removed": True,
            "armature_name": armature_name,
            "bone_name": bone_name,
            "constraint_name": constraint_name
        }


class GetBoneConstraintsHandler(BaseHandler):
    """Handler for getting all constraints on a bone"""

    def get_command_name(self) -> str:
        return "get_bone_constraints"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "bone_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get all constraints on a bone"""
        armature_name = params["armature_name"]
        bone_name = params["bone_name"]

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            raise ValueError(f"Bone '{bone_name}' not found")

        constraints = []
        for constraint in pose_bone.constraints:
            constraint_info = {
                "name": constraint.name,
                "type": constraint.type,
                "enabled": constraint.enabled,
                "influence": constraint.influence
            }

            # Add target info if available
            if hasattr(constraint, 'target') and constraint.target:
                constraint_info["target"] = constraint.target.name
            if hasattr(constraint, 'subtarget'):
                constraint_info["subtarget"] = constraint.subtarget

            constraints.append(constraint_info)

        return {
            "armature_name": armature_name,
            "bone_name": bone_name,
            "constraints": constraints,
            "count": len(constraints)
        }


# Import mathutils for SetupIKChainHandler
import mathutils
