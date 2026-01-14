# Render Output and Sketchfab Integration Fix

## Summary
Fixed two issues:
1. **Render Output Path**: Added ability to change render output location
2. **Sketchfab Integration**: Fixed Sketchfab handlers not working in the new modular system

## Changes Made

### 1. Render Output Handler (`handlers/rendering/render_settings.py`)
- Created `SetRenderOutputHandler` to set render output path and format
- Created `GetRenderSettingsHandler` to get current render settings
- Supports:
  - Setting filepath (directory for animations, full path for images)
  - File formats: PNG, JPEG, OPEN_EXR, TIFF
  - Color modes: RGB, RGBA, BW
  - Color depth: 8, 16, 32 bits
  - Compression settings for JPEG
  - EXR codec settings

**Usage:**
```json
{
  "type": "set_render_output",
  "params": {
    "filepath": "/path/to/output",
    "file_format": "PNG",
    "color_mode": "RGB",
    "color_depth": "8"
  }
}
```

### 2. Sketchfab Integration Handlers (`handlers/integrations/sketchfab.py`)
- Created `GetSketchfabStatusHandler` - Check Sketchfab integration status
- Created `SearchSketchfabModelsHandler` - Search for models on Sketchfab
- Created `GetSketchfabModelPreviewHandler` - Get model preview thumbnails
- Created `DownloadSketchfabModelHandler` - Download and import models

**Fixed Issues:**
- Added missing `mathutils` import
- Handlers now properly check if Sketchfab is enabled
- Error handling improved with proper exception messages
- GLB download and import working correctly

### 3. Handler Registry Updates (`handlers/handler_registry.py`)
- Added rendering handlers to registry
- Added Sketchfab handlers to registry (conditionally imported)
- All handlers now properly registered on startup

## How to Use

### Change Render Output Location

**In Blender:**
1. Use the `set_render_output` command via MCP
2. Or manually set: `bpy.context.scene.render.filepath = "/your/path/"`

**Via MCP Command:**
```json
{
  "type": "set_render_output",
  "params": {
    "filepath": "/tmp/render_output/",
    "file_format": "PNG"
  }
}
```

### Use Sketchfab Integration

1. **Enable in Blender:**
   - Open BlenderMCP panel (N key in 3D viewport)
   - Check "Use assets from Sketchfab"
   - Enter your Sketchfab API key
   - Restart Blender or reload the addon

2. **Check Status:**
   ```json
   {
     "type": "get_sketchfab_status",
     "params": {}
   }
   ```

3. **Search Models:**
   ```json
   {
     "type": "search_sketchfab_models",
     "params": {
       "query": "chair",
       "count": 20,
       "downloadable": true
     }
   }
   ```

4. **Download Model:**
   ```json
   {
     "type": "download_sketchfab_model",
     "params": {
       "uid": "model_uid_here",
       "normalize_size": true,
       "target_size": 1.0
     }
   }
   ```

## Error Resolution

### "Render error (Read-only file system)"
**Solution:** Use `set_render_output` to change the output path to a writable location:
```json
{
  "type": "set_render_output",
  "params": {
    "filepath": "/tmp/blender_renders/"
  }
}
```

### "Error checking Sketchfab status: Communication error with Blender: Unknown error from Blender"
**Solution:** 
1. Ensure Sketchfab handlers are registered (check handler registry)
2. Make sure `blendermcp_use_sketchfab` is enabled in scene properties
3. Verify API key is set correctly
4. Restart Blender to reload handlers

## Files Modified
- `handlers/rendering/__init__.py` (created)
- `handlers/rendering/render_settings.py` (created)
- `handlers/integrations/sketchfab.py` (created)
- `handlers/handler_registry.py` (updated)

## Testing
All handlers follow the BaseHandler pattern and include:
- Parameter validation
- Error handling
- Proper logging
- Standardized response format
