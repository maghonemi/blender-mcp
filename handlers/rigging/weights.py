# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Weight painting and skinning handlers for rigging workflow

import bpy
from typing import Dict, Any, List
from handlers.base_handler import BaseHandler
from utils.logger import logger


class ParentToArmatureHandler(BaseHandler):
    """Handler for parenting mesh to armature with automatic weights"""

    def get_command_name(self) -> str:
        return "parent_to_armature"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {"type": str, "required": True},
            "armature_name": {"type": str, "required": True},
            "parent_type": {"type": str, "required": False},
            "use_automatic_weight": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Parent mesh to armature with optional automatic weights"""
        mesh_name = params["mesh_name"]
        armature_name = params["armature_name"]
        parent_type = params.get("parent_type", "ARMATURE_AUTO")
        use_automatic_weight = params.get("use_automatic_weight", True)

        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")

        armature_obj = bpy.data.objects.get(armature_name)
        if not armature_obj or armature_obj.type != 'ARMATURE':
            raise ValueError(f"Armature '{armature_name}' not found")

        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Select mesh first, then armature (armature must be active)
        mesh_obj.select_set(True)
        armature_obj.select_set(True)
        bpy.context.view_layer.objects.active = armature_obj

        # Parent based on type
        if use_automatic_weight or parent_type == "ARMATURE_AUTO":
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            parent_method = "ARMATURE_AUTO"
        elif parent_type == "ARMATURE_NAME":
            bpy.ops.object.parent_set(type='ARMATURE_NAME')
            parent_method = "ARMATURE_NAME"
        elif parent_type == "ARMATURE_ENVELOPE":
            bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
            parent_method = "ARMATURE_ENVELOPE"
        else:
            bpy.ops.object.parent_set(type='ARMATURE')
            parent_method = "ARMATURE"

        # Get vertex groups created
        vertex_groups = [vg.name for vg in mesh_obj.vertex_groups]

        logger.info(f"Parented {mesh_name} to {armature_name} with {parent_method}")

        return {
            "parented": True,
            "mesh_name": mesh_name,
            "armature_name": armature_name,
            "parent_type": parent_method,
            "vertex_groups_created": vertex_groups,
            "vertex_group_count": len(vertex_groups)
        }


class CreateVertexGroupHandler(BaseHandler):
    """Handler for creating a vertex group"""

    def get_command_name(self) -> str:
        return "create_vertex_group"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {"type": str, "required": True},
            "group_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a new vertex group"""
        mesh_name = params["mesh_name"]
        group_name = params["group_name"]

        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")

        # Check if group already exists
        if group_name in mesh_obj.vertex_groups:
            return {
                "created": False,
                "message": f"Vertex group '{group_name}' already exists",
                "group_name": group_name
            }

        # Create vertex group
        vg = mesh_obj.vertex_groups.new(name=group_name)

        logger.info(f"Created vertex group '{group_name}' on {mesh_name}")

        return {
            "created": True,
            "mesh_name": mesh_name,
            "group_name": vg.name,
            "group_index": vg.index
        }


class SetVertexWeightsHandler(BaseHandler):
    """Handler for setting vertex weights"""

    def get_command_name(self) -> str:
        return "set_vertex_weights"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {"type": str, "required": True},
            "vertex_group_name": {"type": str, "required": True},
            "weights": {"type": dict, "required": True},
            "mode": {"type": str, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set vertex weights for a vertex group"""
        mesh_name = params["mesh_name"]
        group_name = params["vertex_group_name"]
        weights = params["weights"]  # {vertex_index: weight}
        mode = params.get("mode", "REPLACE")  # REPLACE, ADD

        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")

        vg = mesh_obj.vertex_groups.get(group_name)
        if not vg:
            # Create the group if it doesn't exist
            vg = mesh_obj.vertex_groups.new(name=group_name)

        vertices_set = 0

        for vertex_idx, weight in weights.items():
            vertex_idx = int(vertex_idx)
            weight = float(weight)

            # Clamp weight to 0-1
            weight = max(0.0, min(1.0, weight))

            if mode == "ADD":
                vg.add([vertex_idx], weight, 'ADD')
            else:
                vg.add([vertex_idx], weight, 'REPLACE')

            vertices_set += 1

        logger.info(f"Set {vertices_set} vertex weights on {group_name}")

        return {
            "weights_set": True,
            "mesh_name": mesh_name,
            "vertex_group_name": group_name,
            "vertices_affected": vertices_set,
            "mode": mode
        }


class GetVertexWeightsHandler(BaseHandler):
    """Handler for getting vertex weights"""

    def get_command_name(self) -> str:
        return "get_vertex_weights"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {"type": str, "required": True},
            "vertex_group_name": {"type": str, "required": True},
            "vertex_indices": {"type": list, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get vertex weights from a vertex group"""
        mesh_name = params["mesh_name"]
        group_name = params["vertex_group_name"]
        vertex_indices = params.get("vertex_indices")

        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")

        vg = mesh_obj.vertex_groups.get(group_name)
        if not vg:
            raise ValueError(f"Vertex group '{group_name}' not found")

        weights = {}
        mesh_data = mesh_obj.data

        # Get indices to check
        if vertex_indices:
            indices = vertex_indices
        else:
            indices = range(len(mesh_data.vertices))

        # Get weights
        for idx in indices:
            try:
                weight = vg.weight(idx)
                if weight > 0:
                    weights[idx] = weight
            except RuntimeError:
                # Vertex not in group
                pass

        return {
            "mesh_name": mesh_name,
            "vertex_group_name": group_name,
            "weights": weights,
            "vertex_count": len(weights)
        }


class NormalizeWeightsHandler(BaseHandler):
    """Handler for normalizing vertex weights"""

    def get_command_name(self) -> str:
        return "normalize_weights"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {"type": str, "required": True},
            "mode": {"type": str, "required": False},
            "lock_active": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Normalize vertex weights"""
        mesh_name = params["mesh_name"]
        mode = params.get("mode", "ALL")  # ALL or ACTIVE
        lock_active = params.get("lock_active", False)

        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")

        # Select and make active
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        bpy.context.view_layer.objects.active = mesh_obj

        # Enter weight paint mode
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

        try:
            if mode.upper() == "ALL":
                bpy.ops.object.vertex_group_normalize_all(lock_active=lock_active)
            else:
                bpy.ops.object.vertex_group_normalize()

            logger.info(f"Normalized weights on {mesh_name}")

        finally:
            bpy.ops.object.mode_set(mode='OBJECT')

        return {
            "normalized": True,
            "mesh_name": mesh_name,
            "mode": mode
        }


class TransferWeightsHandler(BaseHandler):
    """Handler for transferring weights between meshes"""

    def get_command_name(self) -> str:
        return "transfer_weights"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "source_mesh": {"type": str, "required": True},
            "target_mesh": {"type": str, "required": True},
            "vertex_group": {"type": str, "required": False},
            "mix_mode": {"type": str, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Transfer weights from source to target mesh"""
        source_name = params["source_mesh"]
        target_name = params["target_mesh"]
        vertex_group = params.get("vertex_group")  # None = all groups
        mix_mode = params.get("mix_mode", "REPLACE")

        source_obj = bpy.data.objects.get(source_name)
        if not source_obj or source_obj.type != 'MESH':
            raise ValueError(f"Source mesh '{source_name}' not found")

        target_obj = bpy.data.objects.get(target_name)
        if not target_obj or target_obj.type != 'MESH':
            raise ValueError(f"Target mesh '{target_name}' not found")

        # Deselect all, then select target and source
        bpy.ops.object.select_all(action='DESELECT')
        source_obj.select_set(True)
        target_obj.select_set(True)
        bpy.context.view_layer.objects.active = target_obj

        # Add data transfer modifier
        modifier = target_obj.modifiers.new(name="WeightTransfer", type='DATA_TRANSFER')
        modifier.object = source_obj
        modifier.use_vert_data = True
        modifier.data_types_verts = {'VGROUP_WEIGHTS'}

        if vertex_group:
            modifier.vert_mapping = 'NEAREST'
            modifier.layers_vgroup_select_src = vertex_group
            modifier.layers_vgroup_select_dst = vertex_group
        else:
            modifier.layers_vgroup_select_src = 'ALL'
            modifier.layers_vgroup_select_dst = 'NAME'

        # Apply modifier
        bpy.ops.object.modifier_apply(modifier=modifier.name)

        logger.info(f"Transferred weights from {source_name} to {target_name}")

        return {
            "transferred": True,
            "source_mesh": source_name,
            "target_mesh": target_name,
            "vertex_group": vertex_group if vertex_group else "ALL",
            "target_groups": [vg.name for vg in target_obj.vertex_groups]
        }


class GetVertexGroupsHandler(BaseHandler):
    """Handler for getting all vertex groups on a mesh"""

    def get_command_name(self) -> str:
        return "get_vertex_groups"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mesh_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get all vertex groups on a mesh"""
        mesh_name = params["mesh_name"]

        mesh_obj = bpy.data.objects.get(mesh_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            raise ValueError(f"Mesh '{mesh_name}' not found")

        groups = []
        for vg in mesh_obj.vertex_groups:
            groups.append({
                "name": vg.name,
                "index": vg.index,
                "lock_weight": vg.lock_weight
            })

        return {
            "mesh_name": mesh_name,
            "vertex_groups": groups,
            "count": len(groups)
        }
