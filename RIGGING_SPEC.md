# Rigging & Armature System Specification

## Overview
This document specifies the complete rigging and armature system for Blender MCP, enabling full control over bone creation, manipulation, weight painting, and skinning.

---

## 1. Armature Creation & Management

### 1.1 Create Armature
**Command**: `create_armature`

**Parameters**:
```json
{
    "name": "Armature",
    "location": [0, 0, 0],
    "add_bones": false
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "armature_name": "Armature",
        "bone_count": 0,
        "mode": "EDIT"
    }
}
```

### 1.2 Get Armature Info
**Command**: `get_armature_info`

**Parameters**:
```json
{
    "armature_name": "Armature"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "name": "Armature",
        "bone_count": 15,
        "mode": "POSE",
        "bones": [
            {
                "name": "Bone",
                "parent": null,
                "head": [0, 0, 0],
                "tail": [0, 0, 1],
                "length": 1.0
            }
        ]
    }
}
```

---

## 2. Bone Operations

### 2.1 Create Bone
**Command**: `create_bone`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "UpperArm.L",
    "head": [0, 0, 0],
    "tail": [0, 1, 0],
    "parent": "Shoulder.L",
    "roll": 0.0,
    "length": null
}
```

### 2.2 Delete Bone
**Command**: `delete_bone`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "Bone",
    "delete_children": false
}
```

### 2.3 Get Bone Info
**Command**: `get_bone_info`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "UpperArm.L"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "name": "UpperArm.L",
        "parent": "Shoulder.L",
        "children": ["Forearm.L"],
        "head": [0, 0, 0],
        "tail": [0, 1, 0],
        "length": 1.0,
        "roll": 0.0,
        "matrix": [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]],
        "layers": [true, false, false, ...],
        "constraints": []
    }
}
```

### 2.4 Transform Bone
**Command**: `transform_bone`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "UpperArm.L",
    "mode": "EDIT|POSE",
    "translation": [1, 0, 0],
    "rotation": [0, 0, 0.5],
    "scale": [1, 1, 1],
    "head": [0, 0, 0],
    "tail": [0, 1, 0]
}
```

### 2.5 Set Bone Parent
**Command**: `set_bone_parent`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "Forearm.L",
    "parent_name": "UpperArm.L",
    "parent_type": "BONE",
    "use_connect": false,
    "use_local_location": false,
    "use_local_rotation": false
}
```

### 2.6 Bone Constraints
**Command**: `add_bone_constraint`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "Hand.L",
    "constraint_type": "IK",
    "constraint_name": "IK_Hand",
    "target": "TargetObject",
    "pole_target": "PoleObject",
    "chain_length": 2,
    "settings": {
        "influence": 1.0,
        "iterations": 500,
        "pole_angle": 0.0
    }
}
```

**Supported Constraint Types**:
- `IK` - Inverse Kinematics
- `SPLINE_IK` - Spline IK
- `COPY_TRANSFORMS` - Copy Transforms
- `LIMIT_ROTATION` - Limit Rotation
- `LIMIT_LOCATION` - Limit Location
- `LIMIT_SCALE` - Limit Scale
- `TRACK_TO` - Track To
- `STRETCH_TO` - Stretch To
- `DAMPED_TRACK` - Damped Track
- `LOCKED_TRACK` - Locked Track
- `ACTION` - Action Constraint

---

## 3. Bone Properties

### 3.1 Set Bone Properties
**Command**: `set_bone_properties`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "Bone",
    "properties": {
        "use_deform": true,
        "use_envelope_multiply": false,
        "envelope_distance": 0.1,
        "envelope_weight": 1.0,
        "head_radius": 0.1,
        "tail_radius": 0.1,
        "bbone_segments": 1,
        "bbone_in": 0.0,
        "bbone_out": 0.0
    }
}
```

### 3.2 Bone Layers
**Command**: `set_bone_layers`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "Bone",
    "layers": [true, false, false, true, ...]  // 32 layers
}
```

### 3.3 Bone Groups
**Command**: `manage_bone_groups`

**Parameters**:
```json
{
    "action": "create|add|remove|set",
    "armature_name": "Armature",
    "group_name": "LeftArm",
    "bone_names": ["UpperArm.L", "Forearm.L", "Hand.L"],
    "color_set": "THEME01"
}
```

---

## 4. Weight Painting

### 4.1 Get Vertex Weights
**Command**: `get_vertex_weights`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "vertex_group_name": "Bone",
    "vertex_indices": [0, 1, 2]  // Optional, all if not specified
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "vertex_group": "Bone",
        "weights": {
            "0": 1.0,
            "1": 0.8,
            "2": 0.5
        }
    }
}
```

### 4.2 Set Vertex Weights
**Command**: `set_vertex_weights`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "vertex_group_name": "Bone",
    "weights": {
        "0": 1.0,
        "1": 0.8,
        "2": 0.5
    },
    "add": false,
    "remove": false
}
```

### 4.3 Paint Weights
**Command**: `paint_weights`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "vertex_group_name": "Bone",
    "brush_settings": {
        "strength": 1.0,
        "radius": 0.1,
        "mode": "ADD|SUBTRACT|MULTIPLY|SMOOTH",
        "weight": 1.0
    },
    "vertices": [
        {"index": 0, "weight": 1.0},
        {"index": 1, "weight": 0.8}
    ]
}
```

### 4.4 Transfer Weights
**Command**: `transfer_weights`

**Parameters**:
```json
{
    "source_mesh": "SourceMesh",
    "target_mesh": "TargetMesh",
    "method": "NEAREST_FACE|NEAREST_VERTEX|NEAREST_VERTEX_IN_FACE",
    "max_distance": 0.1,
    "source_vertex_groups": ["Bone1", "Bone2"]
}
```

### 4.5 Normalize Weights
**Command**: `normalize_weights`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "vertex_group_name": "Bone",
    "mode": "ALL|ACTIVE|SELECTED",
    "lock_active": false
}
```

---

## 5. Skinning

### 5.1 Parent to Armature
**Command**: `parent_to_armature`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "armature_name": "Armature",
    "parent_type": "ARMATURE",
    "use_automatic_weight": true,
    "use_deform_preserve_volume": false
}
```

### 5.2 Automatic Weight Assignment
**Command**: `auto_weight_assign`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "armature_name": "Armature",
    "method": "HEAT|ENVELOPE",
    "remove_unused_vertex_groups": true
}
```

**Methods**:
- `HEAT` - Heat-based weighting (more accurate)
- `ENVELOPE` - Envelope-based weighting (faster)

### 5.3 Manual Weight Assignment
**Command**: `assign_weights_manual`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "bone_name": "Bone",
    "vertex_indices": [0, 1, 2, 3],
    "weight": 1.0
}
```

### 5.4 Clear Weights
**Command**: `clear_weights`

**Parameters**:
```json
{
    "mesh_name": "Character",
    "vertex_group_name": "Bone",
    "mode": "ALL|SELECTED|ACTIVE"
}
```

---

## 6. Pose Mode Operations

### 6.1 Set Bone Pose
**Command**: `set_bone_pose`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "UpperArm.L",
    "location": [0, 0, 0],
    "rotation": [0, 0, 0.5],
    "scale": [1, 1, 1],
    "rotation_mode": "XYZ"
}
```

### 6.2 Get Bone Pose
**Command**: `get_bone_pose`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "UpperArm.L"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "location": [0, 0, 0],
        "rotation": [0, 0, 0.5],
        "scale": [1, 1, 1],
        "matrix": [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
    }
}
```

### 6.3 Clear Pose
**Command**: `clear_pose`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_names": ["UpperArm.L", "Forearm.L"],  // Optional, all if not specified
    "clear_location": true,
    "clear_rotation": true,
    "clear_scale": true
}
```

### 6.4 Apply Pose as Rest
**Command**: `apply_pose_as_rest`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_names": ["UpperArm.L"]  // Optional
}
```

---

## 7. Bone Selection & Multi-Edit

### 7.1 Select Bones
**Command**: `select_bones`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_names": ["UpperArm.L", "Forearm.L"],
    "mode": "SET|ADD|SUBTRACT|TOGGLE",
    "deselect_all": false
}
```

### 7.2 Get Selected Bones
**Command**: `get_selected_bones`

**Parameters**:
```json
{
    "armature_name": "Armature"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "selected_bones": ["UpperArm.L", "Forearm.L"]
    }
}
```

---

## 8. Advanced Rigging Features

### 8.1 Create Control Rig
**Command**: `create_control_rig`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "UpperArm.L",
    "control_type": "IK_FK_SWITCH|TWIST|STRETCH",
    "settings": {
        "ik_chain_length": 2,
        "pole_target": "Pole.L"
    }
}
```

### 8.2 Bone Drivers
**Command**: `add_bone_driver`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "UpperArm.L",
    "data_path": "rotation_euler.x",
    "driver_type": "SCRIPTED",
    "expression": "UpperArm.L.rotation_euler.y * 0.5",
    "variables": [
        {
            "name": "UpperArm.L",
            "type": "TRANSFORMS",
            "target": "Armature",
            "bone_target": "UpperArm.L",
            "transform_type": "ROT_Y"
        }
    ]
}
```

### 8.3 Bone Shape Customization
**Command**: `set_bone_shape`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_name": "Bone",
    "shape_type": "SPHERE|CUBE|ARROW|...",
    "custom_object": "CustomShape",  // Optional
    "scale": [1, 1, 1],
    "color": [1, 0, 0, 1]
}
```

---

## 9. Rigging Workflows

### 9.1 Create Humanoid Rig
**Command**: `create_humanoid_rig`

**Parameters**:
```json
{
    "armature_name": "HumanoidRig",
    "scale": 1.0,
    "features": {
        "spine_count": 5,
        "finger_count": 5,
        "toe_count": 5,
        "ik_legs": true,
        "ik_arms": true
    }
}
```

### 9.2 Mirror Bones
**Command**: `mirror_bones`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "bone_names": ["UpperArm.L"],
    "axis": "X",
    "flip_names": true
}
```

### 9.3 Rename Bones
**Command**: `rename_bones`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "rename_map": {
        "Bone.L": "LeftBone",
        "Bone.R": "RightBone"
    },
    "find_replace": {
        "find": ".L",
        "replace": "_Left"
    }
}
```

---

## 10. Rig Export/Import

### 10.1 Export Rig
**Command**: `export_rig`

**Parameters**:
```json
{
    "armature_name": "Armature",
    "filepath": "/path/to/rig.blend",
    "include_meshes": false,
    "include_actions": true
}
```

### 10.2 Import Rig
**Command**: `import_rig`

**Parameters**:
```json
{
    "filepath": "/path/to/rig.blend",
    "armature_name": "Armature",
    "link": false
}
```

---

## Error Handling

All rigging commands return standardized error responses:

```json
{
    "status": "error",
    "error_code": "ARMATURE_NOT_FOUND|BONE_NOT_FOUND|INVALID_MODE|...",
    "message": "Human-readable error message",
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2"
    ]
}
```

---

## Performance Considerations

1. **Batch Operations**: Support batch bone creation/editing
2. **Lazy Evaluation**: Only compute bone matrices when needed
3. **Caching**: Cache bone hierarchy and transforms
4. **Optimization**: Use Blender's built-in optimization tools

---

## Testing Requirements

1. Unit tests for each command type
2. Integration tests for complex rigging workflows
3. Performance tests with large armatures (100+ bones)
4. Edge case testing (invalid bones, missing armatures, etc.)
