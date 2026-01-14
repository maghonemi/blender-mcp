# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Camera handlers for movie production workflow

import bpy
import math
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.logger import logger


class CreateCameraHandler(BaseHandler):
    """Handler for creating camera objects"""

    def get_command_name(self) -> str:
        return "create_camera"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "name": {"type": str, "required": True},
            "location": {"type": list, "required": False},
            "rotation": {"type": list, "required": False},
            "lens": {"type": (int, float), "required": False},
            "sensor_width": {"type": (int, float), "required": False},
            "clip_start": {"type": (int, float), "required": False},
            "clip_end": {"type": (int, float), "required": False},
            "type": {"type": str, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a new camera"""
        name = params["name"]
        location = params.get("location", [0, 0, 0])
        rotation = params.get("rotation", [0, 0, 0])
        lens = params.get("lens", 50)
        sensor_width = params.get("sensor_width", 36)
        clip_start = params.get("clip_start", 0.1)
        clip_end = params.get("clip_end", 1000)
        cam_type = params.get("type", "PERSP")

        # Create camera data
        camera_data = bpy.data.cameras.new(name=name)
        camera_data.lens = lens
        camera_data.sensor_width = sensor_width
        camera_data.clip_start = clip_start
        camera_data.clip_end = clip_end
        camera_data.type = cam_type

        # Create camera object
        camera_obj = bpy.data.objects.new(name, camera_data)
        camera_obj.location = location
        camera_obj.rotation_euler = rotation

        # Link to scene
        bpy.context.scene.collection.objects.link(camera_obj)

        logger.info(f"Created camera: {name}")

        return {
            "camera_created": True,
            "camera_name": camera_obj.name,
            "location": list(camera_obj.location),
            "lens": camera_data.lens,
            "type": camera_data.type
        }


class SetActiveCameraHandler(BaseHandler):
    """Handler for setting the active scene camera"""

    def get_command_name(self) -> str:
        return "set_active_camera"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "camera_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set the active camera for the scene"""
        camera_name = params["camera_name"]

        camera = bpy.data.objects.get(camera_name)
        if not camera:
            raise ValueError(f"Camera '{camera_name}' not found")

        if camera.type != 'CAMERA':
            raise ValueError(f"Object '{camera_name}' is not a camera")

        bpy.context.scene.camera = camera

        logger.info(f"Set active camera to: {camera_name}")

        return {
            "active_camera_set": True,
            "camera_name": camera_name
        }


class SetCameraPropertiesHandler(BaseHandler):
    """Handler for setting camera properties"""

    def get_command_name(self) -> str:
        return "set_camera_properties"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "camera_name": {"type": str, "required": True},
            "lens": {"type": (int, float), "required": False},
            "sensor_width": {"type": (int, float), "required": False},
            "clip_start": {"type": (int, float), "required": False},
            "clip_end": {"type": (int, float), "required": False},
            "type": {"type": str, "required": False},
            "shift_x": {"type": (int, float), "required": False},
            "shift_y": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set camera properties"""
        camera_name = params["camera_name"]

        camera_obj = bpy.data.objects.get(camera_name)
        if not camera_obj or camera_obj.type != 'CAMERA':
            raise ValueError(f"Camera '{camera_name}' not found")

        camera = camera_obj.data

        # Set properties if provided
        if "lens" in params:
            camera.lens = params["lens"]
        if "sensor_width" in params:
            camera.sensor_width = params["sensor_width"]
        if "clip_start" in params:
            camera.clip_start = params["clip_start"]
        if "clip_end" in params:
            camera.clip_end = params["clip_end"]
        if "type" in params:
            camera.type = params["type"]
        if "shift_x" in params:
            camera.shift_x = params["shift_x"]
        if "shift_y" in params:
            camera.shift_y = params["shift_y"]

        logger.info(f"Updated camera properties: {camera_name}")

        return {
            "properties_set": True,
            "camera_name": camera_name,
            "lens": camera.lens,
            "sensor_width": camera.sensor_width,
            "clip_start": camera.clip_start,
            "clip_end": camera.clip_end,
            "type": camera.type
        }


class SetCameraDOFHandler(BaseHandler):
    """Handler for setting camera depth of field"""

    def get_command_name(self) -> str:
        return "set_camera_dof"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "camera_name": {"type": str, "required": True},
            "use_dof": {"type": bool, "required": False},
            "focus_distance": {"type": (int, float), "required": False},
            "focus_object": {"type": str, "required": False},
            "aperture_fstop": {"type": (int, float), "required": False},
            "aperture_blades": {"type": int, "required": False},
            "aperture_rotation": {"type": (int, float), "required": False},
            "aperture_ratio": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set camera depth of field settings"""
        camera_name = params["camera_name"]

        camera_obj = bpy.data.objects.get(camera_name)
        if not camera_obj or camera_obj.type != 'CAMERA':
            raise ValueError(f"Camera '{camera_name}' not found")

        camera = camera_obj.data
        dof = camera.dof

        # Enable/disable DOF
        if "use_dof" in params:
            dof.use_dof = params["use_dof"]

        # Set focus distance
        if "focus_distance" in params:
            dof.focus_distance = params["focus_distance"]

        # Set focus object
        if "focus_object" in params:
            focus_obj = bpy.data.objects.get(params["focus_object"])
            if focus_obj:
                dof.focus_object = focus_obj

        # Set aperture settings
        if "aperture_fstop" in params:
            dof.aperture_fstop = params["aperture_fstop"]
        if "aperture_blades" in params:
            dof.aperture_blades = params["aperture_blades"]
        if "aperture_rotation" in params:
            dof.aperture_rotation = params["aperture_rotation"]
        if "aperture_ratio" in params:
            dof.aperture_ratio = params["aperture_ratio"]

        logger.info(f"Set DOF for camera: {camera_name}")

        return {
            "dof_set": True,
            "camera_name": camera_name,
            "use_dof": dof.use_dof,
            "focus_distance": dof.focus_distance,
            "aperture_fstop": dof.aperture_fstop
        }


class GetCameraInfoHandler(BaseHandler):
    """Handler for getting camera information"""

    def get_command_name(self) -> str:
        return "get_camera_info"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "camera_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get camera information"""
        camera_name = params["camera_name"]

        camera_obj = bpy.data.objects.get(camera_name)
        if not camera_obj or camera_obj.type != 'CAMERA':
            raise ValueError(f"Camera '{camera_name}' not found")

        camera = camera_obj.data
        dof = camera.dof

        return {
            "name": camera_obj.name,
            "location": list(camera_obj.location),
            "rotation": list(camera_obj.rotation_euler),
            "lens": camera.lens,
            "sensor_width": camera.sensor_width,
            "clip_start": camera.clip_start,
            "clip_end": camera.clip_end,
            "type": camera.type,
            "dof": {
                "use_dof": dof.use_dof,
                "focus_distance": dof.focus_distance,
                "focus_object": dof.focus_object.name if dof.focus_object else None,
                "aperture_fstop": dof.aperture_fstop,
                "aperture_blades": dof.aperture_blades
            },
            "is_active": bpy.context.scene.camera == camera_obj
        }


class AddCameraConstraintHandler(BaseHandler):
    """Handler for adding constraints to cameras"""

    def get_command_name(self) -> str:
        return "add_camera_constraint"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "camera_name": {"type": str, "required": True},
            "constraint_type": {"type": str, "required": True},
            "constraint_name": {"type": str, "required": True},
            "target": {"type": str, "required": False},
            "settings": {"type": dict, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Add a constraint to a camera"""
        camera_name = params["camera_name"]
        constraint_type = params["constraint_type"]
        constraint_name = params["constraint_name"]
        target = params.get("target")
        settings = params.get("settings", {})

        camera_obj = bpy.data.objects.get(camera_name)
        if not camera_obj or camera_obj.type != 'CAMERA':
            raise ValueError(f"Camera '{camera_name}' not found")

        # Add constraint
        constraint = camera_obj.constraints.new(type=constraint_type)
        constraint.name = constraint_name

        # Set target if provided
        if target:
            target_obj = bpy.data.objects.get(target)
            if target_obj:
                constraint.target = target_obj

        # Apply additional settings
        for key, value in settings.items():
            if hasattr(constraint, key):
                setattr(constraint, key, value)

        logger.info(f"Added {constraint_type} constraint to camera: {camera_name}")

        return {
            "constraint_added": True,
            "camera_name": camera_name,
            "constraint_name": constraint_name,
            "constraint_type": constraint_type
        }
