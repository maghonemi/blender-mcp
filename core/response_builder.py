# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import time
from typing import Any, Dict, List, Optional
from datetime import datetime
import bpy

class ResponseBuilder:
    """Builds standardized responses for MCP commands"""
    
    @staticmethod
    def success(
        result: Any,
        warnings: Optional[List[Dict[str, str]]] = None,
        suggestions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build a success response"""
        response = {
            "status": "success",
            "result": result
        }
        
        if warnings:
            response["warnings"] = warnings
        
        if suggestions:
            response["suggestions"] = suggestions
        
        # Add context
        response["context"] = ResponseBuilder._get_context()
        
        # Add metadata
        response_metadata = {
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }
        response["metadata"] = response_metadata
        
        return response
    
    @staticmethod
    def error(
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Build an error response"""
        response = {
            "status": "error",
            "error": {
                "code": error_code,
                "message": message,
                "details": details or {}
            }
        }
        
        if suggestions:
            response["suggestions"] = suggestions
        
        response["context"] = ResponseBuilder._get_context()
        response["metadata"] = {
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    @staticmethod
    def partial(
        result: Any,
        completed: int,
        total: int,
        warnings: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Build a partial success response (for long operations)"""
        response = {
            "status": "partial",
            "result": result,
            "progress": {
                "completed": completed,
                "total": total,
                "percentage": (completed / total * 100) if total > 0 else 0
            }
        }
        
        if warnings:
            response["warnings"] = warnings
        
        response["context"] = ResponseBuilder._get_context()
        response["metadata"] = {
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    @staticmethod
    def _get_context() -> Dict[str, Any]:
        """Get current Blender context information"""
        try:
            scene = bpy.context.scene
            active_obj = bpy.context.active_object
            
            context = {
                "scene": scene.name if scene else None,
                "active_object": active_obj.name if active_obj else None,
                "selected_objects": [obj.name for obj in bpy.context.selected_objects],
                "frame_current": scene.frame_current if scene else None
            }
            
            return context
        except Exception:
            return {}
