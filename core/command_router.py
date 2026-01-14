# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

from typing import Dict, Optional, Type
from handlers.base_handler import BaseHandler
from core.response_builder import ResponseBuilder
from utils.error_handler import ErrorCode, create_error_response
from utils.logger import logger

class CommandRouter:
    """Routes commands to appropriate handlers"""
    
    def __init__(self):
        self._handlers: Dict[str, BaseHandler] = {}
        self._handler_classes: Dict[str, Type[BaseHandler]] = {}
    
    def register_handler(self, handler: BaseHandler) -> None:
        """Register a handler instance"""
        command_name = handler.get_command_name()
        self._handlers[command_name] = handler
        logger.info(f"Registered handler for command: {command_name}")
    
    def register_handler_class(self, handler_class: Type[BaseHandler]) -> None:
        """Register a handler class (will be instantiated on first use)"""
        handler_instance = handler_class()
        command_name = handler_instance.get_command_name()
        self._handler_classes[command_name] = handler_class
        logger.info(f"Registered handler class for command: {command_name}")
    
    def route_command(self, command: Dict) -> Dict:
        """Route a command to the appropriate handler"""
        try:
            # Validate command is a dictionary
            if not isinstance(command, dict):
                if isinstance(command, str):
                    # Try to parse if it's a JSON string
                    try:
                        import json
                        command = json.loads(command)
                    except json.JSONDecodeError:
                        return ResponseBuilder.error(
                            error_code=ErrorCode.INVALID_COMMAND.value,
                            message=f"Command must be a dictionary or valid JSON, got: {type(command).__name__}",
                            suggestions=["Ensure command is a valid JSON object", "Check command format"]
                        )
                else:
                    return ResponseBuilder.error(
                        error_code=ErrorCode.INVALID_COMMAND.value,
                        message=f"Command must be a dictionary, got: {type(command).__name__}",
                        suggestions=["Ensure command is a dictionary", "Check command format"]
                    )
            
            # Now safe to use .get()
            command_type = command.get("type")
            if not command_type:
                return ResponseBuilder.error(
                    error_code=ErrorCode.INVALID_COMMAND.value,
                    message="Command type is required",
                    suggestions=["Include 'type' field in command"]
                )
            
            # Try to get handler instance
            handler = self._handlers.get(command_type)
            
            # If not found, try to instantiate from class
            if handler is None:
                handler_class = self._handler_classes.get(command_type)
                if handler_class:
                    handler = handler_class()
                    self._handlers[command_type] = handler
                else:
                    return ResponseBuilder.error(
                        error_code=ErrorCode.INVALID_COMMAND.value,
                        message=f"Unknown command type: {command_type}",
                        suggestions=[
                            f"Command '{command_type}' is not registered",
                            "Check available commands",
                            "Verify command name spelling"
                        ]
                    )
            
            # Execute handler
            return handler.handle(command)
            
        except Exception as e:
            logger.exception(f"Error routing command: {str(e)}")
            return ResponseBuilder.error(
                error_code=ErrorCode.UNKNOWN_ERROR.value,
                message=f"Error routing command: {str(e)}",
                suggestions=["Check command format", "Verify handler is properly registered"]
            )
    
    def get_registered_commands(self) -> list:
        """Get list of all registered command names"""
        commands = list(self._handlers.keys())
        commands.extend(self._handler_classes.keys())
        return sorted(set(commands))
    
    def has_handler(self, command_type: str) -> bool:
        """Check if a handler exists for a command type"""
        return command_type in self._handlers or command_type in self._handler_classes

# Global router instance
command_router = CommandRouter()
