# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Template handlers for rigging workflow

"""
Template handlers for creating preset rigs and mirroring operations
"""

import bpy
import math
from typing import Dict, Any, List
from handlers.base_handler import BaseHandler
from utils.logger import logger


class CreateHumanoidRigHandler(BaseHandler):
    """Handler for creating a complete humanoid rig"""

    def get_command_name(self) -> str:
        return "create_humanoid_rig"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": False},
            "location": {"type": list, "required": False},
            "scale": {"type": (int, float), "required": False},
            "spine_count": {"type": int, "required": False},
            "finger_count": {"type": int, "required": False},
            "ik_legs": {"type": bool, "required": False},
            "ik_arms": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a complete humanoid rig with IK setup"""
        armature_name = params.get("armature_name", "Humanoid_Rig")
        location = params.get("location", [0, 0, 0])
        scale = params.get("scale", 1.0)
        spine_count = params.get("spine_count", 3)
        finger_count = params.get("finger_count", 5)
        ik_legs = params.get("ik_legs", True)
        ik_arms = params.get("ik_arms", True)

        # Create armature
        armature_data = bpy.data.armatures.new(armature_name)
        armature_obj = bpy.data.objects.new(armature_name, armature_data)
        armature_obj.location = location
        bpy.context.scene.collection.objects.link(armature_obj)

        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        bones_created = []
        ik_targets = []

        try:
            # Reference heights
            hip_height = 1.0 * scale
            shoulder_height = 1.5 * scale
            head_top = 1.85 * scale

            # Root
            root = armature_data.edit_bones.new("root")
            root.head = [0, 0, 0]
            root.tail = [0, 0, 0.1 * scale]
            bones_created.append("root")

            # Hip
            hip = armature_data.edit_bones.new("hip")
            hip.head = [0, 0, hip_height]
            hip.tail = [0, 0, hip_height + 0.1 * scale]
            hip.parent = root
            bones_created.append("hip")

            # Spine chain
            spine_length = (shoulder_height - hip_height - 0.2 * scale) / spine_count
            prev_bone = hip
            for i in range(spine_count):
                spine = armature_data.edit_bones.new(f"spine.{i+1:03d}")
                spine.head = [0, 0, hip_height + 0.1 * scale + spine_length * i]
                spine.tail = [0, 0, hip_height + 0.1 * scale + spine_length * (i + 1)]
                spine.parent = prev_bone
                spine.use_connect = True
                prev_bone = spine
                bones_created.append(spine.name)

            # Chest
            chest = armature_data.edit_bones.new("chest")
            chest.head = prev_bone.tail.copy()
            chest.tail = [0, 0, shoulder_height]
            chest.parent = prev_bone
            chest.use_connect = True
            bones_created.append("chest")

            # Neck
            neck = armature_data.edit_bones.new("neck")
            neck.head = [0, 0, shoulder_height]
            neck.tail = [0, 0, shoulder_height + 0.1 * scale]
            neck.parent = chest
            neck.use_connect = True
            bones_created.append("neck")

            # Head
            head = armature_data.edit_bones.new("head")
            head.head = neck.tail.copy()
            head.tail = [0, 0, head_top]
            head.parent = neck
            head.use_connect = True
            bones_created.append("head")

            # Create legs and arms for both sides
            for side in ['L', 'R']:
                sign = 1 if side == 'L' else -1
                hip_offset = 0.1 * scale * sign

                # Leg bones
                thigh = armature_data.edit_bones.new(f"thigh.{side}")
                thigh.head = [hip_offset, 0, hip_height]
                thigh.tail = [hip_offset, 0, hip_height - 0.45 * scale]
                thigh.parent = hip
                bones_created.append(thigh.name)

                shin = armature_data.edit_bones.new(f"shin.{side}")
                shin.head = thigh.tail.copy()
                shin.tail = [hip_offset, 0, 0.1 * scale]
                shin.parent = thigh
                shin.use_connect = True
                bones_created.append(shin.name)

                foot = armature_data.edit_bones.new(f"foot.{side}")
                foot.head = shin.tail.copy()
                foot.tail = [hip_offset, -0.15 * scale, 0]
                foot.parent = shin
                foot.use_connect = True
                bones_created.append(foot.name)

                toe = armature_data.edit_bones.new(f"toe.{side}")
                toe.head = foot.tail.copy()
                toe.tail = [hip_offset, -0.25 * scale, 0]
                toe.parent = foot
                toe.use_connect = True
                bones_created.append(toe.name)

                # Arm bones
                shoulder_off = 0.15 * scale * sign
                clavicle = armature_data.edit_bones.new(f"clavicle.{side}")
                clavicle.head = [0, 0, shoulder_height - 0.05 * scale]
                clavicle.tail = [shoulder_off, 0, shoulder_height]
                clavicle.parent = chest
                bones_created.append(clavicle.name)

                upper_arm = armature_data.edit_bones.new(f"upper_arm.{side}")
                upper_arm.head = clavicle.tail.copy()
                upper_arm.tail = [shoulder_off + 0.3 * scale * sign, 0, shoulder_height]
                upper_arm.parent = clavicle
                upper_arm.use_connect = True
                bones_created.append(upper_arm.name)

                forearm = armature_data.edit_bones.new(f"forearm.{side}")
                forearm.head = upper_arm.tail.copy()
                forearm.tail = [shoulder_off + 0.55 * scale * sign, 0, shoulder_height]
                forearm.parent = upper_arm
                forearm.use_connect = True
                bones_created.append(forearm.name)

                hand = armature_data.edit_bones.new(f"hand.{side}")
                hand.head = forearm.tail.copy()
                hand.tail = [shoulder_off + 0.65 * scale * sign, 0, shoulder_height]
                hand.parent = forearm
                hand.use_connect = True
                bones_created.append(hand.name)

                # Fingers
                if finger_count > 0:
                    finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky'][:finger_count]
                    for f_idx, fname in enumerate(finger_names):
                        for joint in range(3):
                            joint_name = f"{fname}.{joint+1:02d}.{side}"
                            finger = armature_data.edit_bones.new(joint_name)
                            base_x = shoulder_off + (0.65 + 0.02 * joint) * scale * sign
                            offset_y = (f_idx - 2) * 0.02 * scale
                            finger.head = [base_x, offset_y, shoulder_height]
                            finger.tail = [base_x + 0.02 * scale * sign, offset_y, shoulder_height]
                            if joint == 0:
                                finger.parent = hand
                            else:
                                finger.parent = armature_data.edit_bones.get(f"{fname}.{joint:02d}.{side}")
                                finger.use_connect = True
                            bones_created.append(joint_name)

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')

        # Setup IK
        if ik_legs or ik_arms:
            bpy.ops.object.mode_set(mode='POSE')
            try:
                for side in ['L', 'R']:
                    sign = 1 if side == 'L' else -1

                    if ik_legs:
                        # Leg IK target
                        ik_target = bpy.data.objects.new(f"leg_IK.{side}", None)
                        ik_target.empty_display_type = 'SPHERE'
                        ik_target.empty_display_size = 0.1 * scale
                        ik_target.location = [0.1 * scale * sign, 0, 0.1 * scale]
                        bpy.context.scene.collection.objects.link(ik_target)
                        ik_targets.append(ik_target.name)

                        shin = armature_obj.pose.bones.get(f"shin.{side}")
                        if shin:
                            ik = shin.constraints.new(type='IK')
                            ik.target = ik_target
                            ik.chain_count = 2

                    if ik_arms:
                        ik_target = bpy.data.objects.new(f"arm_IK.{side}", None)
                        ik_target.empty_display_type = 'SPHERE'
                        ik_target.empty_display_size = 0.1 * scale
                        ik_target.location = [0.65 * scale * sign, 0, shoulder_height]
                        bpy.context.scene.collection.objects.link(ik_target)
                        ik_targets.append(ik_target.name)

                        forearm = armature_obj.pose.bones.get(f"forearm.{side}")
                        if forearm:
                            ik = forearm.constraints.new(type='IK')
                            ik.target = ik_target
                            ik.chain_count = 2
            finally:
                bpy.ops.object.mode_set(mode='OBJECT')

        logger.info(f"Created humanoid rig '{armature_name}' with {len(bones_created)} bones")

        return {
            "rig_created": True,
            "armature_name": armature_obj.name,
            "bones_created": bones_created,
            "bone_count": len(bones_created),
            "ik_targets": ik_targets,
            "ik_legs": ik_legs,
            "ik_arms": ik_arms
        }


class CreateSimpleRigHandler(BaseHandler):
    """Handler for creating a simple bone chain rig"""

    def get_command_name(self) -> str:
        return "create_simple_rig"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": False},
            "location": {"type": list, "required": False},
            "bone_count": {"type": int, "required": False},
            "bone_length": {"type": (int, float), "required": False},
            "direction": {"type": str, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a simple bone chain"""
        armature_name = params.get("armature_name", "Simple_Rig")
        location = params.get("location", [0, 0, 0])
        bone_count = params.get("bone_count", 5)
        bone_length = params.get("bone_length", 0.5)
        direction = params.get("direction", "Z")  # X, Y, Z, -X, -Y, -Z

        # Direction vectors
        dir_map = {
            "X": [1, 0, 0], "-X": [-1, 0, 0],
            "Y": [0, 1, 0], "-Y": [0, -1, 0],
            "Z": [0, 0, 1], "-Z": [0, 0, -1]
        }
        dir_vec = dir_map.get(direction.upper(), [0, 0, 1])

        # Create armature
        armature_data = bpy.data.armatures.new(armature_name)
        armature_obj = bpy.data.objects.new(armature_name, armature_data)
        armature_obj.location = location
        bpy.context.scene.collection.objects.link(armature_obj)

        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        bones_created = []

        try:
            prev_bone = None
            for i in range(bone_count):
                bone = armature_data.edit_bones.new(f"bone.{i+1:03d}")
                bone.head = [
                    dir_vec[0] * bone_length * i,
                    dir_vec[1] * bone_length * i,
                    dir_vec[2] * bone_length * i
                ]
                bone.tail = [
                    dir_vec[0] * bone_length * (i + 1),
                    dir_vec[1] * bone_length * (i + 1),
                    dir_vec[2] * bone_length * (i + 1)
                ]
                if prev_bone:
                    bone.parent = prev_bone
                    bone.use_connect = True
                prev_bone = bone
                bones_created.append(bone.name)

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')

        logger.info(f"Created simple rig '{armature_name}' with {bone_count} bones")

        return {
            "rig_created": True,
            "armature_name": armature_obj.name,
            "bones_created": bones_created,
            "bone_count": len(bones_created)
        }


class MirrorBonesHandler(BaseHandler):
    """Handler for mirroring bones from one side to the other"""

    def get_command_name(self) -> str:
        return "mirror_bones"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "source_side": {"type": str, "required": False},
            "target_side": {"type": str, "required": False},
            "bone_names": {"type": list, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Mirror bones from one side to the other"""
        armature_name = params["armature_name"]
        source_side = params.get("source_side", "L")
        target_side = params.get("target_side", "R")
        bone_names = params.get("bone_names")  # None = all bones with source suffix

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        mirrored_bones = []

        try:
            # Get bones to mirror
            if bone_names:
                source_bones = [armature.data.edit_bones.get(name) for name in bone_names]
                source_bones = [b for b in source_bones if b]
            else:
                source_bones = [
                    b for b in armature.data.edit_bones
                    if b.name.endswith(f".{source_side}")
                ]

            for source_bone in source_bones:
                # Create mirrored name
                if source_bone.name.endswith(f".{source_side}"):
                    target_name = source_bone.name[:-len(source_side)-1] + f".{target_side}"
                else:
                    target_name = f"{source_bone.name}.{target_side}"

                # Check if target already exists
                if armature.data.edit_bones.get(target_name):
                    continue

                # Create mirrored bone
                target_bone = armature.data.edit_bones.new(target_name)
                target_bone.head = [-source_bone.head[0], source_bone.head[1], source_bone.head[2]]
                target_bone.tail = [-source_bone.tail[0], source_bone.tail[1], source_bone.tail[2]]
                target_bone.roll = -source_bone.roll
                target_bone.use_connect = source_bone.use_connect
                target_bone.use_deform = source_bone.use_deform

                # Set parent if exists
                if source_bone.parent:
                    parent_name = source_bone.parent.name
                    if parent_name.endswith(f".{source_side}"):
                        mirror_parent_name = parent_name[:-len(source_side)-1] + f".{target_side}"
                    else:
                        mirror_parent_name = parent_name

                    mirror_parent = armature.data.edit_bones.get(mirror_parent_name)
                    if mirror_parent:
                        target_bone.parent = mirror_parent

                mirrored_bones.append(target_name)

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')

        logger.info(f"Mirrored {len(mirrored_bones)} bones in armature '{armature_name}'")

        return {
            "mirrored": True,
            "armature_name": armature_name,
            "source_side": source_side,
            "target_side": target_side,
            "bones_mirrored": mirrored_bones,
            "count": len(mirrored_bones)
        }
