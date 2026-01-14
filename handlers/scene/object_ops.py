# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
import mathutils
from typing import Dict, Any, Optional
from handlers.base_handler import BaseHandler
from utils.error_handler import ErrorCode, create_error_response
from utils.validation import OBJECT_NAME_SCHEMA, validate_object_exists
from utils.logger import logger

class GetObjectInfoHandler(BaseHandler):
    """Handler for getting object information"""
    
    def get_command_name(self) -> str:
        return "get_object_info"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get detailed information about a specific object"""
        name = params["name"]
        obj = bpy.data.objects.get(name)
        
        if not obj:
            raise ValueError(f"Object not found: {name}")
        
        # Basic object info
        obj_info = {
            "name": obj.name,
            "type": obj.type,
            "location": [obj.location.x, obj.location.y, obj.location.z],
            "rotation": [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z],
            "scale": [obj.scale.x, obj.scale.y, obj.scale.z],
            "visible": obj.visible_get(),
            "materials": [],
        }
        
        if obj.type == "MESH":
            bounding_box = self._get_aabb(obj)
            obj_info["world_bounding_box"] = bounding_box
        
        # Add material slots
        for slot in obj.material_slots:
            if slot.material:
                obj_info["materials"].append(slot.material.name)
        
        # Add mesh data if applicable
        if obj.type == 'MESH' and obj.data:
            mesh = obj.data
            obj_info["mesh"] = {
                "vertices": len(mesh.vertices),
                "edges": len(mesh.edges),
                "polygons": len(mesh.polygons),
            }
        
        return obj_info
    
    @staticmethod
    def _get_aabb(obj):
        """Returns the world-space axis-aligned bounding box (AABB) of an object."""
        if obj.type != 'MESH':
            raise TypeError("Object must be a mesh")
        
        # Get the bounding box corners in local space
        local_bbox_corners = [mathutils.Vector(corner) for corner in obj.bound_box]
        
        # Convert to world coordinates
        world_bbox_corners = [obj.matrix_world @ corner for corner in local_bbox_corners]
        
        # Compute axis-aligned min/max coordinates
        min_corner = mathutils.Vector(map(min, zip(*world_bbox_corners)))
        max_corner = mathutils.Vector(map(max, zip(*world_bbox_corners)))
        
        return [
            [*min_corner], [*max_corner]
        ]

class GetViewportScreenshotHandler(BaseHandler):
    """Handler for capturing viewport screenshots"""
    
    def get_command_name(self) -> str:
        return "get_viewport_screenshot"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "max_size": {
                "type": int,
                "required": False
            },
            "filepath": {
                "type": str,
                "required": True
            },
            "format": {
                "type": str,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Capture a screenshot of the current 3D viewport"""
        filepath = params["filepath"]
        max_size = params.get("max_size", 800)
        format_str = params.get("format", "png")
        
        if not filepath:
            raise ValueError("No filepath provided")
        
        # Find the active 3D viewport
        area = None
        for a in bpy.context.screen.areas:
            if a.type == 'VIEW_3D':
                area = a
                break
        
        if not area:
            raise ValueError("No 3D viewport found")
        
        # Take screenshot with proper context override
        with bpy.context.temp_override(area=area):
            bpy.ops.screen.screenshot_area(filepath=filepath)
        
        # Load and resize if needed
        img = bpy.data.images.load(filepath)
        width, height = img.size
        
        if max(width, height) > max_size:
            scale = max_size / max(width, height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img.scale(new_width, new_height)
            
            # Set format and save
            img.file_format = format_str.upper()
            img.save()
            width, height = new_width, new_height
        
        # Cleanup Blender image data
        bpy.data.images.remove(img)
        
        return {
            "success": True,
            "width": width,
            "height": height,
            "filepath": filepath
        }

class ExecuteCodeHandler(BaseHandler):
    """Handler for executing arbitrary Python code"""
    
    def get_command_name(self) -> str:
        return "execute_code"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "code": {
                "type": str,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Execute arbitrary Blender Python code"""
        # WARNING: This is powerful but potentially dangerous
        code = params["code"]
        
        try:
            # Create a local namespace for execution
            namespace = {"bpy": bpy, "__builtins__": __builtins__}
            
            # Capture stdout during execution
            import io
            from contextlib import redirect_stdout
            capture_buffer = io.StringIO()
            
            with redirect_stdout(capture_buffer):
                exec(code, namespace)
            
            captured_output = capture_buffer.getvalue()
            return {"executed": True, "result": captured_output}
        except Exception as e:
            raise Exception(f"Code execution error: {str(e)}")
