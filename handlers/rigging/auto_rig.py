# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Version: 1.0.0 - Auto-rigging handlers for hands and bodies

import bpy
from mathutils import Vector
from typing import Dict, Any, List, Tuple
from handlers.base_handler import BaseHandler
from utils.validation import validate_object_exists
from utils.logger import logger

HANDLER_VERSION = "1.0.0"


class RigHandHandler(BaseHandler):
    """Handler for automatically rigging a hand mesh"""
    
    def get_command_name(self) -> str:
        return "rig_hand"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "armature_name": {
                "type": str,
                "required": False
            },
            "bone_scale": {
                "type": float,
                "required": False
            },
            "finger_count": {
                "type": int,
                "required": False
            },
            "auto_position": {
                "type": bool,
                "required": False
            }
        }
    
    def _analyze_hand_geometry(self, mesh_obj) -> Dict[str, Any]:
        """Analyze hand mesh geometry to determine bone positions"""
        # Get bounding box in local space
        bbox_corners = [Vector(corner) for corner in mesh_obj.bound_box]
        
        min_x = min(v.x for v in bbox_corners)
        max_x = max(v.x for v in bbox_corners)
        min_y = min(v.y for v in bbox_corners)
        max_y = max(v.y for v in bbox_corners)
        min_z = min(v.z for v in bbox_corners)
        max_z = max(v.z for v in bbox_corners)
        
        size_x = max_x - min_x
        size_y = max_y - min_y
        size_z = max_z - min_z
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        return {
            "min": Vector((min_x, min_y, min_z)),
            "max": Vector((max_x, max_y, max_z)),
            "size": Vector((size_x, size_y, size_z)),
            "center": Vector((center_x, center_y, center_z))
        }
    
    def _create_hand_bones(self, armature, geometry: Dict, finger_count: int, bone_scale: float):
        """Create bone structure for a hand"""
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Clear default bone
        for bone in list(armature.data.edit_bones):
            armature.data.edit_bones.remove(bone)
        
        geo = geometry
        scale = bone_scale
        
        # Create wrist bone at base
        wrist = armature.data.edit_bones.new('Wrist')
        wrist.head = Vector((geo["center"].x, geo["min"].y, geo["center"].z))
        wrist.tail = Vector((geo["center"].x, geo["min"].y + geo["size"].y * 0.15 * scale, geo["center"].z))
        
        # Create palm bone
        palm = armature.data.edit_bones.new('Palm')
        palm.parent = wrist
        palm.head = wrist.tail
        palm.tail = Vector((geo["center"].x, geo["min"].y + geo["size"].y * 0.5 * scale, geo["center"].z + geo["size"].z * 0.2 * scale))
        
        # Create thumb bones (2 segments)
        thumb_base_y = geo["min"].y + geo["size"].y * 0.25
        thumb_1 = armature.data.edit_bones.new('Thumb_1')
        thumb_1.parent = wrist
        thumb_1.head = Vector((geo["min"].x + geo["size"].x * 0.15, thumb_base_y, geo["center"].z))
        thumb_1.tail = Vector((geo["min"].x + geo["size"].x * 0.05, thumb_base_y - geo["size"].y * 0.1 * scale, geo["center"].z))
        
        thumb_2 = armature.data.edit_bones.new('Thumb_2')
        thumb_2.parent = thumb_1
        thumb_2.head = thumb_1.tail
        thumb_2.tail = Vector((geo["min"].x, thumb_base_y - geo["size"].y * 0.15 * scale, geo["center"].z))
        
        # Create finger bones
        finger_names = ['Index', 'Middle', 'Ring', 'Pinky']
        finger_x_offsets = [0.012, 0.004, -0.004, -0.012]
        
        finger_base_y = geo["min"].y + geo["size"].y * 0.5
        finger_tip_y = geo["max"].y - geo["size"].y * 0.02
        
        for i, (name, x_offset) in enumerate(zip(finger_names[:finger_count], finger_x_offsets[:finger_count])):
            x_pos = geo["center"].x + x_offset * geo["size"].x
            
            # Proximal bone
            finger_1 = armature.data.edit_bones.new(f'{name}_1')
            finger_1.parent = palm
            finger_1.head = Vector((x_pos, finger_base_y, geo["center"].z + geo["size"].z * 0.12 * scale))
            finger_1.tail = Vector((x_pos, finger_base_y + (finger_tip_y - finger_base_y) * 0.33, geo["center"].z + geo["size"].z * 0.2 * scale))
            
            # Middle bone
            finger_2 = armature.data.edit_bones.new(f'{name}_2')
            finger_2.parent = finger_1
            finger_2.head = finger_1.tail
            finger_2.tail = Vector((x_pos, finger_base_y + (finger_tip_y - finger_base_y) * 0.66, geo["center"].z + geo["size"].z * 0.25 * scale))
            
            # Distal bone
            finger_3 = armature.data.edit_bones.new(f'{name}_3')
            finger_3.parent = finger_2
            finger_3.head = finger_2.tail
            finger_3.tail = Vector((x_pos, finger_tip_y, geo["center"].z + geo["size"].z * 0.25 * scale))
        
        bpy.ops.object.mode_set(mode='OBJECT')
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Automatically rig a hand mesh"""
        mesh_name = params["mesh_name"]
        armature_name = params.get("armature_name", f"{mesh_name}_Rig")
        bone_scale = params.get("bone_scale", 1.0)
        finger_count = params.get("finger_count", 4)
        auto_position = params.get("auto_position", True)
        
        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")
        
        # Unparent mesh if already parented
        if mesh_obj.parent:
            mesh_obj.parent = None
        
        # Analyze hand geometry
        geometry = self._analyze_hand_geometry(mesh_obj)
        
        # Create armature at mesh location
        bpy.ops.object.armature_add(location=mesh_obj.location)
        armature = bpy.context.active_object
        armature.name = armature_name
        armature.rotation_euler = mesh_obj.rotation_euler
        
        # Create bone structure
        self._create_hand_bones(armature, geometry, finger_count, bone_scale)
        
        # Parent mesh to armature with automatic weights
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        
        bone_count = len(armature.data.bones)
        vertex_group_count = len(mesh_obj.vertex_groups) if mesh_obj.vertex_groups else 0
        
        return {
            "rigged": True,
            "mesh_name": mesh_name,
            "armature_name": armature_name,
            "bone_count": bone_count,
            "vertex_groups_created": vertex_group_count,
            "finger_count": finger_count
        }


class RigBodyHandler(BaseHandler):
    """Handler for automatically rigging a body mesh"""
    
    def get_command_name(self) -> str:
        return "rig_body"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {
                "type": str,
                "required": True,
                "validator": validate_object_exists
            },
            "armature_name": {
                "type": str,
                "required": False
            },
            "bone_scale": {
                "type": float,
                "required": False
            },
            "include_fingers": {
                "type": bool,
                "required": False
            },
            "include_toes": {
                "type": bool,
                "required": False
            },
            "ik_arms": {
                "type": bool,
                "required": False
            },
            "ik_legs": {
                "type": bool,
                "required": False
            }
        }
    
    def _analyze_body_geometry(self, mesh_obj) -> Dict[str, Any]:
        """Analyze body mesh geometry"""
        bbox_corners = [Vector(corner) for corner in mesh_obj.bound_box]
        
        min_x = min(v.x for v in bbox_corners)
        max_x = max(v.x for v in bbox_corners)
        min_y = min(v.y for v in bbox_corners)
        max_y = max(v.y for v in bbox_corners)
        min_z = min(v.z for v in bbox_corners)
        max_z = max(v.z for v in bbox_corners)
        
        size_x = max_x - min_x
        size_y = max_y - min_y
        size_z = max_z - min_z
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        return {
            "min": Vector((min_x, min_y, min_z)),
            "max": Vector((max_x, max_y, max_z)),
            "size": Vector((size_x, size_y, size_z)),
            "center": Vector((center_x, center_y, center_z))
        }
    
    def _create_body_bones(self, armature, geometry: Dict, include_fingers: bool, include_toes: bool, bone_scale: float):
        """Create basic body bone structure"""
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Clear default bone
        for bone in list(armature.data.edit_bones):
            armature.data.edit_bones.remove(bone)
        
        geo = geometry
        scale = bone_scale
        
        # Root/Hip bone
        root = armature.data.edit_bones.new('Root')
        root.head = Vector((geo["center"].x, geo["min"].y + geo["size"].y * 0.2, geo["center"].z))
        root.tail = Vector((geo["center"].x, geo["min"].y + geo["size"].y * 0.3, geo["center"].z))
        
        # Spine bones (3 segments)
        spine_1 = armature.data.edit_bones.new('Spine_1')
        spine_1.parent = root
        spine_1.head = root.tail
        spine_1.tail = Vector((geo["center"].x, geo["min"].y + geo["size"].y * 0.5, geo["center"].z))
        
        spine_2 = armature.data.edit_bones.new('Spine_2')
        spine_2.parent = spine_1
        spine_2.head = spine_1.tail
        spine_2.tail = Vector((geo["center"].x, geo["min"].y + geo["size"].y * 0.7, geo["center"].z))
        
        spine_3 = armature.data.edit_bones.new('Spine_3')
        spine_3.parent = spine_2
        spine_3.head = spine_2.tail
        spine_3.tail = Vector((geo["center"].x, geo["min"].y + geo["size"].y * 0.85, geo["center"].z))
        
        # Head
        head = armature.data.edit_bones.new('Head')
        head.parent = spine_3
        head.head = spine_3.tail
        head.tail = Vector((geo["center"].x, geo["max"].y, geo["center"].z))
        
        # Left arm
        shoulder_l = armature.data.edit_bones.new('Shoulder.L')
        shoulder_l.parent = spine_3
        shoulder_l.head = spine_3.tail
        shoulder_l.tail = Vector((geo["min"].x, geo["min"].y + geo["size"].y * 0.8, geo["center"].z))
        
        upper_arm_l = armature.data.edit_bones.new('UpperArm.L')
        upper_arm_l.parent = shoulder_l
        upper_arm_l.head = shoulder_l.tail
        upper_arm_l.tail = Vector((geo["min"].x, geo["min"].y + geo["size"].y * 0.6, geo["center"].z))
        
        forearm_l = armature.data.edit_bones.new('Forearm.L')
        forearm_l.parent = upper_arm_l
        forearm_l.head = upper_arm_l.tail
        forearm_l.tail = Vector((geo["min"].x, geo["min"].y + geo["size"].y * 0.4, geo["center"].z))
        
        hand_l = armature.data.edit_bones.new('Hand.L')
        hand_l.parent = forearm_l
        hand_l.head = forearm_l.tail
        hand_l.tail = Vector((geo["min"].x, geo["min"].y + geo["size"].y * 0.3, geo["center"].z))
        
        # Right arm (mirror)
        shoulder_r = armature.data.edit_bones.new('Shoulder.R')
        shoulder_r.parent = spine_3
        shoulder_r.head = spine_3.tail
        shoulder_r.tail = Vector((geo["max"].x, geo["min"].y + geo["size"].y * 0.8, geo["center"].z))
        
        upper_arm_r = armature.data.edit_bones.new('UpperArm.R')
        upper_arm_r.parent = shoulder_r
        upper_arm_r.head = shoulder_r.tail
        upper_arm_r.tail = Vector((geo["max"].x, geo["min"].y + geo["size"].y * 0.6, geo["center"].z))
        
        forearm_r = armature.data.edit_bones.new('Forearm.R')
        forearm_r.parent = upper_arm_r
        forearm_r.head = upper_arm_r.tail
        forearm_r.tail = Vector((geo["max"].x, geo["min"].y + geo["size"].y * 0.4, geo["center"].z))
        
        hand_r = armature.data.edit_bones.new('Hand.R')
        hand_r.parent = forearm_r
        hand_r.head = forearm_r.tail
        hand_r.tail = Vector((geo["max"].x, geo["min"].y + geo["size"].y * 0.3, geo["center"].z))
        
        # Left leg
        thigh_l = armature.data.edit_bones.new('Thigh.L')
        thigh_l.parent = root
        thigh_l.head = root.head
        thigh_l.tail = Vector((geo["min"].x, geo["min"].y, geo["center"].z))
        
        shin_l = armature.data.edit_bones.new('Shin.L')
        shin_l.parent = thigh_l
        shin_l.head = thigh_l.tail
        shin_l.tail = Vector((geo["min"].x, geo["min"].y - geo["size"].y * 0.2, geo["center"].z))
        
        foot_l = armature.data.edit_bones.new('Foot.L')
        foot_l.parent = shin_l
        foot_l.head = shin_l.tail
        foot_l.tail = Vector((geo["min"].x, geo["min"].y - geo["size"].y * 0.3, geo["center"].z))
        
        # Right leg (mirror)
        thigh_r = armature.data.edit_bones.new('Thigh.R')
        thigh_r.parent = root
        thigh_r.head = root.head
        thigh_r.tail = Vector((geo["max"].x, geo["min"].y, geo["center"].z))
        
        shin_r = armature.data.edit_bones.new('Shin.R')
        shin_r.parent = thigh_r
        shin_r.head = thigh_r.tail
        shin_r.tail = Vector((geo["max"].x, geo["min"].y - geo["size"].y * 0.2, geo["center"].z))
        
        foot_r = armature.data.edit_bones.new('Foot.R')
        foot_r.parent = shin_r
        foot_r.head = shin_r.tail
        foot_r.tail = Vector((geo["max"].x, geo["min"].y - geo["size"].y * 0.3, geo["center"].z))
        
        # TODO: Add finger and toe bones if requested
        # This is a simplified version - full implementation would add detailed finger/toe bones
        
        bpy.ops.object.mode_set(mode='OBJECT')
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Automatically rig a body mesh"""
        mesh_name = params["mesh_name"]
        armature_name = params.get("armature_name", f"{mesh_name}_Rig")
        bone_scale = params.get("bone_scale", 1.0)
        include_fingers = params.get("include_fingers", True)
        include_toes = params.get("include_toes", True)
        ik_arms = params.get("ik_arms", False)
        ik_legs = params.get("ik_legs", False)
        
        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")
        
        # Unparent mesh if already parented
        if mesh_obj.parent:
            mesh_obj.parent = None
        
        # Analyze body geometry
        geometry = self._analyze_body_geometry(mesh_obj)
        
        # Create armature at mesh location
        bpy.ops.object.armature_add(location=mesh_obj.location)
        armature = bpy.context.active_object
        armature.name = armature_name
        armature.rotation_euler = mesh_obj.rotation_euler
        
        # Create bone structure
        self._create_body_bones(armature, geometry, include_fingers, include_toes, bone_scale)
        
        # TODO: Add IK constraints if requested
        # This would require additional constraint handlers
        
        # Parent mesh to armature with automatic weights
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        
        bone_count = len(armature.data.bones)
        vertex_group_count = len(mesh_obj.vertex_groups) if mesh_obj.vertex_groups else 0
        
        return {
            "rigged": True,
            "mesh_name": mesh_name,
            "armature_name": armature_name,
            "bone_count": bone_count,
            "vertex_groups_created": vertex_group_count,
            "include_fingers": include_fingers,
            "include_toes": include_toes,
            "ik_arms": ik_arms,
            "ik_legs": ik_legs
        }
