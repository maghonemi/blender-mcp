# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Version: 1.0.0 - Skinning and weight painting handlers

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.validation import validate_object_exists
from utils.logger import logger

HANDLER_VERSION = "1.0.0"


class ParentToArmatureHandler(BaseHandler):
    """Handler for parenting mesh to armature with automatic weights"""
    
    def get_command_name(self) -> str:
        return "parent_to_armature"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "armature_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "use_automatic_weight": {
                "type": bool,
                "required": False
            },
            "use_deform_preserve_volume": {
                "type": bool,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Parent a mesh to an armature with optional automatic weights"""
        mesh_name = params["mesh_name"]
        armature_name = params["armature_name"]
        use_automatic_weight = params.get("use_automatic_weight", True)
        use_deform_preserve_volume = params.get("use_deform_preserve_volume", False)
        
        mesh_obj = bpy.data.objects.get(mesh_name)
        armature_obj = bpy.data.objects.get(armature_name)
        
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")
        
        if not armature_obj or armature_obj.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")
        
        # Store current selection
        previous_selection = [obj for obj in bpy.context.selected_objects]
        previous_active = bpy.context.view_layer.objects.active
        
        try:
            # Select mesh first, then armature (armature must be active)
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            armature_obj.select_set(True)
            bpy.context.view_layer.objects.active = armature_obj
            
            # Parent with automatic weights
            if use_automatic_weight:
                bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            else:
                bpy.ops.object.parent_set(type='ARMATURE')
            
            # Set deform preserve volume if requested
            if use_deform_preserve_volume and mesh_obj.modifiers:
                for mod in mesh_obj.modifiers:
                    if mod.type == 'ARMATURE':
                        mod.use_deform_preserve_volume = True
            
            # Count vertex groups created
            vertex_group_count = len(mesh_obj.vertex_groups) if mesh_obj.vertex_groups else 0
            
            return {
                "parented": True,
                "mesh_name": mesh_name,
                "armature_name": armature_name,
                "vertex_groups_created": vertex_group_count,
                "automatic_weights": use_automatic_weight
            }
        finally:
            # Restore previous selection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in previous_selection:
                obj.select_set(True)
            if previous_active:
                bpy.context.view_layer.objects.active = previous_active


class AutoWeightAssignHandler(BaseHandler):
    """Handler for automatic weight assignment"""
    
    def get_command_name(self) -> str:
        return "auto_weight_assign"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "armature_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "method": {
                "type": str,
                "required": False
            },
            "remove_unused_vertex_groups": {
                "type": bool,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Assign automatic weights to a mesh from an armature"""
        mesh_name = params["mesh_name"]
        armature_name = params["armature_name"]
        method = params.get("method", "ENVELOPE")  # ENVELOPE or HEAT
        remove_unused = params.get("remove_unused_vertex_groups", True)
        
        mesh_obj = bpy.data.objects.get(mesh_name)
        armature_obj = bpy.data.objects.get(armature_name)
        
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")
        
        if not armature_obj or armature_obj.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")
        
        # Check if mesh is already parented to armature
        if mesh_obj.parent != armature_obj:
            raise ValueError(f"Mesh '{mesh_name}' must be parented to armature '{armature_name}' first")
        
        # Store current selection
        previous_selection = [obj for obj in bpy.context.selected_objects]
        previous_active = bpy.context.view_layer.objects.active
        
        try:
            # Select mesh and enter weight paint mode
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            bpy.context.view_layer.objects.active = mesh_obj
            
            # Enter weight paint mode
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
            
            # Select all vertices
            bpy.ops.mesh.select_all(action='SELECT')
            
            # Assign automatic weights
            if method == "HEAT":
                # Heat-based weighting (more accurate but slower)
                bpy.ops.paint.weight_from_bones(type='HEAT')
            else:
                # Envelope-based weighting (faster)
                bpy.ops.paint.weight_from_bones(type='ENVELOPE')
            
            # Remove unused vertex groups if requested
            if remove_unused:
                # Get bone names from armature
                bone_names = {bone.name for bone in armature_obj.data.bones}
                
                # Remove vertex groups that don't match bones
                groups_to_remove = []
                for vg in mesh_obj.vertex_groups:
                    if vg.name not in bone_names:
                        groups_to_remove.append(vg)
                
                for vg in groups_to_remove:
                    mesh_obj.vertex_groups.remove(vg)
            
            # Return to object mode
            bpy.ops.object.mode_set(mode='OBJECT')
            
            vertex_group_count = len(mesh_obj.vertex_groups)
            
            return {
                "weights_assigned": True,
                "mesh_name": mesh_name,
                "armature_name": armature_name,
                "method": method,
                "vertex_groups_count": vertex_group_count
            }
        finally:
            # Restore previous selection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in previous_selection:
                obj.select_set(True)
            if previous_active:
                bpy.context.view_layer.objects.active = previous_active
