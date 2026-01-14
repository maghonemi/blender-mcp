# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Lighting handlers for movie production workflow

import bpy
import math
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.logger import logger


class CreateLightHandler(BaseHandler):
    """Handler for creating light objects"""

    def get_command_name(self) -> str:
        return "create_light"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "name": {"type": str, "required": True},
            "type": {"type": str, "required": True},
            "location": {"type": list, "required": False},
            "rotation": {"type": list, "required": False},
            "energy": {"type": (int, float), "required": False},
            "color": {"type": list, "required": False},
            "size": {"type": (int, float), "required": False},
            "use_shadow": {"type": bool, "required": False},
            "shadow_soft_size": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a new light"""
        name = params["name"]
        light_type = params["type"].upper()
        location = params.get("location", [0, 0, 5])
        rotation = params.get("rotation", [0, 0, 0])
        energy = params.get("energy", 1000)
        color = params.get("color", [1, 1, 1])
        size = params.get("size", 1.0)
        use_shadow = params.get("use_shadow", True)
        shadow_soft_size = params.get("shadow_soft_size", 0.25)

        # Validate light type
        valid_types = ['POINT', 'SUN', 'SPOT', 'AREA']
        if light_type not in valid_types:
            raise ValueError(f"Invalid light type. Must be one of: {valid_types}")

        # Create light data
        light_data = bpy.data.lights.new(name=name, type=light_type)
        light_data.energy = energy
        light_data.color = color[:3]  # RGB only
        light_data.use_shadow = use_shadow

        # Type-specific settings
        if light_type == 'AREA':
            light_data.size = size
        elif light_type == 'SPOT':
            light_data.shadow_soft_size = shadow_soft_size
        elif light_type == 'POINT':
            light_data.shadow_soft_size = shadow_soft_size
        elif light_type == 'SUN':
            light_data.angle = math.radians(size)  # Sun angle in radians

        # Create light object
        light_obj = bpy.data.objects.new(name, light_data)
        light_obj.location = location
        light_obj.rotation_euler = rotation

        # Link to scene
        bpy.context.scene.collection.objects.link(light_obj)

        logger.info(f"Created {light_type} light: {name}")

        return {
            "light_created": True,
            "light_name": light_obj.name,
            "light_type": light_type,
            "location": list(light_obj.location),
            "energy": light_data.energy
        }


class SetLightPropertiesHandler(BaseHandler):
    """Handler for setting light properties"""

    def get_command_name(self) -> str:
        return "set_light_properties"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "light_name": {"type": str, "required": True},
            "energy": {"type": (int, float), "required": False},
            "color": {"type": list, "required": False},
            "size": {"type": (int, float), "required": False},
            "use_shadow": {"type": bool, "required": False},
            "shadow_soft_size": {"type": (int, float), "required": False},
            "spot_size": {"type": (int, float), "required": False},
            "spot_blend": {"type": (int, float), "required": False},
            "specular_factor": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set light properties"""
        light_name = params["light_name"]

        light_obj = bpy.data.objects.get(light_name)
        if not light_obj or light_obj.type != 'LIGHT':
            raise ValueError(f"Light '{light_name}' not found")

        light = light_obj.data

        # Set properties if provided
        if "energy" in params:
            light.energy = params["energy"]
        if "color" in params:
            light.color = params["color"][:3]
        if "use_shadow" in params:
            light.use_shadow = params["use_shadow"]
        if "specular_factor" in params:
            light.specular_factor = params["specular_factor"]

        # Type-specific settings
        if light.type == 'AREA' and "size" in params:
            light.size = params["size"]
        if light.type in ['POINT', 'SPOT'] and "shadow_soft_size" in params:
            light.shadow_soft_size = params["shadow_soft_size"]
        if light.type == 'SPOT':
            if "spot_size" in params:
                light.spot_size = params["spot_size"]
            if "spot_blend" in params:
                light.spot_blend = params["spot_blend"]
        if light.type == 'SUN' and "size" in params:
            light.angle = math.radians(params["size"])

        logger.info(f"Updated light properties: {light_name}")

        return {
            "properties_set": True,
            "light_name": light_name,
            "energy": light.energy,
            "color": list(light.color),
            "use_shadow": light.use_shadow
        }


class GetLightInfoHandler(BaseHandler):
    """Handler for getting light information"""

    def get_command_name(self) -> str:
        return "get_light_info"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "light_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get light information"""
        light_name = params["light_name"]

        light_obj = bpy.data.objects.get(light_name)
        if not light_obj or light_obj.type != 'LIGHT':
            raise ValueError(f"Light '{light_name}' not found")

        light = light_obj.data

        result = {
            "name": light_obj.name,
            "type": light.type,
            "location": list(light_obj.location),
            "rotation": list(light_obj.rotation_euler),
            "energy": light.energy,
            "color": list(light.color),
            "use_shadow": light.use_shadow,
            "specular_factor": light.specular_factor
        }

        # Type-specific properties
        if light.type == 'AREA':
            result["size"] = light.size
            result["shape"] = light.shape
        elif light.type == 'SPOT':
            result["spot_size"] = light.spot_size
            result["spot_blend"] = light.spot_blend
            result["shadow_soft_size"] = light.shadow_soft_size
        elif light.type == 'POINT':
            result["shadow_soft_size"] = light.shadow_soft_size
        elif light.type == 'SUN':
            result["angle"] = math.degrees(light.angle)

        return result


class CreateThreePointLightingHandler(BaseHandler):
    """Handler for creating three-point lighting setup"""

    def get_command_name(self) -> str:
        return "create_three_point_lighting"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "target_object": {"type": str, "required": True},
            "key_energy": {"type": (int, float), "required": False},
            "fill_energy": {"type": (int, float), "required": False},
            "rim_energy": {"type": (int, float), "required": False},
            "distance": {"type": (int, float), "required": False},
            "key_color": {"type": list, "required": False},
            "fill_color": {"type": list, "required": False},
            "rim_color": {"type": list, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a three-point lighting setup around a target object"""
        target_name = params["target_object"]
        key_energy = params.get("key_energy", 1000)
        fill_energy = params.get("fill_energy", 500)
        rim_energy = params.get("rim_energy", 750)
        distance = params.get("distance", 5)
        key_color = params.get("key_color", [1, 0.95, 0.9])  # Warm
        fill_color = params.get("fill_color", [0.9, 0.95, 1])  # Cool
        rim_color = params.get("rim_color", [1, 1, 1])

        target_obj = bpy.data.objects.get(target_name)
        if not target_obj:
            raise ValueError(f"Target object '{target_name}' not found")

        target_loc = target_obj.location
        lights_created = []

        # Key light - 45 degrees to the right, 45 degrees up
        key_angle = math.radians(45)
        key_height = math.radians(45)
        key_x = target_loc.x + distance * math.cos(key_angle)
        key_y = target_loc.y - distance * math.sin(key_angle)
        key_z = target_loc.z + distance * math.sin(key_height)

        key_data = bpy.data.lights.new(name="Key_Light", type='AREA')
        key_data.energy = key_energy
        key_data.color = key_color[:3]
        key_data.size = 2

        key_obj = bpy.data.objects.new("Key_Light", key_data)
        key_obj.location = [key_x, key_y, key_z]
        bpy.context.scene.collection.objects.link(key_obj)

        # Add Track To constraint
        track_constraint = key_obj.constraints.new(type='TRACK_TO')
        track_constraint.target = target_obj
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'

        lights_created.append(key_obj.name)

        # Fill light - 45 degrees to the left, lower
        fill_angle = math.radians(-45)
        fill_x = target_loc.x + distance * math.cos(fill_angle)
        fill_y = target_loc.y - distance * math.sin(fill_angle)
        fill_z = target_loc.z + distance * 0.5

        fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
        fill_data.energy = fill_energy
        fill_data.color = fill_color[:3]
        fill_data.size = 3

        fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
        fill_obj.location = [fill_x, fill_y, fill_z]
        bpy.context.scene.collection.objects.link(fill_obj)

        track_constraint = fill_obj.constraints.new(type='TRACK_TO')
        track_constraint.target = target_obj
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'

        lights_created.append(fill_obj.name)

        # Rim/Back light - behind and above
        rim_x = target_loc.x
        rim_y = target_loc.y + distance
        rim_z = target_loc.z + distance * 0.75

        rim_data = bpy.data.lights.new(name="Rim_Light", type='AREA')
        rim_data.energy = rim_energy
        rim_data.color = rim_color[:3]
        rim_data.size = 1.5

        rim_obj = bpy.data.objects.new("Rim_Light", rim_data)
        rim_obj.location = [rim_x, rim_y, rim_z]
        bpy.context.scene.collection.objects.link(rim_obj)

        track_constraint = rim_obj.constraints.new(type='TRACK_TO')
        track_constraint.target = target_obj
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'

        lights_created.append(rim_obj.name)

        logger.info(f"Created three-point lighting for: {target_name}")

        return {
            "lighting_setup_created": True,
            "target_object": target_name,
            "lights_created": lights_created,
            "key_light": {
                "name": "Key_Light",
                "energy": key_energy,
                "location": [key_x, key_y, key_z]
            },
            "fill_light": {
                "name": "Fill_Light",
                "energy": fill_energy,
                "location": [fill_x, fill_y, fill_z]
            },
            "rim_light": {
                "name": "Rim_Light",
                "energy": rim_energy,
                "location": [rim_x, rim_y, rim_z]
            }
        }


class SetWorldLightingHandler(BaseHandler):
    """Handler for setting world/environment lighting"""

    def get_command_name(self) -> str:
        return "set_world_lighting"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "type": {"type": str, "required": True},
            "color": {"type": list, "required": False},
            "strength": {"type": (int, float), "required": False},
            "hdri_path": {"type": str, "required": False},
            "hdri_rotation": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set world/environment lighting"""
        lighting_type = params["type"].upper()
        color = params.get("color", [0.05, 0.05, 0.05])
        strength = params.get("strength", 1.0)
        hdri_path = params.get("hdri_path")
        hdri_rotation = params.get("hdri_rotation", 0)

        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world

        world.use_nodes = True
        nodes = world.node_tree.nodes
        links = world.node_tree.links

        # Clear existing nodes
        nodes.clear()

        # Create output node
        output_node = nodes.new(type='ShaderNodeOutputWorld')
        output_node.location = (300, 0)

        if lighting_type == "COLOR":
            # Simple background color
            bg_node = nodes.new(type='ShaderNodeBackground')
            bg_node.location = (0, 0)
            bg_node.inputs['Color'].default_value = (*color[:3], 1)
            bg_node.inputs['Strength'].default_value = strength

            links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

            return {
                "world_lighting_set": True,
                "type": "COLOR",
                "color": color,
                "strength": strength
            }

        elif lighting_type == "HDRI":
            if not hdri_path:
                raise ValueError("HDRI path is required for HDRI lighting")

            # Environment texture setup
            env_tex_node = nodes.new(type='ShaderNodeTexEnvironment')
            env_tex_node.location = (-300, 0)

            # Load HDRI image
            try:
                img = bpy.data.images.load(hdri_path)
                env_tex_node.image = img
            except Exception as e:
                raise ValueError(f"Could not load HDRI: {hdri_path}. Error: {e}")

            # Texture coordinate and mapping for rotation
            tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
            tex_coord_node.location = (-700, 0)

            mapping_node = nodes.new(type='ShaderNodeMapping')
            mapping_node.location = (-500, 0)
            mapping_node.inputs['Rotation'].default_value = (0, 0, math.radians(hdri_rotation))

            # Background node
            bg_node = nodes.new(type='ShaderNodeBackground')
            bg_node.location = (0, 0)
            bg_node.inputs['Strength'].default_value = strength

            # Connect nodes
            links.new(tex_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
            links.new(mapping_node.outputs['Vector'], env_tex_node.inputs['Vector'])
            links.new(env_tex_node.outputs['Color'], bg_node.inputs['Color'])
            links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

            logger.info(f"Set HDRI world lighting: {hdri_path}")

            return {
                "world_lighting_set": True,
                "type": "HDRI",
                "hdri_path": hdri_path,
                "strength": strength,
                "rotation": hdri_rotation
            }

        elif lighting_type == "SKY":
            # Sky texture
            sky_node = nodes.new(type='ShaderNodeTexSky')
            sky_node.location = (-300, 0)
            sky_node.sky_type = 'NISHITA'

            # Background node
            bg_node = nodes.new(type='ShaderNodeBackground')
            bg_node.location = (0, 0)
            bg_node.inputs['Strength'].default_value = strength

            # Connect
            links.new(sky_node.outputs['Color'], bg_node.inputs['Color'])
            links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

            logger.info("Set sky world lighting")

            return {
                "world_lighting_set": True,
                "type": "SKY",
                "strength": strength
            }

        else:
            raise ValueError(f"Invalid lighting type. Must be COLOR, HDRI, or SKY")
