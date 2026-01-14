# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

from enum import Enum
from typing import Optional, List, Dict, Any
from utils.logger import logger

class ErrorCode(Enum):
    """Standard error codes for Blender MCP"""
    # General
    INVALID_COMMAND = "INVALID_COMMAND"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    
    # Objects
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    INVALID_OBJECT_TYPE = "INVALID_OBJECT_TYPE"
    OBJECT_EXISTS = "OBJECT_EXISTS"
    
    # Animation
    INVALID_FRAME = "INVALID_FRAME"
    INVALID_DATA_PATH = "INVALID_DATA_PATH"
    KEYFRAME_EXISTS = "KEYFRAME_EXISTS"
    NO_ANIMATION_DATA = "NO_ANIMATION_DATA"
    
    # Rigging
    NO_ARMATURE = "NO_ARMATURE"
    BONE_NOT_FOUND = "BONE_NOT_FOUND"
    INVALID_BONE_MODE = "INVALID_BONE_MODE"
    
    # Modeling
    MESH_NOT_FOUND = "MESH_NOT_FOUND"
    INVALID_SELECTION = "INVALID_SELECTION"
    OPERATION_FAILED = "OPERATION_FAILED"
    
    # Rendering
    RENDER_FAILED = "RENDER_FAILED"
    INVALID_CAMERA = "INVALID_CAMERA"
    INVALID_ENGINE = "INVALID_ENGINE"
    
    # Network
    CONNECTION_ERROR = "CONNECTION_ERROR"
    TIMEOUT = "TIMEOUT"
    
    # Integration
    API_KEY_MISSING = "API_KEY_MISSING"
    API_ERROR = "API_ERROR"

class BlenderMCPError(Exception):
    """Base exception for Blender MCP errors"""
    
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        self.suggestions = suggestions or []
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format"""
        return {
            "status": "error",
            "error": {
                "code": self.error_code.value,
                "message": self.message,
                "details": self.details
            },
            "suggestions": self.suggestions
        }

def handle_error(error: Exception, command_type: Optional[str] = None) -> Dict[str, Any]:
    """Handle an exception and return standardized error response"""
    logger.exception(f"Error in command {command_type}: {str(error)}")
    
    if isinstance(error, BlenderMCPError):
        return error.to_dict()
    
    # Convert generic exceptions to BlenderMCPError
    error_code = ErrorCode.UNKNOWN_ERROR
    message = str(error)
    suggestions = []
    
    # Try to provide helpful suggestions based on error type
    if "not found" in message.lower():
        error_code = ErrorCode.OBJECT_NOT_FOUND
        suggestions.append("Check that the object name is correct")
        suggestions.append("Ensure the object exists in the current scene")
    elif "invalid" in message.lower():
        error_code = ErrorCode.INVALID_PARAMETER
        suggestions.append("Check parameter values and types")
    elif "timeout" in message.lower():
        error_code = ErrorCode.TIMEOUT
        suggestions.append("The operation may have taken too long")
        suggestions.append("Try breaking the operation into smaller steps")
    
    return BlenderMCPError(
        error_code=error_code,
        message=message,
        suggestions=suggestions
    ).to_dict()

def create_error_response(
    error_code: ErrorCode,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    suggestions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Create a standardized error response"""
    return BlenderMCPError(
        error_code=error_code,
        message=message,
        details=details,
        suggestions=suggestions
    ).to_dict()
