# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025
# Action handlers for reusable animation blocks

import bpy
from typing import Dict, Any, List
from handlers.base_handler import BaseHandler
from utils.logger import logger


class CreateActionHandler(BaseHandler):
    """Handler for creating a new action (animation block)"""

    def get_command_name(self) -> str:
        return "create_action"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "action_name": {"type": str, "required": True},
            "fake_user": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Create a new action"""
        action_name = params["action_name"]
        fake_user = params.get("fake_user", True)

        # Check if action already exists
        if action_name in bpy.data.actions:
            return {
                "created": False,
                "message": f"Action '{action_name}' already exists",
                "action_name": action_name
            }

        # Create new action
        action = bpy.data.actions.new(name=action_name)
        action.use_fake_user = fake_user

        logger.info(f"Created action: {action_name}")

        return {
            "created": True,
            "action_name": action.name,
            "fake_user": action.use_fake_user
        }


class AssignActionHandler(BaseHandler):
    """Handler for assigning an action to an object"""

    def get_command_name(self) -> str:
        return "assign_action"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "action_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Assign an action to an object"""
        object_name = params["object_name"]
        action_name = params["action_name"]

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        action = bpy.data.actions.get(action_name)
        if not action:
            raise ValueError(f"Action '{action_name}' not found")

        # Ensure object has animation data
        if not obj.animation_data:
            obj.animation_data_create()

        # Assign action
        obj.animation_data.action = action

        logger.info(f"Assigned action '{action_name}' to '{object_name}'")

        return {
            "assigned": True,
            "object_name": object_name,
            "action_name": action_name
        }


class GetActionInfoHandler(BaseHandler):
    """Handler for getting action information"""

    def get_command_name(self) -> str:
        return "get_action_info"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "action_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get information about an action"""
        action_name = params["action_name"]

        action = bpy.data.actions.get(action_name)
        if not action:
            raise ValueError(f"Action '{action_name}' not found")

        # Get frame range
        frame_range = action.frame_range

        # Get FCurves info
        fcurves = []
        for fcurve in action.fcurves:
            fcurves.append({
                "data_path": fcurve.data_path,
                "array_index": fcurve.array_index,
                "keyframe_count": len(fcurve.keyframe_points)
            })

        return {
            "action_name": action.name,
            "frame_start": frame_range[0],
            "frame_end": frame_range[1],
            "frame_count": int(frame_range[1] - frame_range[0]) + 1,
            "fcurves": fcurves,
            "fcurve_count": len(action.fcurves),
            "use_fake_user": action.use_fake_user,
            "users": action.users
        }


class ListActionsHandler(BaseHandler):
    """Handler for listing all actions in the blend file"""

    def get_command_name(self) -> str:
        return "list_actions"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, params: Dict[str, Any]) -> Any:
        """List all actions"""
        actions = []

        for action in bpy.data.actions:
            frame_range = action.frame_range
            actions.append({
                "name": action.name,
                "frame_start": frame_range[0],
                "frame_end": frame_range[1],
                "fcurve_count": len(action.fcurves),
                "use_fake_user": action.use_fake_user,
                "users": action.users
            })

        return {
            "actions": actions,
            "count": len(actions)
        }


class DuplicateActionHandler(BaseHandler):
    """Handler for duplicating an action"""

    def get_command_name(self) -> str:
        return "duplicate_action"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "source_action": {"type": str, "required": True},
            "new_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Duplicate an action"""
        source_name = params["source_action"]
        new_name = params["new_name"]

        source_action = bpy.data.actions.get(source_name)
        if not source_action:
            raise ValueError(f"Source action '{source_name}' not found")

        # Duplicate
        new_action = source_action.copy()
        new_action.name = new_name

        logger.info(f"Duplicated action '{source_name}' as '{new_name}'")

        return {
            "duplicated": True,
            "source_action": source_name,
            "new_action": new_action.name
        }


class DeleteActionHandler(BaseHandler):
    """Handler for deleting an action"""

    def get_command_name(self) -> str:
        return "delete_action"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "action_name": {"type": str, "required": True},
            "force": {"type": bool, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Delete an action"""
        action_name = params["action_name"]
        force = params.get("force", False)

        action = bpy.data.actions.get(action_name)
        if not action:
            raise ValueError(f"Action '{action_name}' not found")

        # Check users
        if action.users > 0 and not force:
            return {
                "deleted": False,
                "message": f"Action '{action_name}' has {action.users} users. Use force=True to delete anyway.",
                "action_name": action_name
            }

        # Remove fake user if needed
        action.use_fake_user = False

        # Delete
        bpy.data.actions.remove(action)

        logger.info(f"Deleted action: {action_name}")

        return {
            "deleted": True,
            "action_name": action_name
        }


class PushDownActionHandler(BaseHandler):
    """Handler for pushing action down to NLA track"""

    def get_command_name(self) -> str:
        return "push_down_action"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True},
            "track_name": {"type": str, "required": False}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Push current action to NLA track"""
        object_name = params["object_name"]
        track_name = params.get("track_name")

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data or not obj.animation_data.action:
            raise ValueError("Object has no active action to push down")

        action = obj.animation_data.action

        # Create NLA track if needed
        if track_name:
            track = obj.animation_data.nla_tracks.new()
            track.name = track_name
        else:
            # Use default or create new
            if obj.animation_data.nla_tracks:
                track = obj.animation_data.nla_tracks[-1]
            else:
                track = obj.animation_data.nla_tracks.new()
                track.name = "NlaTrack"

        # Create strip from action
        frame_start = int(action.frame_range[0])
        strip = track.strips.new(action.name, frame_start, action)

        # Clear the active action
        obj.animation_data.action = None

        logger.info(f"Pushed action to NLA track '{track.name}'")

        return {
            "pushed_down": True,
            "object_name": object_name,
            "action_name": action.name,
            "track_name": track.name,
            "strip_name": strip.name
        }


class GetObjectActionHandler(BaseHandler):
    """Handler for getting the current action assigned to an object"""

    def get_command_name(self) -> str:
        return "get_object_action"

    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "object_name": {"type": str, "required": True}
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        """Get the action currently assigned to an object"""
        object_name = params["object_name"]

        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")

        if not obj.animation_data:
            return {
                "object_name": object_name,
                "has_animation_data": False,
                "action": None
            }

        action = obj.animation_data.action

        if not action:
            return {
                "object_name": object_name,
                "has_animation_data": True,
                "action": None
            }

        frame_range = action.frame_range

        return {
            "object_name": object_name,
            "has_animation_data": True,
            "action": {
                "name": action.name,
                "frame_start": frame_range[0],
                "frame_end": frame_range[1],
                "fcurve_count": len(action.fcurves)
            }
        }
