# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Animation baking handlers for converting constraints to keyframes

import bpy
from typing import Dict, Any, List
from handlers.base_handler import BaseHandler
from utils.logger import logger


class BakeAnimationHandler(BaseHandler):
    """Handler for baking animation (converting constraints/drivers to keyframes)"""

    def get_command_name(self) -> str:
        return "bake_animation"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "frame_start": {"type": int, "required": True},
            "frame_end": {"type": int, "required": True},
            "step": {"type": int, "required": False},
            "only_selected": {"type": bool, "required": False},
            "visual_keying": {"type": bool, "required": False},
            "clear_constraints": {"type": bool, "required": False},
            "clear_parents": {"type": bool, "required": False},
            "bake_types": {"type": list, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Bake object animation"""
        object_name = params["object_name"]
        frame_start = params["frame_start"]
        frame_end = params["frame_end"]
        step = params.get("step", 1)
        only_selected = params.get("only_selected", False)
        visual_keying = params.get("visual_keying", True)
        clear_constraints = params.get("clear_constraints", False)
        clear_parents = params.get("clear_parents", False)
        bake_types = params.get("bake_types", ['LOCATION', 'ROTATION', 'SCALE'])

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        # Select object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Convert bake_types to set for the operator
        do_location = 'LOCATION' in bake_types
        do_rotation = 'ROTATION' in bake_types
        do_scale = 'SCALE' in bake_types

        # Bake animation
        bpy.ops.nla.bake(
            frame_start=frame_start,
            frame_end=frame_end,
            step=step,
            only_selected=only_selected,
            visual_keying=visual_keying,
            clear_constraints=clear_constraints,
            clear_parents=clear_parents,
            use_current_action=True,
            bake_types={'OBJECT'} if obj.type != 'ARMATURE' else {'POSE'}
        )

        # Count keyframes created
        keyframe_count = 0
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                keyframe_count += len(fcurve.keyframe_points)

        logger.info(f"Baked animation for '{object_name}' from frame {frame_start} to {frame_end}")

        return {
            "baked": True,
            "object_name": object_name,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "frame_count": frame_end - frame_start + 1,
            "keyframes_created": keyframe_count,
            "clear_constraints": clear_constraints,
            "clear_parents": clear_parents
        }


class BakeArmatureAnimationHandler(BaseHandler):
    """Handler for baking armature/pose animation"""

    def get_command_name(self) -> str:
        return "bake_armature_animation"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "armature_name": {"type": str, "required": True},
            "frame_start": {"type": int, "required": True},
            "frame_end": {"type": int, "required": True},
            "step": {"type": int, "required": False},
            "bone_names": {"type": list, "required": False},
            "visual_keying": {"type": bool, "required": False},
            "clear_constraints": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Bake armature pose animation"""
        armature_name = params["armature_name"]
        frame_start = params["frame_start"]
        frame_end = params["frame_end"]
        step = params.get("step", 1)
        bone_names = params.get("bone_names")  # None = all bones
        visual_keying = params.get("visual_keying", True)
        clear_constraints = params.get("clear_constraints", False)

        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Select armature and enter pose mode
        bpy.ops.object.select_all(action='DESELECT')
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')

        try:
            # Select bones
            if bone_names:
                bpy.ops.pose.select_all(action='DESELECT')
                for bone_name in bone_names:
                    pose_bone = armature.pose.bones.get(bone_name)
                    if pose_bone:
                        pose_bone.bone.select = True
                only_selected = True
            else:
                bpy.ops.pose.select_all(action='SELECT')
                only_selected = False

            # Bake
            bpy.ops.nla.bake(
                frame_start=frame_start,
                frame_end=frame_end,
                step=step,
                only_selected=only_selected,
                visual_keying=visual_keying,
                clear_constraints=clear_constraints,
                clear_parents=False,
                use_current_action=True,
                bake_types={'POSE'}
            )

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')

        # Count results
        keyframe_count = 0
        bones_baked = []
        if armature.animation_data and armature.animation_data.action:
            for fcurve in armature.animation_data.action.fcurves:
                keyframe_count += len(fcurve.keyframe_points)
                # Extract bone name from data path
                if 'pose.bones' in fcurve.data_path:
                    bone_name = fcurve.data_path.split('"')[1]
                    if bone_name not in bones_baked:
                        bones_baked.append(bone_name)

        logger.info(f"Baked {len(bones_baked)} bones for '{armature_name}'")

        return {
            "baked": True,
            "armature_name": armature_name,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "bones_baked": bones_baked,
            "bone_count": len(bones_baked),
            "keyframes_created": keyframe_count
        }


class SampleAnimationHandler(BaseHandler):
    """Handler for sampling animation at regular intervals"""

    def get_command_name(self) -> str:
        return "sample_animation"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "frame_start": {"type": int, "required": False},
            "frame_end": {"type": int, "required": False},
            "sample_rate": {"type": int, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Sample animation at regular intervals (adds keyframes)"""
        object_name = params["object_name"]
        frame_start = params.get("frame_start")
        frame_end = params.get("frame_end")
        sample_rate = params.get("sample_rate", 1)

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no animation data")

        action = obj.animation_data.action

        # Use action frame range if not specified
        if frame_start is None:
            frame_start = int(action.frame_range[0])
        if frame_end is None:
            frame_end = int(action.frame_range[1])

        keyframes_added = 0

        # Sample each fcurve
        for fcurve in action.fcurves:
            for frame in range(frame_start, frame_end + 1, sample_rate):
                # Evaluate curve at this frame
                value = fcurve.evaluate(frame)

                # Add keyframe
                fcurve.keyframe_points.insert(frame, value)
                keyframes_added += 1

        logger.info(f"Sampled animation for '{object_name}' at rate {sample_rate}")

        return {
            "sampled": True,
            "object_name": object_name,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "sample_rate": sample_rate,
            "keyframes_added": keyframes_added
        }


class CleanKeyframesHandler(BaseHandler):
    """Handler for cleaning up redundant keyframes"""

    def get_command_name(self) -> str:
        return "clean_keyframes"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "threshold": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Clean up redundant keyframes"""
        object_name = params["object_name"]
        threshold = params.get("threshold", 0.001)

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no animation data")

        action = obj.animation_data.action
        keyframes_removed = 0

        for fcurve in action.fcurves:
            # Get keyframes to potentially remove
            keyframes_to_remove = []

            points = list(fcurve.keyframe_points)
            for i in range(1, len(points) - 1):
                prev_val = points[i-1].co[1]
                curr_val = points[i].co[1]
                next_val = points[i+1].co[1]

                # Check if this keyframe can be interpolated from neighbors
                expected = (prev_val + next_val) / 2
                if abs(curr_val - expected) < threshold:
                    keyframes_to_remove.append(points[i])

            # Remove redundant keyframes
            for kf in keyframes_to_remove:
                fcurve.keyframe_points.remove(kf)
                keyframes_removed += 1

        logger.info(f"Cleaned {keyframes_removed} redundant keyframes from '{object_name}'")

        return {
            "cleaned": True,
            "object_name": object_name,
            "keyframes_removed": keyframes_removed,
            "threshold": threshold
        }
