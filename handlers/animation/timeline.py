# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any
from handlers.base_handler import BaseHandler
from utils.validation import FRAME_SCHEMA
from utils.logger import logger

class SetCurrentFrameHandler(BaseHandler):
    """Handler for setting current frame"""
    
    def get_command_name(self) -> str:
        return "set_current_frame"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return FRAME_SCHEMA
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Set the current frame"""
        frame = params["frame"]
        bpy.context.scene.frame_set(frame)
        return {"frame": frame}

class GetTimelineInfoHandler(BaseHandler):
    """Handler for getting timeline information"""
    
    def get_command_name(self) -> str:
        return "get_timeline_info"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {}
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get timeline information"""
        scene = bpy.context.scene
        return {
            "current_frame": scene.frame_current,
            "frame_start": scene.frame_start,
            "frame_end": scene.frame_end,
            "fps": scene.render.fps,
            "playback_mode": "PLAYBACK"  # Can be enhanced
        }

class SetFrameRangeHandler(BaseHandler):
    """Handler for setting frame range"""
    
    def get_command_name(self) -> str:
        return "set_frame_range"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "frame_start": {
                "type": int,
                "required": True
            },
            "frame_end": {
                "type": int,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Set frame range"""
        scene = bpy.context.scene
        scene.frame_start = params["frame_start"]
        scene.frame_end = params["frame_end"]
        return {
            "frame_start": scene.frame_start,
            "frame_end": scene.frame_end
        }

class PlaybackControlHandler(BaseHandler):
    """Handler for playback control"""
    
    def get_command_name(self) -> str:
        return "playback_control"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "action": {
                "type": str,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Control playback"""
        action = params["action"].upper()
        
        if action == "PLAY":
            bpy.ops.screen.animation_play()
        elif action == "PAUSE":
            bpy.ops.screen.animation_pause()
        elif action == "STOP":
            bpy.ops.screen.animation_cancel()
        elif action == "FRAME_NEXT":
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        elif action == "FRAME_PREVIOUS":
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
        
        return {"action": action, "current_frame": bpy.context.scene.frame_current}
