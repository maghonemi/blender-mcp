# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import bpy
import threading
from typing import Any, Callable, Optional, Dict
from utils.logger import logger

class ContextManager:
    """Manages Blender context and ensures thread-safe operations"""
    
    def __init__(self):
        self._lock = threading.Lock()
    
    def get_object(self, name: str) -> Optional[bpy.types.Object]:
        """Get object by name"""
        return bpy.data.objects.get(name)
    
    def get_scene(self, name: Optional[str] = None) -> bpy.types.Scene:
        """Get scene by name, or current scene if None"""
        if name:
            return bpy.data.scenes.get(name) or bpy.context.scene
        return bpy.context.scene
    
    def get_active_object(self) -> Optional[bpy.types.Object]:
        """Get currently active object"""
        return bpy.context.active_object
    
    def get_selected_objects(self) -> list:
        """Get currently selected objects"""
        return list(bpy.context.selected_objects)
    
    def set_active_object(self, obj: bpy.types.Object) -> None:
        """Set active object"""
        bpy.context.view_layer.objects.active = obj
    
    def select_object(self, obj: bpy.types.Object, deselect_all: bool = False) -> None:
        """Select an object"""
        if deselect_all:
            bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        self.set_active_object(obj)
    
    def select_objects(self, objects: list, deselect_all: bool = False) -> None:
        """Select multiple objects"""
        if deselect_all:
            bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            if obj:
                obj.select_set(True)
        if objects:
            self.set_active_object(objects[0])
    
    def ensure_context(self, context_override: Optional[Dict[str, Any]] = None) -> Any:
        """Ensure we have the right context, returns context manager"""
        if context_override:
            return bpy.context.temp_override(**context_override)
        return bpy.context
    
    def execute_in_main_thread(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function in Blender's main thread.
        This is a blocking call that waits for execution.
        """
        result = [None]
        exception = [None]
        event = threading.Event()
        
        def wrapper():
            try:
                result[0] = func(*args, **kwargs)
            except Exception as e:
                exception[0] = e
            finally:
                event.set()
        
        # Schedule execution in main thread
        bpy.app.timers.register(wrapper, first_interval=0.0)
        
        # Wait for execution (with timeout)
        timeout = 30.0  # 30 second timeout
        if not event.wait(timeout):
            raise TimeoutError(f"Operation timed out after {timeout} seconds")
        
        if exception[0]:
            raise exception[0]
        
        return result[0]
    
    def get_viewport_area(self) -> Optional[bpy.types.Area]:
        """Get the active 3D viewport area"""
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                return area
        return None

# Global context manager instance
context_manager = ContextManager()
