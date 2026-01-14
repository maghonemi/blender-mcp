# Rendering & Compositing System Specification

## Overview
This document specifies the complete rendering and compositing system for Blender MCP, enabling full control over render settings, cameras, lighting, and post-processing.

---

## 1. Render Settings

### 1.1 Set Render Engine
**Command**: `set_render_engine`

**Parameters**:
```json
{
    "engine": "CYCLES|EEVEE|WORKBENCH",
    "scene": "Scene"  // Optional
}
```

**Engines**:
- `CYCLES` - Path-traced renderer
- `EEVEE` - Real-time renderer
- `WORKBENCH` - Fast preview renderer

### 1.2 Set Render Resolution
**Command**: `set_render_resolution`

**Parameters**:
```json
{
    "resolution_x": 1920,
    "resolution_y": 1080,
    "resolution_percentage": 100,
    "aspect_ratio": null  // Optional: "16:9", "4:3", etc.
}
```

### 1.3 Set Render Output
**Command**: `set_render_output`

**Parameters**:
```json
{
    "filepath": "/path/to/output",
    "file_format": "PNG|JPEG|OPEN_EXR|TIFF",
    "color_mode": "RGB|RGBA|BW",
    "color_depth": "8|16|32",
    "compression": 15,  // For JPEG
    "exr_codec": "ZIP"  // For EXR
}
```

### 1.4 Set Render Samples
**Command**: `set_render_samples`

**Parameters**:
```json
{
    "engine": "CYCLES",
    "samples": 128,
    "use_denoising": true,
    "denoiser": "OPENIMAGEDENOISE|OPTIX"
}
```

### 1.5 Get Render Settings
**Command**: `get_render_settings`

**Response**:
```json
{
    "status": "success",
    "result": {
        "engine": "CYCLES",
        "resolution": [1920, 1080],
        "samples": 128,
        "file_format": "PNG",
        "output_path": "/path/to/output"
    }
}
```

---

## 2. Camera Control

### 2.1 Create Camera
**Command**: `create_camera`

**Parameters**:
```json
{
    "name": "Camera",
    "location": [0, -10, 5],
    "rotation": [1.1, 0, 0],
    "type": "PERSP|ORTHO|PANO",
    "lens": 50.0,
    "sensor_width": 36.0
}
```

**Camera Types**:
- `PERSP` - Perspective
- `ORTHO` - Orthographic
- `PANO` - Panoramic

### 2.2 Set Active Camera
**Command**: `set_active_camera`

**Parameters**:
```json
{
    "camera_name": "Camera"
}
```

### 2.3 Set Camera Properties
**Command**: `set_camera_properties`

**Parameters**:
```json
{
    "camera_name": "Camera",
    "properties": {
        "type": "PERSP",
        "lens": 50.0,
        "sensor_width": 36.0,
        "sensor_height": 24.0,
        "shift_x": 0.0,
        "shift_y": 0.0,
        "clip_start": 0.1,
        "clip_end": 1000.0,
        "dof_distance": 10.0,
        "dof_object": null
    }
}
```

### 2.4 Camera Constraints
**Command**: `add_camera_constraint`

**Parameters**:
```json
{
    "camera_name": "Camera",
    "constraint_type": "TRACK_TO|FOLLOW_PATH|COPY_LOCATION",
    "target": "TargetObject",
    "settings": {
        "track_axis": "TRACK_NEGATIVE_Z",
        "up_axis": "UP_Y"
    }
}
```

### 2.5 Frame Camera to Selection
**Command**: `frame_camera_to_selection`

**Parameters**:
```json
{
    "camera_name": "Camera",
    "object_names": ["Cube", "Sphere"],
    "padding": 0.1
}
```

### 2.6 Set Camera View
**Command**: `set_camera_view`

**Parameters**:
```json
{
    "camera_name": "Camera",
    "view_type": "PERSP|ORTHO|CAMERA"
}
```

---

## 3. Lighting

### 3.1 Create Light
**Command**: `create_light`

**Parameters**:
```json
{
    "name": "Light",
    "type": "SUN|AREA|POINT|SPOT",
    "location": [5, 5, 10],
    "rotation": [0.785, 0, 0],
    "energy": 10.0,
    "color": [1, 1, 1]
}
```

**Light Types**:
- `SUN` - Sun light
- `AREA` - Area light
- `POINT` - Point light
- `SPOT` - Spot light

### 3.2 Set Light Properties
**Command**: `set_light_properties`

**Parameters**:
```json
{
    "light_name": "Light",
    "properties": {
        "type": "AREA",
        "energy": 10.0,
        "color": [1, 1, 1],
        "size": 1.0,  // For AREA
        "size_x": 1.0,  // For AREA
        "size_y": 1.0,  // For AREA
        "spot_size": 0.785,  // For SPOT
        "spot_blend": 0.15,  // For SPOT
        "use_shadow": true,
        "shadow_soft_size": 0.25
    }
}
```

### 3.3 Create Three-Point Lighting
**Command**: `create_three_point_lighting`

**Parameters**:
```json
{
    "target_object": "Cube",
    "key_light": {
        "energy": 10.0,
        "location": [5, -5, 5]
    },
    "fill_light": {
        "energy": 5.0,
        "location": [-3, -3, 2]
    },
    "rim_light": {
        "energy": 8.0,
        "location": [-5, 5, 3]
    }
}
```

### 3.4 Set World Lighting
**Command**: `set_world_lighting`

**Parameters**:
```json
{
    "world_name": "World",
    "type": "HDRI|SUN_SKY|COLOR",
    "hdri_path": "/path/to/hdri.hdr",  // For HDRI
    "sun_rotation": [0.785, 0, 0],  // For SUN_SKY
    "color": [0.5, 0.5, 0.5],  // For COLOR
    "strength": 1.0
}
```

---

## 4. Render Operations

### 4.1 Render Image
**Command**: `render_image`

**Parameters**:
```json
{
    "filepath": "/path/to/output.png",
    "scene": "Scene",  // Optional
    "camera": "Camera",  // Optional
    "frame": null,  // Optional, current frame if null
    "use_viewport": false
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "filepath": "/path/to/output.png",
        "width": 1920,
        "height": 1080,
        "render_time": 45.2
    }
}
```

### 4.2 Render Animation
**Command**: `render_animation`

**Parameters**:
```json
{
    "filepath": "/path/to/output",
    "frame_start": 1,
    "frame_end": 250,
    "frame_step": 1,
    "scene": "Scene",
    "use_placeholder": true
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "frames_rendered": 250,
        "total_time": 11250.5,
        "output_directory": "/path/to/output"
    }
}
```

### 4.3 Render Region
**Command**: `render_region`

**Parameters**:
```json
{
    "filepath": "/path/to/output.png",
    "region": {
        "x_min": 100,
        "y_min": 100,
        "x_max": 500,
        "y_max": 500
    }
}
```

### 4.4 Cancel Render
**Command**: `cancel_render`

**Parameters**:
```json
{}
```

---

## 5. Render Passes

### 5.1 Enable Render Passes
**Command**: `enable_render_passes`

**Parameters**:
```json
{
    "engine": "CYCLES",
    "passes": [
        "COMBINED",
        "DIFFUSE_DIRECT",
        "DIFFUSE_INDIRECT",
        "GLOSSY_DIRECT",
        "GLOSSY_INDIRECT",
        "TRANSMISSION",
        "EMISSION",
        "ENVIRONMENT",
        "SHADOW",
        "AO",
        "NORMAL",
        "UV",
        "MIST",
        "EMIT",
        "ENVIRONMENT",
        "DIFFUSE_COLOR",
        "GLOSSY_COLOR"
    ]
}
```

### 5.2 Get Render Passes
**Command**: `get_render_passes`

**Response**:
```json
{
    "status": "success",
    "result": {
        "enabled_passes": ["COMBINED", "DIFFUSE_DIRECT"],
        "available_passes": ["COMBINED", "DIFFUSE_DIRECT", ...]
    }
}
```

---

## 6. Compositing

### 6.1 Enable Compositing
**Command**: `enable_compositing`

**Parameters**:
```json
{
    "use_nodes": true,
    "scene": "Scene"
}
```

### 6.2 Create Compositor Node
**Command**: `create_compositor_node`

**Parameters**:
```json
{
    "node_type": "COMPOSITE|RENDER_LAYERS|BLUR|COLORBALANCE",
    "location": [0, 0],
    "name": "Node"
}
```

**Common Node Types**:
- `COMPOSITE` - Output node
- `RENDER_LAYERS` - Render layers input
- `BLUR` - Blur effect
- `COLORBALANCE` - Color correction
- `GLARE` - Glare effect
- `DEFOCUS` - Depth of field
- `DENOISE` - Denoising
- `FILTER` - Filter effects
- `MIX` - Mix nodes
- `ALPHAOVER` - Alpha over
- `TRANSLATE` - Transform
- `SCALE` - Scale
- `ROTATE` - Rotate
- `CROP` - Crop
- `FLIP` - Flip
- `MASK` - Mask
- `KEYING` - Keying
- `COLORCORRECTION` - Color correction

### 6.3 Connect Compositor Nodes
**Command**: `connect_compositor_nodes`

**Parameters**:
```json
{
    "from_node": "RenderLayers",
    "from_socket": "Image",
    "to_node": "Blur",
    "to_socket": "Image"
}
```

### 6.4 Set Compositor Node Properties
**Command**: `set_compositor_node_properties`

**Parameters**:
```json
{
    "node_name": "Blur",
    "properties": {
        "size_x": 5,
        "size_y": 5,
        "filter_type": "FLAT|TENT|QUAD|CUBIC|GAUSS"
    }
}
```

### 6.5 Get Compositor Node Tree
**Command**: `get_compositor_node_tree`

**Response**:
```json
{
    "status": "success",
    "result": {
        "nodes": [
            {
                "name": "RenderLayers",
                "type": "RENDER_LAYERS",
                "location": [0, 0],
                "inputs": ["Image", "Alpha", "Z"],
                "outputs": ["Image", "Alpha", "Z"]
            }
        ],
        "links": [
            {
                "from": {"node": "RenderLayers", "socket": "Image"},
                "to": {"node": "Blur", "socket": "Image"}
            }
        ]
    }
}
```

---

## 7. Render Layers

### 7.1 Create Render Layer
**Command**: `create_render_layer`

**Parameters**:
```json
{
    "name": "Background",
    "collections": ["BackgroundCollection"],
    "exclude_collections": ["ForegroundCollection"],
    "light_override": null,
    "material_override": null
}
```

### 7.2 Set Render Layer Properties
**Command**: `set_render_layer_properties`

**Parameters**:
```json
{
    "layer_name": "Background",
    "properties": {
        "use_solid": true,
        "use_halo": false,
        "use_strand": true,
        "use_freestyle": false,
        "samples": 128
    }
}
```

---

## 8. Post-Processing

### 8.1 Apply Color Correction
**Command**: `apply_color_correction`

**Parameters**:
```json
{
    "brightness": 1.0,
    "contrast": 1.0,
    "saturation": 1.0,
    "exposure": 0.0,
    "gamma": 1.0
}
```

### 8.2 Apply Blur
**Command**: `apply_blur`

**Parameters**:
```json
{
    "amount": 1.0,
    "type": "GAUSSIAN|BOX|FAST_GAUSSIAN"
}
```

### 8.3 Apply Glow
**Command**: `apply_glow`

**Parameters**:
```json
{
    "threshold": 0.8,
    "clamp": 1.0,
    "boost_factor": 1.0,
    "blend_factor": 0.5
}
```

---

## 9. Render Optimization

### 9.1 Set Performance Settings
**Command**: `set_performance_settings`

**Parameters**:
```json
{
    "engine": "CYCLES",
    "settings": {
        "use_adaptive_sampling": true,
        "adaptive_threshold": 0.01,
        "use_denoising": true,
        "tile_size": [256, 256],
        "threads": 0,  // 0 = auto
        "use_persistent_data": true
    }
}
```

### 9.2 Set Memory Settings
**Command**: `set_memory_settings`

**Parameters**:
```json
{
    "engine": "CYCLES",
    "settings": {
        "max_bounces": 12,
        "min_bounces": 3,
        "caustics_reflective": true,
        "caustics_refractive": true,
        "light_tree": true
    }
}
```

---

## 10. Render Queue

### 10.1 Add to Render Queue
**Command**: `add_to_render_queue`

**Parameters**:
```json
{
    "scene": "Scene",
    "frame_start": 1,
    "frame_end": 250,
    "filepath": "/path/to/output"
}
```

### 10.2 Get Render Queue
**Command**: `get_render_queue`

**Response**:
```json
{
    "status": "success",
    "result": {
        "queue": [
            {
                "scene": "Scene",
                "frame_start": 1,
                "frame_end": 250,
                "status": "PENDING|RENDERING|COMPLETE|FAILED"
            }
        ]
    }
}
```

### 10.3 Clear Render Queue
**Command**: `clear_render_queue`

**Parameters**:
```json
{
    "status_filter": "PENDING|RENDERING|COMPLETE|FAILED|ALL"
}
```

---

## Error Handling

All rendering commands return standardized error responses:

```json
{
    "status": "error",
    "error_code": "RENDER_FAILED|INVALID_CAMERA|INVALID_ENGINE|...",
    "message": "Human-readable error message",
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2"
    ]
}
```

---

## Performance Considerations

1. **Progressive Rendering**: Support progressive rendering for preview
2. **Render Caching**: Cache render results when possible
3. **Batch Rendering**: Optimize batch render operations
4. **GPU Acceleration**: Utilize GPU when available

---

## Testing Requirements

1. Unit tests for each command type
2. Integration tests for complete render workflows
3. Performance tests with various scene complexities
4. Edge case testing (invalid settings, missing files, etc.)
