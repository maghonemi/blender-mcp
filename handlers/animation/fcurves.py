# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# F-curve handlers for advanced animation control

import bpy
from typing import Dict, Any, List
from handlers.base_handler import BaseHandler
from utils.logger import logger


class GetFCurvesHandler(BaseHandler):
    """Handler for getting F-curve information from an object"""

    def get_command_name(self) -> str:
        return "get_fcurves"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "data_path_filter": {"type": str, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get F-curves from an object"""
        object_name = params["object_name"]
        data_path_filter = params.get("data_path_filter")

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            return {
                "object_name": object_name,
                "fcurves": [],
                "count": 0,
                "message": "Object has no animation data"
            }

        fcurves_info = []
        action = obj.animation_data.action

        # Check if fcurves attribute exists (Blender version compatibility)
        if not hasattr(action, 'fcurves'):
            return {
                "object_name": object_name,
                "fcurves": [],
                "count": 0,
                "message": "Action does not have fcurves attribute (may need to update Blender or action)"
            }

        for fcurve in action.fcurves:
            # Filter by data path if specified
            if data_path_filter and data_path_filter not in fcurve.data_path:
                continue

            keyframes = []
            for keyframe in fcurve.keyframe_points:
                keyframes.append({
                    "frame": keyframe.co[0],
                    "value": keyframe.co[1],
                    "interpolation": keyframe.interpolation,
                    "handle_left": list(keyframe.handle_left),
                    "handle_right": list(keyframe.handle_right),
                    "handle_left_type": keyframe.handle_left_type,
                    "handle_right_type": keyframe.handle_right_type
                })

            fcurve_info = {
                "data_path": fcurve.data_path,
                "array_index": fcurve.array_index,
                "keyframe_count": len(fcurve.keyframe_points),
                "keyframes": keyframes,
                "extrapolation": fcurve.extrapolation,
                "muted": fcurve.mute
            }

            # Get modifiers if any
            if fcurve.modifiers:
                fcurve_info["modifiers"] = [
                    {"name": mod.name, "type": mod.type, "muted": mod.mute}
                    for mod in fcurve.modifiers
                ]

            fcurves_info.append(fcurve_info)

        return {
            "object_name": object_name,
            "action_name": action.name,
            "fcurves": fcurves_info,
            "count": len(fcurves_info)
        }


class SetFCurveInterpolationHandler(BaseHandler):
    """Handler for setting F-curve interpolation mode"""

    def get_command_name(self) -> str:
        return "set_fcurve_interpolation"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "data_path": {"type": str, "required": True},
            "array_index": {"type": int, "required": False},
            "interpolation": {"type": str, "required": True},
            "frame_start": {"type": int, "required": False},
            "frame_end": {"type": int, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set interpolation mode for F-curve keyframes"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        array_index = params.get("array_index", 0)
        interpolation = params["interpolation"].upper()
        frame_start = params.get("frame_start")
        frame_end = params.get("frame_end")

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no animation data")

        action = obj.animation_data.action

        # Find the F-curve
        fcurve = action.fcurves.find(data_path, index=array_index)
        if not fcurve:
            raise ValueError(f"F-curve not found for {data_path}[{array_index}]")

        # Valid interpolation types
        valid_types = ['CONSTANT', 'LINEAR', 'BEZIER', 'SINE', 'QUAD', 'CUBIC',
                       'QUART', 'QUINT', 'EXPO', 'CIRC', 'BACK', 'BOUNCE', 'ELASTIC']

        if interpolation not in valid_types:
            raise ValueError(f"Invalid interpolation type. Must be one of: {valid_types}")

        keyframes_modified = 0

        for keyframe in fcurve.keyframe_points:
            # Check frame range if specified
            if frame_start and keyframe.co[0] < frame_start:
                continue
            if frame_end and keyframe.co[0] > frame_end:
                continue

            keyframe.interpolation = interpolation
            keyframes_modified += 1

        logger.info(f"Set {keyframes_modified} keyframes to {interpolation} interpolation")

        return {
            "modified": True,
            "object_name": object_name,
            "data_path": data_path,
            "interpolation": interpolation,
            "keyframes_modified": keyframes_modified
        }


class SetFCurveHandlesHandler(BaseHandler):
    """Handler for setting F-curve keyframe handles"""

    def get_command_name(self) -> str:
        return "set_fcurve_handles"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "data_path": {"type": str, "required": True},
            "array_index": {"type": int, "required": False},
            "handle_type": {"type": str, "required": True},
            "frame": {"type": int, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set handle type for F-curve keyframes"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        array_index = params.get("array_index", 0)
        handle_type = params["handle_type"].upper()
        frame = params.get("frame")

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no animation data")

        action = obj.animation_data.action
        fcurve = action.fcurves.find(data_path, index=array_index)

        if not fcurve:
            raise ValueError(f"F-curve not found for {data_path}[{array_index}]")

        # Valid handle types
        valid_types = ['FREE', 'ALIGNED', 'VECTOR', 'AUTO', 'AUTO_CLAMPED']

        if handle_type not in valid_types:
            raise ValueError(f"Invalid handle type. Must be one of: {valid_types}")

        keyframes_modified = 0

        for keyframe in fcurve.keyframe_points:
            if frame and abs(keyframe.co[0] - frame) > 0.01:
                continue

            keyframe.handle_left_type = handle_type
            keyframe.handle_right_type = handle_type
            keyframes_modified += 1

        logger.info(f"Set handles to {handle_type} for {keyframes_modified} keyframes")

        return {
            "modified": True,
            "object_name": object_name,
            "data_path": data_path,
            "handle_type": handle_type,
            "keyframes_modified": keyframes_modified
        }


class AddFCurveModifierHandler(BaseHandler):
    """Handler for adding modifiers to F-curves"""

    def get_command_name(self) -> str:
        return "add_fcurve_modifier"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "data_path": {"type": str, "required": True},
            "array_index": {"type": int, "required": False},
            "modifier_type": {"type": str, "required": True},
            "settings": {"type": dict, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Add a modifier to an F-curve"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        array_index = params.get("array_index", 0)
        modifier_type = params["modifier_type"].upper()
        settings = params.get("settings", {})

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no animation data")

        action = obj.animation_data.action
        fcurve = action.fcurves.find(data_path, index=array_index)

        if not fcurve:
            raise ValueError(f"F-curve not found for {data_path}[{array_index}]")

        # Valid modifier types
        valid_types = ['NULL', 'GENERATOR', 'FNGENERATOR', 'ENVELOPE', 'CYCLES',
                       'NOISE', 'LIMITS', 'STEPPED']

        if modifier_type not in valid_types:
            raise ValueError(f"Invalid modifier type. Must be one of: {valid_types}")

        # Add modifier
        modifier = fcurve.modifiers.new(type=modifier_type)

        # Apply settings
        for key, value in settings.items():
            if hasattr(modifier, key):
                setattr(modifier, key, value)

        logger.info(f"Added {modifier_type} modifier to F-curve {data_path}")

        return {
            "modifier_added": True,
            "object_name": object_name,
            "data_path": data_path,
            "modifier_type": modifier_type
        }


class RemoveFCurveModifierHandler(BaseHandler):
    """Handler for removing F-curve modifiers"""

    def get_command_name(self) -> str:
        return "remove_fcurve_modifier"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "data_path": {"type": str, "required": True},
            "array_index": {"type": int, "required": False},
            "modifier_index": {"type": int, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Remove a modifier from an F-curve"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        array_index = params.get("array_index", 0)
        modifier_index = params.get("modifier_index", 0)

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no animation data")

        action = obj.animation_data.action
        fcurve = action.fcurves.find(data_path, index=array_index)

        if not fcurve:
            raise ValueError(f"F-curve not found for {data_path}[{array_index}]")

        if modifier_index >= len(fcurve.modifiers):
            raise ValueError(f"Modifier index {modifier_index} out of range")

        modifier = fcurve.modifiers[modifier_index]
        modifier_type = modifier.type
        fcurve.modifiers.remove(modifier)

        logger.info(f"Removed {modifier_type} modifier from F-curve {data_path}")

        return {
            "modifier_removed": True,
            "object_name": object_name,
            "data_path": data_path,
            "modifier_type": modifier_type
        }


class SmoothFCurveHandler(BaseHandler):
    """Handler for smoothing F-curve keyframes"""

    def get_command_name(self) -> str:
        return "smooth_fcurve"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "data_path": {"type": str, "required": False},
            "iterations": {"type": int, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Smooth F-curve keyframes"""
        object_name = params["object_name"]
        data_path = params.get("data_path")
        iterations = params.get("iterations", 1)

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no animation data")

        # Select object and enter graph editor context
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        action = obj.animation_data.action
        fcurves_smoothed = []

        for fcurve in action.fcurves:
            if data_path and data_path not in fcurve.data_path:
                continue

            # Select all keyframes on this fcurve
            for keyframe in fcurve.keyframe_points:
                keyframe.select_control_point = True

            fcurves_smoothed.append(f"{fcurve.data_path}[{fcurve.array_index}]")

        # Apply smoothing
        for _ in range(iterations):
            try:
                # This requires graph editor context, may not work in all cases
                # Fallback: manually smooth values
                for fcurve in action.fcurves:
                    if data_path and data_path not in fcurve.data_path:
                        continue

                    points = fcurve.keyframe_points
                    if len(points) < 3:
                        continue

                    # Simple moving average smoothing
                    values = [p.co[1] for p in points]
                    smoothed = values.copy()

                    for i in range(1, len(values) - 1):
                        smoothed[i] = (values[i-1] + values[i] + values[i+1]) / 3

                    for i, point in enumerate(points):
                        point.co[1] = smoothed[i]

            except Exception as e:
                logger.warning(f"Smoothing fallback used: {e}")

        logger.info(f"Smoothed {len(fcurves_smoothed)} F-curves")

        return {
            "smoothed": True,
            "object_name": object_name,
            "fcurves_smoothed": fcurves_smoothed,
            "iterations": iterations
        }
