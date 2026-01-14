# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
from typing import Dict, Any, Optional
from handlers.base_handler import BaseHandler
from utils.validation import OBJECT_NAME_SCHEMA
from utils.logger import logger

class AddConstraintHandler(BaseHandler):
    """Handler for adding constraints"""
    
    def get_command_name(self) -> str:
        return "add_constraint"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            "constraint_type": {
                "type": str,
                "required": True
            },
            "constraint_name": {
                "type": str,
                "required": True
            },
            "target": {
                "type": str,
                "required": False
            },
            "settings": {
                "type": dict,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Add a constraint to an object"""
        object_name = params["object_name"]
        constraint_type = params["constraint_type"]
        constraint_name = params["constraint_name"]
        target = params.get("target")
        settings = params.get("settings", {})
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        # Add constraint
        constraint = obj.constraints.new(type=constraint_type)
        constraint.name = constraint_name
        
        # Set target if provided
        if target:
            target_obj = bpy.data.objects.get(target)
            if target_obj:
                constraint.target = target_obj
        
        # Apply settings
        for key, value in settings.items():
            if hasattr(constraint, key):
                setattr(constraint, key, value)
        
        return {
            "constraint_added": True,
            "constraint_name": constraint_name,
            "constraint_type": constraint_type
        }

class ModifyConstraintHandler(BaseHandler):
    """Handler for modifying constraints"""
    
    def get_command_name(self) -> str:
        return "modify_constraint"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            "constraint_name": {
                "type": str,
                "required": True
            },
            "settings": {
                "type": dict,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Modify a constraint"""
        object_name = params["object_name"]
        constraint_name = params["constraint_name"]
        settings = params["settings"]
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        constraint = obj.constraints.get(constraint_name)
        if not constraint:
            raise ValueError(f"Constraint '{constraint_name}' not found")
        
        # Apply settings
        for key, value in settings.items():
            if hasattr(constraint, key):
                setattr(constraint, key, value)
        
        return {"modified": True, "constraint_name": constraint_name}

class RemoveConstraintHandler(BaseHandler):
    """Handler for removing constraints"""
    
    def get_command_name(self) -> str:
        return "remove_constraint"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            **OBJECT_NAME_SCHEMA,
            "constraint_name": {
                "type": str,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Remove a constraint"""
        object_name = params["object_name"]
        constraint_name = params["constraint_name"]
        
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")
        
        constraint = obj.constraints.get(constraint_name)
        if not constraint:
            raise ValueError(f"Constraint '{constraint_name}' not found")
        
        obj.constraints.remove(constraint)
        return {"removed": True, "constraint_name": constraint_name}
