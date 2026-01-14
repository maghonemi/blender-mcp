# Animation System Specification

## Overview
This document specifies the complete animation system for Blender MCP, enabling full control over Blender's animation capabilities including keyframes, F-curves, timeline, constraints, and shape keys.

---

## 1. Keyframe Management

### 1.1 Create Keyframes
**Command**: `create_keyframe`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path": "location",
    "frame": 1,
    "value": [1.0, 2.0, 3.0],
    "interpolation": "BEZIER",
    "keyframe_type": "KEYFRAME"
}
```

**Supported Data Paths**:
- Location: `location`, `location.x`, `location.y`, `location.z`
- Rotation: `rotation_euler`, `rotation_quaternion`, `rotation_axis_angle`
- Scale: `scale`, `scale.x`, `scale.y`, `scale.z`
- Custom properties: `["custom_property_name"]`
- Material properties: `material_slots[0].material.node_tree.nodes["Principled BSDF"].inputs[0].default_value`
- Shape keys: `data.shape_keys.key_blocks["Key"].value`

**Interpolation Types**:
- `CONSTANT` - No interpolation
- `LINEAR` - Linear interpolation
- `BEZIER` - Bezier curve (default)
- `SINE` - Sine wave
- `QUAD` - Quadratic
- `CUBIC` - Cubic
- `QUART` - Quartic
- `QUINT` - Quintic
- `EXPO` - Exponential
- `CIRC` - Circular
- `BACK` - Back
- `BOUNCE` - Bounce
- `ELASTIC` - Elastic

**Keyframe Types**:
- `KEYFRAME` - Standard keyframe
- `BREAKDOWN` - Breakdown keyframe
- `MOVING_HOLD` - Moving hold
- `EXTREME` - Extreme keyframe
- `JITTER` - Jitter keyframe

**Response**:
```json
{
    "status": "success",
    "result": {
        "keyframe_created": true,
        "frame": 1,
        "value": [1.0, 2.0, 3.0],
        "fcurve": {
            "data_path": "location",
            "array_index": -1,
            "keyframe_count": 1
        }
    }
}
```

### 1.2 Delete Keyframes
**Command**: `delete_keyframe`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path": "location",
    "frame": 1,
    "frame_range": null  // Optional: [start, end] for range deletion
}
```

### 1.3 Get Keyframes
**Command**: `get_keyframes`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path": "location",
    "frame_range": [1, 100]  // Optional
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "keyframes": [
            {
                "frame": 1,
                "value": [1.0, 2.0, 3.0],
                "interpolation": "BEZIER",
                "handle_left": [0.5, 2.0],
                "handle_right": [1.5, 2.0]
            }
        ],
        "fcurve_info": {
            "data_path": "location",
            "array_index": -1,
            "extrapolation": "CONSTANT"
        }
    }
}
```

### 1.4 Batch Keyframe Operations
**Command**: `batch_keyframes`

**Parameters**:
```json
{
    "operations": [
        {
            "action": "create",
            "object_name": "Cube",
            "data_path": "location",
            "frame": 1,
            "value": [0, 0, 0]
        },
        {
            "action": "create",
            "object_name": "Cube",
            "data_path": "location",
            "frame": 50,
            "value": [5, 5, 5]
        }
    ]
}
```

---

## 2. Animation Curves (F-Curves)

### 2.1 Get F-Curves
**Command**: `get_fcurves`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path_filter": "location"  // Optional
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "fcurves": [
            {
                "data_path": "location",
                "array_index": 0,
                "keyframe_count": 10,
                "extrapolation": "CONSTANT",
                "modifiers": []
            }
        ]
    }
}
```

### 2.2 Modify F-Curve Interpolation
**Command**: `set_fcurve_interpolation`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path": "location",
    "array_index": 0,  // Optional, -1 for all
    "interpolation": "BEZIER",
    "keyframe_range": [1, 50]  // Optional
}
```

### 2.3 F-Curve Modifiers
**Command**: `add_fcurve_modifier`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path": "location",
    "array_index": 0,
    "modifier_type": "NOISE",
    "modifier_settings": {
        "strength": 0.5,
        "scale": 1.0,
        "phase": 0.0
    }
}
```

**Supported Modifiers**:
- `GENERATOR` - Generate values
- `FNGENERATOR` - Function generator
- `ENVELOPE` - Envelope
- `CYCLES` - Cycles
- `NOISE` - Noise
- `LIMITS` - Limits
- `STEPPED` - Stepped interpolation

### 2.4 Bake F-Curve
**Command**: `bake_fcurve`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path": "location",
    "array_index": 0,
    "frame_start": 1,
    "frame_end": 100,
    "step": 1
}
```

---

## 3. Timeline Control

### 3.1 Set Current Frame
**Command**: `set_current_frame`

**Parameters**:
```json
{
    "frame": 50
}
```

### 3.2 Get Timeline Info
**Command**: `get_timeline_info`

**Response**:
```json
{
    "status": "success",
    "result": {
        "current_frame": 50,
        "frame_start": 1,
        "frame_end": 250,
        "fps": 24,
        "playback_mode": "PLAYBACK"
    }
}
```

### 3.3 Set Frame Range
**Command**: `set_frame_range`

**Parameters**:
```json
{
    "frame_start": 1,
    "frame_end": 250
}
```

### 3.4 Playback Control
**Command**: `playback_control`

**Parameters**:
```json
{
    "action": "play|pause|stop|frame_next|frame_previous"
}
```

### 3.5 Timeline Markers
**Command**: `manage_markers`

**Parameters**:
```json
{
    "action": "create|delete|get",
    "marker_name": "Action Start",
    "frame": 10,
    "camera": "Camera"  // Optional
}
```

---

## 4. Animation Constraints

### 4.1 Add Constraint
**Command**: `add_constraint`

**Parameters**:
```json
{
    "object_name": "Cube",
    "constraint_type": "COPY_LOCATION",
    "constraint_name": "CopyLocation",
    "target": "TargetObject",
    "settings": {
        "use_x": true,
        "use_y": true,
        "use_z": false,
        "influence": 1.0
    }
}
```

**Supported Constraint Types**:
- `COPY_LOCATION` - Copy Location
- `COPY_ROTATION` - Copy Rotation
- `COPY_SCALE` - Copy Scale
- `COPY_TRANSFORMS` - Copy Transforms
- `LIMIT_LOCATION` - Limit Location
- `LIMIT_ROTATION` - Limit Rotation
- `LIMIT_SCALE` - Limit Scale
- `LIMIT_DISTANCE` - Limit Distance
- `MAINTAIN_VOLUME` - Maintain Volume
- `TRANSFORM` - Transform
- `CLAMP_TO` - Clamp To
- `DAMPED_TRACK` - Damped Track
- `LOCKED_TRACK` - Locked Track
- `TRACK_TO` - Track To
- `STRETCH_TO` - Stretch To
- `IK` - Inverse Kinematics
- `SPLINE_IK` - Spline IK
- `FOLLOW_PATH` - Follow Path
- `RIGID_BODY_JOINT` - Rigid Body Joint
- `CHILD_OF` - Child Of
- `PIVOT` - Pivot
- `FOLLOW_TRACK` - Follow Track
- `CAMERA_SOLVER` - Camera Solver
- `OBJECT_SOLVER` - Object Solver
- `ROTATION_DIFFERENCE` - Rotation Difference
- `TRANSFORM_CACHE` - Transform Cache
- `SHRINKWRAP` - Shrinkwrap
- `ACTION` - Action Constraint

### 4.2 Modify Constraint
**Command**: `modify_constraint`

**Parameters**:
```json
{
    "object_name": "Cube",
    "constraint_name": "CopyLocation",
    "settings": {
        "influence": 0.5
    }
}
```

### 4.3 Remove Constraint
**Command**: `remove_constraint`

**Parameters**:
```json
{
    "object_name": "Cube",
    "constraint_name": "CopyLocation"
}
```

### 4.4 Animate Constraint
**Command**: `animate_constraint`

**Parameters**:
```json
{
    "object_name": "Cube",
    "constraint_name": "CopyLocation",
    "property": "influence",
    "keyframes": [
        {"frame": 1, "value": 0.0},
        {"frame": 50, "value": 1.0}
    ]
}
```

---

## 5. Shape Keys

### 5.1 Create Shape Key
**Command**: `create_shape_key`

**Parameters**:
```json
{
    "object_name": "Cube",
    "shape_key_name": "Smile",
    "value": 0.0,
    "relative_to": "Basis"  // Optional
}
```

### 5.2 Set Shape Key Value
**Command**: `set_shape_key_value`

**Parameters**:
```json
{
    "object_name": "Cube",
    "shape_key_name": "Smile",
    "value": 1.0
}
```

### 5.3 Animate Shape Key
**Command**: `animate_shape_key`

**Parameters**:
```json
{
    "object_name": "Cube",
    "shape_key_name": "Smile",
    "keyframes": [
        {"frame": 1, "value": 0.0},
        {"frame": 25, "value": 1.0},
        {"frame": 50, "value": 0.0}
    ]
}
```

### 5.4 Get Shape Keys
**Command**: `get_shape_keys`

**Parameters**:
```json
{
    "object_name": "Cube"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "shape_keys": [
            {
                "name": "Basis",
                "value": 1.0,
                "keyframe_count": 0
            },
            {
                "name": "Smile",
                "value": 0.5,
                "keyframe_count": 3
            }
        ]
    }
}
```

---

## 6. Action Management

### 6.1 Create Action
**Command**: `create_action`

**Parameters**:
```json
{
    "action_name": "WalkCycle",
    "frame_range": [1, 24]
}
```

### 6.2 Assign Action
**Command**: `assign_action`

**Parameters**:
```json
{
    "object_name": "Armature",
    "action_name": "WalkCycle"
}
```

### 6.3 Get Action Info
**Command**: `get_action_info`

**Parameters**:
```json
{
    "action_name": "WalkCycle"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "name": "WalkCycle",
        "frame_range": [1, 24],
        "fcurve_count": 15,
        "users": 1
    }
}
```

### 6.4 Action Blending
**Command**: `blend_actions`

**Parameters**:
```json
{
    "object_name": "Armature",
    "action1": "WalkCycle",
    "action2": "RunCycle",
    "blend_factor": 0.5,
    "blend_mode": "REPLACE|ADD|MULTIPLY"
}
```

---

## 7. Animation Workflows

### 7.1 Create Animation from Path
**Command**: `animate_along_path`

**Parameters**:
```json
{
    "object_name": "Cube",
    "curve_name": "Path",
    "frame_start": 1,
    "frame_end": 100,
    "follow_path": true,
    "forward_axis": "FORWARD_X"
}
```

### 7.2 Create Bounce Animation
**Command**: `create_bounce_animation`

**Parameters**:
```json
{
    "object_name": "Ball",
    "start_location": [0, 0, 10],
    "end_location": [0, 0, 0],
    "bounces": 3,
    "frame_start": 1,
    "frame_end": 100
}
```

### 7.3 Create Rotation Animation
**Command**: `create_rotation_animation`

**Parameters**:
```json
{
    "object_name": "Wheel",
    "axis": "Z",
    "rotations": 2,
    "frame_start": 1,
    "frame_end": 100,
    "ease_in": true,
    "ease_out": true
}
```

---

## 8. Advanced Features

### 8.1 Drivers
**Command**: `create_driver`

**Parameters**:
```json
{
    "object_name": "Cube",
    "data_path": "location.x",
    "driver_type": "SCRIPTED",
    "expression": "frame / 10",
    "variables": [
        {
            "name": "frame",
            "type": "SINGLE_PROP",
            "target": "Scene",
            "data_path": "frame_current"
        }
    ]
}
```

### 8.2 Animation Baking
**Command**: `bake_animation`

**Parameters**:
```json
{
    "object_name": "Cube",
    "frame_start": 1,
    "frame_end": 100,
    "step": 1,
    "only_selected": false,
    "clear_constraints": false,
    "clear_parents": false
}
```

### 8.3 Animation Retargeting
**Command**: `retarget_animation`

**Parameters**:
```json
{
    "source_object": "SourceArmature",
    "target_object": "TargetArmature",
    "bone_mapping": {
        "UpperArm.L": "LeftArm",
        "UpperArm.R": "RightArm"
    }
}
```

---

## Error Handling

All animation commands should return standardized error responses:

```json
{
    "status": "error",
    "error_code": "INVALID_OBJECT|INVALID_DATA_PATH|INVALID_FRAME|...",
    "message": "Human-readable error message",
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2"
    ]
}
```

---

## Performance Considerations

1. **Batch Operations**: Support batch keyframe creation for efficiency
2. **Lazy Evaluation**: Only evaluate F-curves when needed
3. **Caching**: Cache F-curve data for frequently accessed objects
4. **Optimization**: Use Blender's built-in optimization tools

---

## Testing Requirements

1. Unit tests for each command type
2. Integration tests for complex workflows
3. Performance tests with large numbers of keyframes
4. Edge case testing (invalid frames, missing objects, etc.)
