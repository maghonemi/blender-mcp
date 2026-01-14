# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.validation import OBJECT_NAME_SCHEMA, validate_object_exists
from utils.logger import logger

class CreatePrimitiveHandler(BaseHandler):
    """Handler for creating primitive meshes"""
    
    def get_command_name(self) -> str:
        return "create_primitive"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "type": {
                "type": str,
                "required": True
            },
            "name": {
                "type": str,
                "required": True
            },
            "location": {
                "type": list,
                "required": False
            },
            "scale": {
                "type": list,
                "required": False
            },
            "properties": {
                "type": dict,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a primitive mesh"""
        mesh_type = params["type"]
        name = params["name"]
        location = params.get("location", [0, 0, 0])
        scale = params.get("scale", [1, 1, 1])
        properties = params.get("properties", {})
        
        # Map command types to Blender operators
        operator_map = {
            "MESH_CUBE": "mesh.primitive_cube_add",
            "MESH_SPHERE": "mesh.primitive_uv_sphere_add",
            "MESH_CYLINDER": "mesh.primitive_cylinder_add",
            "MESH_PLANE": "mesh.primitive_plane_add",
            "MESH_TORUS": "mesh.primitive_torus_add",
            "MESH_MONKEY": "mesh.primitive_monkey_add"
        }
        
        operator = operator_map.get(mesh_type)
        if not operator:
            raise ValueError(f"Unknown primitive type: {mesh_type}")
        
        # Create the primitive
        bpy.ops.mesh.primitive_cube_add(location=location)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        
        # Apply properties if any
        if properties and obj.data:
            if "radius" in properties and hasattr(obj.data, "radius"):
                obj.data.radius = properties["radius"]
            if "size" in properties and hasattr(obj.data, "size"):
                obj.data.size = properties["size"]
        
        return {
            "object_name": name,
            "type": mesh_type,
            "location": location,
            "scale": scale
        }

class ExtrudeMeshHandler(BaseHandler):
    """Handler for extruding mesh elements"""
    
    def get_command_name(self) -> str:
        return "extrude_mesh"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            "mode": {
                "type": str,
                "required": False
            },
            "offset": {
                "type": list,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Extrude mesh elements"""
        object_name = params["object_name"]
        mode = params.get("mode", "FACE")
        offset = params.get("offset", [0, 0, 1])
        
        obj = bpy.data.objects.get(object_name)
        if not obj or obj.type != 'MESH':
            raise ValueError(f"Mesh object '{object_name}' not found")
        
        # Set active and enter edit mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Select all or use current selection
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Extrude
        if mode == "VERT":
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": offset})
        elif mode == "EDGE":
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": offset})
        else:  # FACE
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": offset})
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return {"extruded": True, "mode": mode}
