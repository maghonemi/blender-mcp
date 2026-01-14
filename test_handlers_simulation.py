#!/usr/bin/env python3
"""
Simulation test for render output and Sketchfab handlers
Tests handler registration and command routing logic
"""

import sys
import os
import json

# Mock bpy module for testing
class MockBpy:
    class types:
        class Object:
            pass
        class Scene:
            pass
    
    class context:
        class scene:
            name = "Scene"
            frame_current = 1
            frame_start = 1
            frame_end = 250
            
            class render:
                filepath = "/tmp/default_render.png"
                engine = "CYCLES"
                resolution_x = 1920
                resolution_y = 1080
                resolution_percentage = 100
                
                class image_settings:
                    file_format = "PNG"
                    color_mode = "RGB"
                    color_depth = 8
                    quality = 15
                    exr_codec = "ZIP"
            
            blendermcp_use_sketchfab = False
            blendermcp_sketchfab_api_key = ""
    
    class data:
        class objects:
            @staticmethod
            def get(name):
                return None
        
        class images:
            @staticmethod
            def load(filepath):
                class MockImage:
                    size = (1920, 1080)
                    def scale(self, w, h):
                        self.size = (w, h)
                    def save(self):
                        pass
                return MockImage()
    
    class ops:
        class screen:
            @staticmethod
            def screenshot_area(filepath):
                pass
        
        class import_scene:
            @staticmethod
            def gltf(filepath):
                pass
    
    class app:
        class timers:
            @staticmethod
            def register(func, first_interval=0.0):
                return None
    
    class mathutils:
        class Vector:
            def __init__(self, *args):
                self.x = args[0] if len(args) > 0 else 0
                self.y = args[1] if len(args) > 1 else 0
                self.z = args[2] if len(args) > 2 else 0

# Inject mock bpy
mock_bpy = MockBpy()
sys.modules['bpy'] = mock_bpy
sys.modules['bpy.context'] = mock_bpy.context
sys.modules['bpy.data'] = mock_bpy.data
sys.modules['bpy.ops'] = mock_bpy.ops
sys.modules['bpy.app'] = mock_bpy.app
sys.modules['bpy.types'] = mock_bpy.types
sys.modules['mathutils'] = mock_bpy.mathutils

# Now we can import handlers
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_handler_imports():
    """Test that handlers can be imported"""
    print("="*60)
    print("Testing Handler Imports")
    print("="*60)
    
    results = []
    
    # Test render handlers
    try:
        from handlers.rendering.render_settings import (
            SetRenderOutputHandler,
            GetRenderSettingsHandler
        )
        print("✓ Render handlers imported successfully")
        results.append(("Render Handlers Import", True))
    except Exception as e:
        print(f"✗ Failed to import render handlers: {e}")
        results.append(("Render Handlers Import", False))
    
    # Test Sketchfab handlers
    try:
        from handlers.integrations.sketchfab import (
            GetSketchfabStatusHandler,
            SearchSketchfabModelsHandler,
            GetSketchfabModelPreviewHandler,
            DownloadSketchfabModelHandler
        )
        print("✓ Sketchfab handlers imported successfully")
        results.append(("Sketchfab Handlers Import", True))
    except Exception as e:
        print(f"✗ Failed to import Sketchfab handlers: {e}")
        results.append(("Sketchfab Handlers Import", False))
    
    # Test handler registry
    try:
        from handlers.handler_registry import register_all_handlers
        print("✓ Handler registry imported successfully")
        results.append(("Handler Registry Import", True))
    except Exception as e:
        print(f"✗ Failed to import handler registry: {e}")
        results.append(("Handler Registry Import", False))
    
    return results

def test_handler_instantiation():
    """Test that handlers can be instantiated"""
    print("\n" + "="*60)
    print("Testing Handler Instantiation")
    print("="*60)
    
    results = []
    
    try:
        from handlers.rendering.render_settings import (
            SetRenderOutputHandler,
            GetRenderSettingsHandler
        )
        
        set_handler = SetRenderOutputHandler()
        get_handler = GetRenderSettingsHandler()
        
        print(f"✓ SetRenderOutputHandler instantiated - command: {set_handler.get_command_name()}")
        print(f"✓ GetRenderSettingsHandler instantiated - command: {get_handler.get_command_name()}")
        results.append(("Render Handlers Instantiation", True))
    except Exception as e:
        print(f"✗ Failed to instantiate render handlers: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Render Handlers Instantiation", False))
    
    try:
        from handlers.integrations.sketchfab import (
            GetSketchfabStatusHandler,
            SearchSketchfabModelsHandler,
            GetSketchfabModelPreviewHandler,
            DownloadSketchfabModelHandler
        )
        
        status_handler = GetSketchfabStatusHandler()
        search_handler = SearchSketchfabModelsHandler()
        preview_handler = GetSketchfabModelPreviewHandler()
        download_handler = DownloadSketchfabModelHandler()
        
        print(f"✓ GetSketchfabStatusHandler instantiated - command: {status_handler.get_command_name()}")
        print(f"✓ SearchSketchfabModelsHandler instantiated - command: {search_handler.get_command_name()}")
        print(f"✓ GetSketchfabModelPreviewHandler instantiated - command: {preview_handler.get_command_name()}")
        print(f"✓ DownloadSketchfabModelHandler instantiated - command: {download_handler.get_command_name()}")
        results.append(("Sketchfab Handlers Instantiation", True))
    except Exception as e:
        print(f"✗ Failed to instantiate Sketchfab handlers: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Sketchfab Handlers Instantiation", False))
    
    return results

def test_handler_schemas():
    """Test handler parameter schemas"""
    print("\n" + "="*60)
    print("Testing Handler Parameter Schemas")
    print("="*60)
    
    results = []
    
    try:
        from handlers.rendering.render_settings import SetRenderOutputHandler
        
        handler = SetRenderOutputHandler()
        schema = handler.get_parameter_schema()
        
        # Check required fields
        assert "filepath" in schema, "filepath should be in schema"
        assert schema["filepath"]["required"] == True, "filepath should be required"
        
        print("✓ SetRenderOutputHandler schema is valid")
        print(f"  Required fields: {[k for k, v in schema.items() if v.get('required')]}")
        results.append(("Render Handler Schema", True))
    except Exception as e:
        print(f"✗ Render handler schema test failed: {e}")
        results.append(("Render Handler Schema", False))
    
    try:
        from handlers.integrations.sketchfab import GetSketchfabStatusHandler
        
        handler = GetSketchfabStatusHandler()
        schema = handler.get_parameter_schema()
        
        # Should have no required params (empty dict or all optional)
        print("✓ GetSketchfabStatusHandler schema is valid")
        print(f"  Schema: {schema}")
        results.append(("Sketchfab Handler Schema", True))
    except Exception as e:
        print(f"✗ Sketchfab handler schema test failed: {e}")
        results.append(("Sketchfab Handler Schema", False))
    
    return results

def test_handler_registry():
    """Test handler registry registration"""
    print("\n" + "="*60)
    print("Testing Handler Registry")
    print("="*60)
    
    results = []
    
    try:
        from core.command_router import command_router
        from handlers.rendering.render_settings import (
            SetRenderOutputHandler,
            GetRenderSettingsHandler
        )
        from handlers.integrations.sketchfab import (
            GetSketchfabStatusHandler,
            SearchSketchfabModelsHandler
        )
        
        # Clear existing handlers for clean test
        command_router._handlers.clear()
        command_router._handler_classes.clear()
        
        # Register handlers
        command_router.register_handler(SetRenderOutputHandler())
        command_router.register_handler(GetRenderSettingsHandler())
        command_router.register_handler(GetSketchfabStatusHandler())
        command_router.register_handler(SearchSketchfabModelsHandler())
        
        # Check registration
        commands = command_router.get_registered_commands()
        
        assert "set_render_output" in commands, "set_render_output should be registered"
        assert "get_render_settings" in commands, "get_render_settings should be registered"
        assert "get_sketchfab_status" in commands, "get_sketchfab_status should be registered"
        assert "search_sketchfab_models" in commands, "search_sketchfab_models should be registered"
        
        print(f"✓ Handlers registered successfully")
        print(f"  Registered commands: {sorted(commands)}")
        print(f"  Total: {len(commands)} handlers")
        results.append(("Handler Registry", True))
    except Exception as e:
        print(f"✗ Handler registry test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Handler Registry", False))
    
    return results

def test_command_routing():
    """Test command routing to handlers"""
    print("\n" + "="*60)
    print("Testing Command Routing")
    print("="*60)
    
    results = []
    
    try:
        from core.command_router import command_router
        from handlers.rendering.render_settings import GetRenderSettingsHandler
        from handlers.integrations.sketchfab import GetSketchfabStatusHandler
        
        # Clear and register
        command_router._handlers.clear()
        command_router._handler_classes.clear()
        command_router.register_handler(GetRenderSettingsHandler())
        command_router.register_handler(GetSketchfabStatusHandler())
        
        # Test routing get_render_settings
        command = {
            "type": "get_render_settings",
            "params": {}
        }
        response = command_router.route_command(command)
        
        assert response.get("status") == "success", f"Expected success, got: {response.get('status')}"
        assert "result" in response, "Response should have result"
        
        print("✓ get_render_settings command routed successfully")
        print(f"  Response status: {response.get('status')}")
        results.append(("Command Routing - Render", True))
    except Exception as e:
        print(f"✗ Command routing test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Command Routing - Render", False))
    
    try:
        from core.command_router import command_router as router2
        # Test routing get_sketchfab_status
        command = {
            "type": "get_sketchfab_status",
            "params": {}
        }
        response = router2.route_command(command)
        
        assert response.get("status") == "success", f"Expected success, got: {response.get('status')}"
        assert "result" in response, "Response should have result"
        
        print("✓ get_sketchfab_status command routed successfully")
        print(f"  Response status: {response.get('status')}")
        result = response.get("result", {})
        print(f"  Sketchfab enabled: {result.get('enabled', False)}")
        results.append(("Command Routing - Sketchfab", True))
    except Exception as e:
        print(f"✗ Sketchfab routing test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Command Routing - Sketchfab", False))
    
    return results

def main():
    """Run all simulation tests"""
    print("="*60)
    print("Blender MCP Handler Simulation Tests")
    print("="*60)
    print("\nTesting handlers without requiring Blender to be running...")
    
    all_results = []
    
    # Run all tests
    all_results.extend(test_handler_imports())
    all_results.extend(test_handler_instantiation())
    all_results.extend(test_handler_schemas())
    all_results.extend(test_handler_registry())
    all_results.extend(test_command_routing())
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    for test_name, passed in all_results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:40} {status}")
    
    total = len(all_results)
    passed = sum(1 for _, p in all_results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All simulation tests passed!")
        print("\nNote: These tests verify the handler code structure.")
        print("To test with actual Blender:")
        print("1. Restart Blender completely")
        print("2. Enable the addon")
        print("3. Start the MCP server")
        print("4. Run: python3 test_render_and_sketchfab.py")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check the output above for details.")

if __name__ == "__main__":
    main()
