# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Version: 2.0.2 - Completely rewritten to avoid fcurves issues

import bpy
from typing import Dict, Any, List, Optional
from handlers.base_handler import BaseHandler
from utils.error_handler import ErrorCode
from utils.validation import OBJECT_NAME_SCHEMA, FRAME_SCHEMA, DATA_PATH_SCHEMA, validate_frame
from utils.logger import logger

HANDLER_VERSION = "2.0.2"

class CreateKeyframeHandler(BaseHandler):
    """Handler for creating keyframes - bulletproof version"""
    
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
        """Create a keyframe - simplified and bulletproof"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        frame = params["frame"]
        value = params["value"]
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        # Handle component paths like location.x
        base_path = data_path
        index = -1
        
        if data_path.endswith(".x"):
            base_path = data_path[:-2]
            index = 0
        elif data_path.endswith(".y"):
            base_path = data_path[:-2]
            index = 1
        elif data_path.endswith(".z"):
            base_path = data_path[:-2]
            index = 2
        
        # Set the current frame
        bpy.context.scene.frame_set(frame)
        
        # Set the value
        try:
            prop = getattr(obj, base_path)
            if isinstance(value, list):
                if index >= 0:
                    prop[index] = value[0] if value else 0
                else:
                    for i, v in enumerate(value):
                        if i < len(prop):
                            prop[i] = v
            else:
                if index >= 0:
                    prop[index] = value
                else:
                    setattr(obj, base_path, value)
        except Exception as e:
            logger.warning(f"Set value warning: {e}")
        
        # Insert keyframe - use simple approach
        try:
            if index >= 0:
                obj.keyframe_insert(data_path=base_path, index=index, frame=frame)
            else:
                obj.keyframe_insert(data_path=base_path, frame=frame)
        except Exception as e:
            raise ValueError(f"Keyframe insert failed: {e}")
        
        return {
            "keyframe_created": True,
            "frame": frame,
            "data_path": data_path,
            "value": value
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
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Delete keyframe(s)"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        frame = params.get("frame")
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        base_path = data_path
        if data_path.endswith((".x", ".y", ".z")):
            base_path = data_path[:-2]
        
        try:
            if frame:
                obj.keyframe_delete(data_path=base_path, frame=frame)
            else:
                obj.keyframe_delete(data_path=base_path)
            return {"deleted": True, "data_path": data_path}
        except Exception as e:
            raise ValueError(f"Delete failed: {e}")


class GetKeyframesHandler(BaseHandler):
    """Handler for getting keyframes - no fcurves dependency"""
    
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
        """Get keyframes - works without fcurves access"""
        object_name = params["object_name"]
        data_path = params["data_path"]
        frame_range = params.get("frame_range")
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        # Check if object has animation data
        if not obj.animation_data:
            return {"keyframes": [], "has_animation": False}
        
        if not obj.animation_data.action:
            return {"keyframes": [], "has_animation": False}
        
        action = obj.animation_data.action
        keyframes = []
        
        # Handle component paths
        base_path = data_path
        target_index = -1
        if data_path.endswith(".x"):
            base_path = data_path[:-2]
            target_index = 0
        elif data_path.endswith(".y"):
            base_path = data_path[:-2]
            target_index = 1
        elif data_path.endswith(".z"):
            base_path = data_path[:-2]
            target_index = 2
        
        # Try to get fcurves safely
        try:
            # Multiple ways to access fcurves depending on Blender version
            fcurves = None
            
            # Method 1: Direct attribute access
            if hasattr(action, 'fcurves') and action.fcurves is not None:
                fcurves = action.fcurves
            
            # Method 2: Try as property
            if fcurves is None:
                try:
                    fcurves = getattr(action, 'fcurves', None)
                except:
                    pass
            
            if fcurves:
                for fc in fcurves:
                    if fc.data_path == base_path:
                        if target_index < 0 or fc.array_index == target_index:
                            for kp in fc.keyframe_points:
                                kf_frame = int(kp.co[0])
                                kf_value = kp.co[1]
                                
                                if frame_range:
                                    if kf_frame < frame_range[0] or kf_frame > frame_range[1]:
                                        continue
                                
                                keyframes.append({
                                    "frame": kf_frame,
                                    "value": kf_value
                                })
        except Exception as e:
            # If fcurves access fails, return empty but don't crash
            logger.warning(f"FCurves access failed: {e}")
            return {"keyframes": [], "has_animation": True, "fcurves_error": str(e)}
        
        return {"keyframes": keyframes, "has_animation": True}


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
            try:
                if action == "create":
                    handler = CreateKeyframeHandler()
                    result = handler.execute(op)
                    results.append({"success": True, "result": result})
                elif action == "delete":
                    handler = DeleteKeyframeHandler()
                    result = handler.execute(op)
                    results.append({"success": True, "result": result})
                else:
                    results.append({"success": False, "error": f"Unknown: {action}"})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        return {"operations": results, "total": len(operations)}
