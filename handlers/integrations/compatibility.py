# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

"""
Compatibility layer for existing integrations.
This module provides handlers that wrap the original integration methods.
"""

import bpy
import sys
import os
from typing import Dict, Any

# Try to import original addon methods
# We'll create a bridge to the original BlenderMCPServer methods

class IntegrationBridge:
    """Bridge to original integration methods"""
    
    _original_server = None
    
    @classmethod
    def set_original_server(cls, server):
        """Set the original server instance"""
        cls._original_server = server
    
    @classmethod
    def get_original_server(cls):
        """Get the original server instance"""
        return cls._original_server

# These handlers will be registered and will delegate to original methods
# The original addon.py methods will be accessible through the bridge
