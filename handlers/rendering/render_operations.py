# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Render operations handlers for movie production workflow

"""
Render operations handlers for actually rendering images and animations
"""

from typing import Any, Dict
import bpy
import os
from handlers.base_handler import BaseHandler
from utils.logger import logger


class SetRenderEngineHandler(BaseHandler):
    """Handler for setting the render engine"""

    def get_command_name(self) -> str:
        return "set_render_engine"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "engine": {"type": str, "required": True},
            "device": {"type": str, "required": False},
            "feature_set": {"type": str, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set the render engine"""
        engine = params["engine"].upper()
        device = params.get("device", "GPU")
        feature_set = params.get("feature_set", "SUPPORTED")

        # Map engine names
        engine_map = {
            "CYCLES": "CYCLES",
            "EEVEE": "BLENDER_EEVEE_NEXT",
            "BLENDER_EEVEE": "BLENDER_EEVEE_NEXT",
            "BLENDER_EEVEE_NEXT": "BLENDER_EEVEE_NEXT",
            "WORKBENCH": "BLENDER_WORKBENCH",
            "BLENDER_WORKBENCH": "BLENDER_WORKBENCH"
        }

        render_engine = engine_map.get(engine)
        if not render_engine:
            raise ValueError(f"Invalid engine '{engine}'. Valid options: CYCLES, EEVEE, WORKBENCH")

        bpy.context.scene.render.engine = render_engine

        # Set Cycles-specific options
        if render_engine == "CYCLES":
            cycles = bpy.context.scene.cycles

            # Set device
            if device.upper() == "GPU":
                cycles.device = 'GPU'
                # Try to enable GPU compute
                try:
                    prefs = bpy.context.preferences.addons['cycles'].preferences
                    prefs.compute_device_type = 'CUDA'  # or 'OPTIX', 'HIP', 'METAL'
                    for device_entry in prefs.devices:
                        device_entry.use = True
                except Exception as e:
                    logger.warning(f"Could not configure GPU: {e}")
            else:
                cycles.device = 'CPU'

            # Set feature set
            if feature_set.upper() == "EXPERIMENTAL":
                cycles.feature_set = 'EXPERIMENTAL'
            else:
                cycles.feature_set = 'SUPPORTED'

        logger.info(f"Set render engine to {render_engine}")

        return {
            "engine": bpy.context.scene.render.engine,
            "device": device,
            "set": True
        }


class SetRenderResolutionHandler(BaseHandler):
    """Handler for setting render resolution"""

    def get_command_name(self) -> str:
        return "set_render_resolution"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "resolution_x": {"type": int, "required": True},
            "resolution_y": {"type": int, "required": True},
            "resolution_percentage": {"type": int, "required": False},
            "pixel_aspect_x": {"type": (int, float), "required": False},
            "pixel_aspect_y": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set render resolution"""
        resolution_x = params["resolution_x"]
        resolution_y = params["resolution_y"]
        resolution_percentage = params.get("resolution_percentage", 100)
        pixel_aspect_x = params.get("pixel_aspect_x", 1.0)
        pixel_aspect_y = params.get("pixel_aspect_y", 1.0)

        render = bpy.context.scene.render

        render.resolution_x = resolution_x
        render.resolution_y = resolution_y
        render.resolution_percentage = resolution_percentage
        render.pixel_aspect_x = pixel_aspect_x
        render.pixel_aspect_y = pixel_aspect_y

        logger.info(f"Set render resolution to {resolution_x}x{resolution_y} at {resolution_percentage}%")

        return {
            "resolution_x": render.resolution_x,
            "resolution_y": render.resolution_y,
            "resolution_percentage": render.resolution_percentage,
            "effective_resolution": [
                int(resolution_x * resolution_percentage / 100),
                int(resolution_y * resolution_percentage / 100)
            ],
            "set": True
        }


class SetRenderSamplesHandler(BaseHandler):
    """Handler for setting render samples and quality"""

    def get_command_name(self) -> str:
        return "set_render_samples"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "samples": {"type": int, "required": True},
            "use_denoising": {"type": bool, "required": False},
            "denoiser": {"type": str, "required": False},
            "use_adaptive_sampling": {"type": bool, "required": False},
            "adaptive_threshold": {"type": (int, float), "required": False},
            "time_limit": {"type": (int, float), "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Set render samples and denoising"""
        samples = params["samples"]
        use_denoising = params.get("use_denoising", True)
        denoiser = params.get("denoiser", "OPENIMAGEDENOISE")
        use_adaptive_sampling = params.get("use_adaptive_sampling", True)
        adaptive_threshold = params.get("adaptive_threshold", 0.01)
        time_limit = params.get("time_limit", 0)

        scene = bpy.context.scene
        render_engine = scene.render.engine

        result = {
            "engine": render_engine,
            "samples": samples,
            "set": True
        }

        if render_engine == "CYCLES":
            cycles = scene.cycles
            cycles.samples = samples
            cycles.use_denoising = use_denoising

            if use_denoising:
                # Set denoiser
                denoiser_map = {
                    "OPENIMAGEDENOISE": "OPENIMAGEDENOISE",
                    "OPTIX": "OPTIX",
                    "OID": "OPENIMAGEDENOISE"
                }
                cycles.denoiser = denoiser_map.get(denoiser.upper(), "OPENIMAGEDENOISE")

            # Adaptive sampling
            cycles.use_adaptive_sampling = use_adaptive_sampling
            if use_adaptive_sampling:
                cycles.adaptive_threshold = adaptive_threshold

            # Time limit (0 = no limit)
            cycles.time_limit = time_limit

            result["use_denoising"] = cycles.use_denoising
            result["denoiser"] = cycles.denoiser if use_denoising else None
            result["use_adaptive_sampling"] = cycles.use_adaptive_sampling
            result["adaptive_threshold"] = cycles.adaptive_threshold

        elif "EEVEE" in render_engine:
            eevee = scene.eevee
            eevee.taa_render_samples = samples

            result["taa_render_samples"] = eevee.taa_render_samples

        logger.info(f"Set render samples to {samples}")

        return result


class RenderImageHandler(BaseHandler):
    """Handler for rendering a single image"""

    def get_command_name(self) -> str:
        return "render_image"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "filepath": {"type": str, "required": False},
            "camera": {"type": str, "required": False},
            "frame": {"type": int, "required": False},
            "write_still": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Render a single image"""
        filepath = params.get("filepath")
        camera_name = params.get("camera")
        frame = params.get("frame")
        write_still = params.get("write_still", True)

        scene = bpy.context.scene

        # Set camera if specified
        if camera_name:
            camera = bpy.data.objects.get(camera_name)
            if not camera or camera.type != 'CAMERA':
                raise ValueError(f"Camera '{camera_name}' not found")
            scene.camera = camera

        # Check if we have a camera
        if not scene.camera:
            raise ValueError("No camera in scene. Create a camera first.")

        # Set frame if specified
        original_frame = scene.frame_current
        if frame:
            scene.frame_set(frame)

        # Set output path if specified
        original_filepath = scene.render.filepath
        if filepath:
            # Ensure directory exists
            output_dir = os.path.dirname(filepath)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            scene.render.filepath = filepath

        try:
            # Render
            logger.info(f"Rendering image to {scene.render.filepath}")
            bpy.ops.render.render(write_still=write_still)

            result = {
                "rendered": True,
                "filepath": scene.render.filepath,
                "camera": scene.camera.name,
                "frame": scene.frame_current,
                "resolution": [scene.render.resolution_x, scene.render.resolution_y],
                "engine": scene.render.engine
            }

        finally:
            # Restore original settings
            if filepath:
                scene.render.filepath = original_filepath
            if frame:
                scene.frame_set(original_frame)

        return result


class RenderAnimationHandler(BaseHandler):
    """Handler for rendering an animation sequence"""

    def get_command_name(self) -> str:
        return "render_animation"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "filepath": {"type": str, "required": False},
            "frame_start": {"type": int, "required": False},
            "frame_end": {"type": int, "required": False},
            "camera": {"type": str, "required": False},
            "file_format": {"type": str, "required": False},
            "use_placeholder": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Render an animation sequence"""
        filepath = params.get("filepath")
        frame_start = params.get("frame_start")
        frame_end = params.get("frame_end")
        camera_name = params.get("camera")
        file_format = params.get("file_format")
        use_placeholder = params.get("use_placeholder", False)

        scene = bpy.context.scene

        # Set camera if specified
        if camera_name:
            camera = bpy.data.objects.get(camera_name)
            if not camera or camera.type != 'CAMERA':
                raise ValueError(f"Camera '{camera_name}' not found")
            scene.camera = camera

        # Check if we have a camera
        if not scene.camera:
            raise ValueError("No camera in scene. Create a camera first.")

        # Store original settings
        original_start = scene.frame_start
        original_end = scene.frame_end
        original_filepath = scene.render.filepath
        original_format = scene.render.image_settings.file_format

        try:
            # Set frame range if specified
            if frame_start:
                scene.frame_start = frame_start
            if frame_end:
                scene.frame_end = frame_end

            # Set output path if specified
            if filepath:
                output_dir = os.path.dirname(filepath)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                scene.render.filepath = filepath

            # Set file format if specified
            if file_format:
                format_map = {
                    "PNG": "PNG",
                    "JPEG": "JPEG",
                    "OPEN_EXR": "OPEN_EXR",
                    "EXR": "OPEN_EXR",
                    "FFMPEG": "FFMPEG"
                }
                scene.render.image_settings.file_format = format_map.get(file_format.upper(), "PNG")

            # Set placeholder option
            scene.render.use_placeholder = use_placeholder

            # Render animation
            total_frames = scene.frame_end - scene.frame_start + 1
            logger.info(f"Rendering animation: frames {scene.frame_start}-{scene.frame_end} ({total_frames} frames)")

            bpy.ops.render.render(animation=True)

            result = {
                "rendered": True,
                "filepath": scene.render.filepath,
                "camera": scene.camera.name,
                "frame_start": scene.frame_start,
                "frame_end": scene.frame_end,
                "total_frames": total_frames,
                "file_format": scene.render.image_settings.file_format,
                "resolution": [scene.render.resolution_x, scene.render.resolution_y],
                "engine": scene.render.engine
            }

        finally:
            # Restore original settings
            scene.frame_start = original_start
            scene.frame_end = original_end
            scene.render.filepath = original_filepath
            scene.render.image_settings.file_format = original_format

        return result


class GetRenderProgressHandler(BaseHandler):
    """Handler for getting render progress information"""

    def get_command_name(self) -> str:
        return "get_render_progress"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get current render progress (if rendering)"""
        scene = bpy.context.scene

        return {
            "engine": scene.render.engine,
            "resolution": [scene.render.resolution_x, scene.render.resolution_y],
            "frame_current": scene.frame_current,
            "frame_start": scene.frame_start,
            "frame_end": scene.frame_end,
            "output_path": scene.render.filepath,
            "file_format": scene.render.image_settings.file_format,
            "camera": scene.camera.name if scene.camera else None
        }
