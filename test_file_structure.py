#!/usr/bin/env python3
"""
Simple test to verify file structure and handler registration
"""

import os
import ast
import re

def test_file_exists(filepath):
    """Test if file exists"""
    exists = os.path.exists(filepath)
    if exists:
        print(f"✓ {filepath}")
    else:
        print(f"✗ {filepath} - NOT FOUND")
    return exists

def test_handler_class_in_file(filepath, class_name):
    """Test if handler class exists in file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if f"class {class_name}" in content:
                print(f"  ✓ Class {class_name} found")
                return True
            else:
                print(f"  ✗ Class {class_name} NOT found")
                return False
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
        return False

def test_handler_registered(filepath, handler_class):
    """Test if handler is registered in handler_registry.py"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if handler_class in content:
                print(f"  ✓ {handler_class} registered")
                return True
            else:
                print(f"  ✗ {handler_class} NOT registered")
                return False
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
        return False

def main():
    print("="*60)
    print("Blender MCP Handler File Structure Test")
    print("="*60)
    
    results = []
    
    # Test render handlers
    print("\n1. Testing Render Handlers...")
    render_file = "handlers/rendering/render_settings.py"
    if test_file_exists(render_file):
        results.append(("Render Handler File", True))
        
        if test_handler_class_in_file(render_file, "SetRenderOutputHandler"):
            results.append(("SetRenderOutputHandler Class", True))
        else:
            results.append(("SetRenderOutputHandler Class", False))
        
        if test_handler_class_in_file(render_file, "GetRenderSettingsHandler"):
            results.append(("GetRenderSettingsHandler Class", True))
        else:
            results.append(("GetRenderSettingsHandler Class", False))
    else:
        results.append(("Render Handler File", False))
    
    # Test Sketchfab handlers
    print("\n2. Testing Sketchfab Handlers...")
    sketchfab_file = "handlers/integrations/sketchfab.py"
    if test_file_exists(sketchfab_file):
        results.append(("Sketchfab Handler File", True))
        
        handlers = [
            "GetSketchfabStatusHandler",
            "SearchSketchfabModelsHandler",
            "GetSketchfabModelPreviewHandler",
            "DownloadSketchfabModelHandler"
        ]
        
        for handler in handlers:
            if test_handler_class_in_file(sketchfab_file, handler):
                results.append((f"{handler} Class", True))
            else:
                results.append((f"{handler} Class", False))
    else:
        results.append(("Sketchfab Handler File", False))
    
    # Test handler registry
    print("\n3. Testing Handler Registry...")
    registry_file = "handlers/handler_registry.py"
    if test_file_exists(registry_file):
        results.append(("Handler Registry File", True))
        
        # Check if render handlers are imported
        if test_handler_registered(registry_file, "SetRenderOutputHandler"):
            results.append(("SetRenderOutputHandler Import", True))
        else:
            results.append(("SetRenderOutputHandler Import", False))
        
        if test_handler_registered(registry_file, "GetRenderSettingsHandler"):
            results.append(("GetRenderSettingsHandler Import", True))
        else:
            results.append(("GetRenderSettingsHandler Import", False))
        
        # Check if Sketchfab handlers are imported
        if test_handler_registered(registry_file, "GetSketchfabStatusHandler"):
            results.append(("GetSketchfabStatusHandler Import", True))
        else:
            results.append(("GetSketchfabStatusHandler Import", False))
        
        # Check if handlers are registered
        if "command_router.register_handler(SetRenderOutputHandler())" in open(registry_file).read():
            print("  ✓ SetRenderOutputHandler registered in registry")
            results.append(("SetRenderOutputHandler Registration", True))
        else:
            print("  ✗ SetRenderOutputHandler NOT registered")
            results.append(("SetRenderOutputHandler Registration", False))
        
        if "command_router.register_handler(GetSketchfabStatusHandler())" in open(registry_file).read():
            print("  ✓ GetSketchfabStatusHandler registered in registry")
            results.append(("GetSketchfabStatusHandler Registration", True))
        else:
            print("  ✗ GetSketchfabStatusHandler NOT registered")
            results.append(("GetSketchfabStatusHandler Registration", False))
    else:
        results.append(("Handler Registry File", False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:50} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All file structure tests passed!")
        print("\nThe handlers are properly implemented and registered.")
        print("To test with actual Blender:")
        print("1. Restart Blender completely")
        print("2. Enable the addon")
        print("3. Start the MCP server")
        print("4. Run: python3 test_render_and_sketchfab.py")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check the output above.")

if __name__ == "__main__":
    main()
