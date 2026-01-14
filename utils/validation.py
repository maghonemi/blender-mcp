# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

from typing import Any, Dict, List, Callable, Optional, Union
from utils.error_handler import ErrorCode, create_error_response
from utils.logger import logger

class ValidationError(Exception):
    """Exception raised when validation fails"""
    pass

class ParameterValidator:
    """Parameter validation system"""
    
    @staticmethod
    def validate(params: Dict[str, Any], schema: Dict[str, Dict[str, Any]]) -> List[str]:
        """
        Validate parameters against schema.
        
        Returns list of error messages. Empty list if valid.
        """
        errors = []
        
        for field, rules in schema.items():
            value = params.get(field)
            
            # Check if required
            if rules.get("required", False) and value is None:
                errors.append(f"{field} is required")
                continue
            
            # Skip validation if value is None and not required
            if value is None:
                continue
            
            # Type check
            expected_type = rules.get("type")
            if expected_type:
                # Handle union types (tuple of types)
                if isinstance(expected_type, tuple):
                    if not isinstance(value, expected_type):
                        errors.append(f"{field} must be one of {[t.__name__ for t in expected_type]}")
                        continue
                else:
                    if not isinstance(value, expected_type):
                        errors.append(f"{field} must be {expected_type.__name__}")
                        continue
            
            # Custom validator
            validator = rules.get("validator")
            if validator:
                try:
                    validator(value)
                except ValidationError as e:
                    errors.append(f"{field}: {str(e)}")
                except Exception as e:
                    errors.append(f"{field}: validation error - {str(e)}")
        
        return errors
    
    @staticmethod
    def validate_and_raise(params: Dict[str, Any], schema: Dict[str, Dict[str, Any]]) -> None:
        """Validate and raise ValidationError if invalid"""
        errors = ParameterValidator.validate(params, schema)
        if errors:
            raise ValidationError(f"Validation failed: {'; '.join(errors)}")

# Common validators
def validate_object_exists(value: str) -> None:
    """Validate that an object exists in the scene"""
    import bpy
    if value not in bpy.data.objects:
        raise ValidationError(f"Object '{value}' not found in scene")

def validate_data_path(value: str) -> None:
    """Validate that a data path is valid"""
    if not value or not isinstance(value, str):
        raise ValidationError("Data path must be a non-empty string")
    # Basic validation - can be extended
    if value.startswith(".") or ".." in value:
        raise ValidationError("Invalid data path format")

def validate_frame(value: int) -> None:
    """Validate frame number"""
    if not isinstance(value, int) or value < 1:
        raise ValidationError("Frame must be a positive integer")

def validate_positive_number(value: Union[int, float]) -> None:
    """Validate that a number is positive"""
    if value <= 0:
        raise ValidationError("Value must be positive")

def validate_range(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> None:
    """Validate that a value is within a range"""
    if value < min_val or value > max_val:
        raise ValidationError(f"Value must be between {min_val} and {max_val}")

def validate_enum(value: Any, allowed_values: List[Any]) -> None:
    """Validate that a value is in allowed list"""
    if value not in allowed_values:
        raise ValidationError(f"Value must be one of {allowed_values}")

# Common schemas
OBJECT_NAME_SCHEMA = {
    "object_name": {
        "type": str,
        "required": True,
        "validator": validate_object_exists
    }
}

FRAME_SCHEMA = {
    "frame": {
        "type": int,
        "required": True,
        "validator": validate_frame
    }
}

DATA_PATH_SCHEMA = {
    "data_path": {
        "type": str,
        "required": True,
        "validator": validate_data_path
    }
}
