# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

from typing import Any, Dict, Optional, List
from abc import ABC, abstractmethod
from core.context_manager import context_manager
from core.response_builder import ResponseBuilder
from utils.error_handler import handle_error, ErrorCode, create_error_response
from utils.validation import ParameterValidator, ValidationError
from utils.logger import logger

class BaseHandler(ABC):
    """Base class for all command handlers"""
    
    def __init__(self):
        self.context_manager = context_manager
        self.response_builder = ResponseBuilder
        self.validator = ParameterValidator()
    
    @abstractmethod
    def get_command_name(self) -> str:
        """Return the command name this handler processes"""
        pass
    
    @abstractmethod
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        """Return the parameter schema for validation"""
        pass
    
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        """Execute the command with given parameters"""
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> List[str]:
        """Validate parameters against schema"""
        schema = self.get_parameter_schema()
        return self.validator.validate(params, schema)
    
    def handle(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Main handler method that validates and executes"""
        try:
            params = command.get("params", {})
            
            # Validate parameters
            errors = self.validate_params(params)
            if errors:
                return self.response_builder.error(
                    error_code=ErrorCode.INVALID_PARAMETER.value,
                    message=f"Validation failed: {'; '.join(errors)}",
                    suggestions=["Check parameter types and values", "Refer to command documentation"]
                )
            
            # Execute command
            logger.info(f"Executing command: {self.get_command_name()}")
            result = self.execute(params)
            
            # Check if result contains an error (for handlers that return {"error": "..."} format)
            if isinstance(result, dict) and "error" in result:
                error_msg = result.get("error", "Unknown error")
                return self.response_builder.error(
                    error_code=ErrorCode.API_ERROR.value,
                    message=error_msg,
                    suggestions=["Check API configuration", "Verify API key is correct"]
                )
            
            # Build success response
            return self.response_builder.success(result)
            
        except ValidationError as e:
            return self.response_builder.error(
                error_code=ErrorCode.INVALID_PARAMETER.value,
                message=str(e),
                suggestions=["Check parameter values"]
            )
        except Exception as e:
            return handle_error(e, self.get_command_name())
    
    def get_help(self) -> str:
        """Return help text for this command"""
        return f"Command: {self.get_command_name()}"
    
    def get_examples(self) -> List[Dict[str, Any]]:
        """Return example usage"""
        return []
