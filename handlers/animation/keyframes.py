# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any, List, Optional
from handlers.base_handler import BaseHandler
from utils.error_handler import ErrorCode
from utils.validation import OBJECT_NAME_SCHEMA, FRAME_SCHEMA, DATA_PATH_SCHEMA, validate_frame
from utils.logger import logger

class CreateKeyframeHandler(BaseHandler):
    """Handler for creating keyframes"""
    
    def get_command_name(self) -> str:
        return "create_keyframe"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            **DATA_PATH_SCHEMA,
            **FRAME_SCHEMA,
            "value": {
                "type": (int, float, list),
                "required": True
            },
            "interpolation": {
                "type": str,
                "required": False
            },
            "keyframe_type": {
                "type": str,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a keyframe"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        frame = params["frame"]
        value = params["value"]
        interpolation = params.get("interpolation", "BEZIER")
        keyframe_type = params.get("keyframe_type", "KEYFRAME")
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        # Ensure animation data exists
        if not obj.animation_data:
            obj.animation_data_create()
        
        # Ensure action exists
        if not obj.animation_data.action:
            action = bpy.data.actions.new(name=f"{object_name}_action")
            obj.animation_data.action = action
        
        # Set the value first
        if isinstance(value, list):
            # Handle vector properties
            if data_path.endswith(".x"):
                # Single component X
                obj.location[0] = value[0] if len(value) > 0 else 0
            elif data_path.endswith(".y"):
                # Single component Y
                obj.location[1] = value[0] if len(value) > 0 else 0
            elif data_path.endswith(".z"):
                # Single component Z
                obj.location[2] = value[0] if len(value) > 0 else 0
            else:
                # Full vector - determine which property
                base_path = data_path.split(".")[0]
                if base_path == "location":
                    obj.location = value[:3]
                elif base_path == "scale":
                    obj.scale = value[:3]
                elif base_path == "rotation_euler":
                    obj.rotation_euler = value[:3]
                else:
                    attr = getattr(obj, base_path)
                    for i, v in enumerate(value):
                        if i < len(attr):
                            attr[i] = v
        else:
            # Single value - handle component paths
            if data_path.endswith(".x"):
                obj.location[0] = value
            elif data_path.endswith(".y"):
                obj.location[1] = value
            elif data_path.endswith(".z"):
                obj.location[2] = value
            else:
                setattr(obj, data_path, value)
        
        # Insert keyframe
        obj.keyframe_insert(
            data_path=data_path,
            frame=frame,
            options={'INSERTKEY_NEEDED'}
        )
        
        # Update action to ensure fcurves are available
        action = obj.animation_data.action
        if action:
            # Force update
            action.update()
            
            # Get the F-curve to set interpolation
            if hasattr(action, 'fcurves'):
                try:
                    for fcurve in action.fcurves:
                        if fcurve.data_path == data_path:
                            for keyframe in fcurve.keyframe_points:
                                if abs(keyframe.co[0] - frame) < 0.001:
                                    keyframe.interpolation = interpolation
                                    break
                except (AttributeError, TypeError):
                    # fcurves might not be accessible yet, skip interpolation setting
                    pass
        
        # Get keyframe count safely
        keyframe_count = 0
        try:
            if obj.animation_data and obj.animation_data.action:
                action = obj.animation_data.action
                if hasattr(action, 'fcurves') and action.fcurves:
                    for fcurve in action.fcurves:
                        if fcurve.data_path == data_path:
                            keyframe_count = len(fcurve.keyframe_points)
                            break
        except:
            pass
        
        return {
            "keyframe_created": True,
            "frame": frame,
            "value": value,
            "fcurve": {
                "data_path": data_path,
                "keyframe_count": keyframe_count
            }
        }

class DeleteKeyframeHandler(BaseHandler):
    """Handler for deleting keyframes"""
    
    def get_command_name(self) -> str:
        return "delete_keyframe"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            **DATA_PATH_SCHEMA,
            "frame": {
                "type": int,
                "required": False
            },
            "frame_range": {
                "type": list,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Delete keyframe(s)"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        frame = params.get("frame")
        frame_range = params.get("frame_range")
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        if frame_range:
            # Delete range
            obj.keyframe_delete(
                data_path=data_path,
                frame_range=(frame_range[0], frame_range[1])
            )
            return {"deleted": True, "frame_range": frame_range}
        elif frame:
            # Delete single frame
            obj.keyframe_delete(data_path=data_path, frame=frame)
            return {"deleted": True, "frame": frame}
        else:
            # Delete all keyframes for this data path
            obj.keyframe_delete(data_path=data_path)
            return {"deleted": True, "data_path": data_path}

class GetKeyframesHandler(BaseHandler):
    """Handler for getting keyframes"""
    
    def get_command_name(self) -> str:
        return "get_keyframes"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            **DATA_PATH_SCHEMA,
            "frame_range": {
                "type": list,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get keyframes for a data path"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        frame_range = params.get("frame_range")
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        if not obj.animation_data or not obj.animation_data.action:
            return {"keyframes": [], "fcurve_info": None}
        
        action = obj.animation_data.action
        # Update action to ensure fcurves are available
        action.update()
        
        # Check if fcurves exist and are accessible
        try:
            if not hasattr(action, 'fcurves'):
                return {"keyframes": [], "fcurve_info": None}
            fcurves = action.fcurves
            if not fcurves:
                return {"keyframes": [], "fcurve_info": None}
        except (AttributeError, TypeError):
            return {"keyframes": [], "fcurve_info": None}
        
        keyframes = []
        fcurve_info = None
        
        for fcurve in fcurves:
            if fcurve.data_path == data_path:
                fcurve_info = {
                    "data_path": fcurve.data_path,
                    "array_index": fcurve.array_index,
                    "extrapolation": fcurve.extrapolation
                }
                
                for keyframe in fcurve.keyframe_points:
                    frame = int(keyframe.co[0])
                    value = keyframe.co[1]
                    
                    # Filter by frame range if provided
                    if frame_range:
                        if frame < frame_range[0] or frame > frame_range[1]:
                            continue
                    
                    keyframes.append({
                        "frame": frame,
                        "value": value,
                        "interpolation": keyframe.interpolation,
                        "handle_left": [keyframe.handle_left[0], keyframe.handle_left[1]],
                        "handle_right": [keyframe.handle_right[0], keyframe.handle_right[1]]
                    })
                break
        
        return {
            "keyframes": keyframes,
            "fcurve_info": fcurve_info
        }

class BatchKeyframesHandler(BaseHandler):
    """Handler for batch keyframe operations"""
    
    def get_command_name(self) -> str:
        return "batch_keyframes"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "operations": {
                "type": list,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Execute batch keyframe operations"""
        operations = params["operations"]
        results = []
        
        for op in operations:
            action = op.get("action")
            if action == "create":
                handler = CreateKeyframeHandler()
                result = handler.execute(op)
                results.append({"action": "create", "result": result})
            elif action == "delete":
                handler = DeleteKeyframeHandler()
                result = handler.execute(op)
                results.append({"action": "delete", "result": result})
            else:
                results.append({"action": action, "error": "Unknown action"})
        
        return {"operations": results}
