# Modeling & Mesh Editing System Specification

## Overview
This document specifies the complete modeling and mesh editing system for Blender MCP, enabling full control over mesh operations, modifiers, geometry nodes, and UV mapping.

---

## 1. Mesh Creation

### 1.1 Create Primitive
**Command**: `create_primitive`

**Parameters**:
```json
{
    "type": "MESH_CUBE|MESH_SPHERE|MESH_CYLINDER|MESH_PLANE|MESH_TORUS|MESH_MONKEY",
    "name": "Cube",
    "location": [0, 0, 0],
    "scale": [1, 1, 1],
    "properties": {
        "radius": 1.0,  // For sphere/cylinder/torus
        "depth": 2.0,  // For cylinder
        "vertices": 32,  // For sphere/cylinder
        "size": [2, 2, 2]  // For cube
    }
}
```

### 1.2 Create from Vertices
**Command**: `create_mesh_from_vertices`

**Parameters**:
```json
{
    "name": "CustomMesh",
    "vertices": [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ],
    "edges": [
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0]
    ],
    "faces": [
        [0, 1, 2, 3]
    ]
}
```

---

## 2. Mesh Selection

### 2.1 Select Vertices
**Command**: `select_vertices`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "vertex_indices": [0, 1, 2, 3],
    "mode": "SET|ADD|SUBTRACT|TOGGLE",
    "deselect_all": false
}
```

### 2.2 Select Edges
**Command**: `select_edges`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "edge_indices": [0, 1, 2],
    "mode": "SET|ADD|SUBTRACT|TOGGLE",
    "select_mode": "VERT|EDGE|FACE"
}
```

### 2.3 Select Faces
**Command**: `select_faces`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "face_indices": [0, 1, 2],
    "mode": "SET|ADD|SUBTRACT|TOGGLE"
}
```

### 2.4 Select by Property
**Command**: `select_by_property`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "property": "NORMAL|MATERIAL|SHARP|SEAM|CREASE",
    "threshold": 0.5,
    "extend": false
}
```

### 2.5 Get Selection
**Command**: `get_selection`

**Parameters**:
```json
{
    "mesh_name": "Cube"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "selected_vertices": [0, 1, 2],
        "selected_edges": [0, 1],
        "selected_faces": [0]
    }
}
```

---

## 3. Mesh Editing Operations

### 3.1 Extrude
**Command**: `extrude_mesh`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "mode": "VERT|EDGE|FACE",
    "offset": [0, 0, 1],
    "use_individual": false,
    "use_normal_flip": false
}
```

### 3.2 Inset Faces
**Command**: `inset_faces`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "thickness": 0.1,
    "depth": 0.0,
    "use_outset": false,
    "use_relative_offset": true,
    "use_boundary": true,
    "use_even_offset": true
}
```

### 3.3 Bevel
**Command**: `bevel_mesh`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "mode": "VERT|EDGE",
    "amount": 0.1,
    "segments": 1,
    "profile": 0.5,
    "affect": "VERTICES|EDGES",
    "clamp_overlap": true,
    "loop_slide": true
}
```

### 3.4 Loop Cut
**Command**: `loop_cut`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "number_cuts": 1,
    "smoothness": 0.0,
    "falloff": "SMOOTH|SPHERE|ROOT|INVERSE_SQUARE|SHARP|LINEAR"
}
```

### 3.5 Subdivide
**Command**: `subdivide_mesh`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "number_cuts": 1,
    "smoothness": 0.0,
    "fractal": 0.0,
    "fractal_randomness": 1.0,
    "corner_type": "INNER_VERT|PATH|LINEAR|FAN"
}
```

### 3.6 Knife Cut
**Command**: `knife_cut`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "cut_path": [
        [0, 0, 0],
        [1, 1, 1]
    ],
    "use_occlude_geometry": true,
    "only_selected": false
}
```

### 3.7 Delete Elements
**Command**: `delete_mesh_elements`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "mode": "VERT|EDGE|FACE|ONLY_FACE|EDGE_FACE|ONLY_EDGE",
    "use_verts": false,
    "use_edges": false,
    "use_faces": true
}
```

### 3.8 Merge Vertices
**Command**: `merge_vertices`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "vertex_indices": [0, 1, 2],
    "type": "FIRST|LAST|CENTER|CURSOR|COLLAPSE|BY_DISTANCE",
    "distance": 0.0001
}
```

### 3.9 Separate
**Command**: `separate_mesh`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "type": "SELECTED|MATERIAL|LOOSE"
}
```

### 3.10 Join Meshes
**Command**: `join_meshes`

**Parameters**:
```json
{
    "mesh_names": ["Cube", "Sphere"],
    "target_name": "CombinedMesh"
}
```

---

## 4. Transform Operations

### 4.1 Transform Selection
**Command**: `transform_selection`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "translation": [1, 0, 0],
    "rotation": [0, 0, 0.5],
    "scale": [1, 1, 1],
    "mode": "GLOBAL|LOCAL|NORMAL|GIMBAL|VIEW"
}
```

### 4.2 Move Along Normal
**Command**: `move_along_normal`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "distance": 0.1,
    "mode": "VERT|EDGE|FACE"
}
```

### 4.3 Rotate Around Normal
**Command**: `rotate_around_normal`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "angle": 0.5,
    "mode": "VERT|EDGE|FACE"
}
```

### 4.4 Scale Along Normal
**Command**: `scale_along_normal`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "factor": 1.1,
    "mode": "VERT|EDGE|FACE"
}
```

---

## 5. Modifiers

### 5.1 Add Modifier
**Command**: `add_modifier`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_type": "SUBSURF|ARRAY|MIRROR|SOLIDIFY|BEVEL",
    "modifier_name": "Subdivision",
    "properties": {
        "levels": 2,
        "render_levels": 3,
        "subdivision_type": "CATMULL_CLARK|SIMPLE|LINEAR"
    }
}
```

**Common Modifier Types**:
- `SUBSURF` - Subdivision Surface
- `ARRAY` - Array
- `MIRROR` - Mirror
- `SOLIDIFY` - Solidify
- `BEVEL` - Bevel
- `BOOLEAN` - Boolean
- `SCREW` - Screw
- `SKIN` - Skin
- `WIREFRAME` - Wireframe
- `DECIMATE` - Decimate
- `MULTIRES` - Multiresolution
- `SMOOTH` - Smooth
- `CAST` - Cast
- `CURVE` - Curve
- `DISPLACE` - Displace
- `HOOK` - Hook
- `LAPLACIANSMOOTH` - Laplacian Smooth
- `LATTICE` - Lattice
- `MASK` - Mask
- `SHRINKWRAP` - Shrinkwrap
- `SIMPLE_DEFORM` - Simple Deform
- `SMOOTH_CORRECTIVE` - Smooth Corrective
- `SMOOTH_LAPLACIAN` - Smooth Laplacian
- `TRIANGULATE` - Triangulate
- `WELD` - Weld
- `WAVE` - Wave
- `CLOTH` - Cloth
- `COLLISION` - Collision
- `DYNAMIC_PAINT` - Dynamic Paint
- `EXPLODE` - Explode
- `FLUID` - Fluid
- `OCEAN` - Ocean
- `PARTICLE_INSTANCE` - Particle Instance
- `PARTICLE_SYSTEM` - Particle System
- `SMOKE` - Smoke
- `SOFT_BODY` - Soft Body

### 5.2 Modify Modifier
**Command**: `modify_modifier`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_name": "Subdivision",
    "properties": {
        "levels": 3
    }
}
```

### 5.3 Remove Modifier
**Command**: `remove_modifier`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_name": "Subdivision"
}
```

### 5.4 Apply Modifier
**Command**: `apply_modifier`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_name": "Subdivision",
    "apply_as": "DATA|SHAPE"
}
```

### 5.5 Get Modifiers
**Command**: `get_modifiers`

**Parameters**:
```json
{
    "mesh_name": "Cube"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "modifiers": [
            {
                "name": "Subdivision",
                "type": "SUBSURF",
                "show_viewport": true,
                "show_render": true,
                "show_in_editmode": false,
                "show_on_cage": false
            }
        ]
    }
}
```

---

## 6. Geometry Nodes

### 6.1 Add Geometry Nodes Modifier
**Command**: `add_geometry_nodes_modifier`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_name": "GeometryNodes",
    "node_group": "MyNodeGroup"  // Optional, creates new if not specified
}
```

### 6.2 Create Geometry Node Group
**Command**: `create_geometry_node_group`

**Parameters**:
```json
{
    "name": "MyNodeGroup",
    "nodes": [
        {
            "type": "GROUP_INPUT",
            "name": "GroupInput",
            "location": [0, 0]
        },
        {
            "type": "MESH_PRIMITIVE_CUBE",
            "name": "Cube",
            "location": [200, 0],
            "properties": {
                "size": [1, 1, 1]
            }
        }
    ],
    "links": [
        {
            "from": {"node": "GroupInput", "socket": "Geometry"},
            "to": {"node": "Cube", "socket": "Mesh"}
        }
    ]
}
```

### 6.3 Add Geometry Node
**Command**: `add_geometry_node`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_name": "GeometryNodes",
    "node_type": "MESH_PRIMITIVE_CUBE",
    "node_name": "Cube",
    "location": [0, 0]
}
```

**Common Node Types**:
- `GROUP_INPUT` - Group Input
- `GROUP_OUTPUT` - Group Output
- `MESH_PRIMITIVE_CUBE` - Cube
- `MESH_PRIMITIVE_SPHERE` - Sphere
- `MESH_PRIMITIVE_CYLINDER` - Cylinder
- `MESH_PRIMITIVE_PLANE` - Plane
- `MESH_PRIMITIVE_ICO_SPHERE` - Ico Sphere
- `MESH_PRIMITIVE_CONE` - Cone
- `MESH_PRIMITIVE_TORUS` - Torus
- `MESH_PRIMITIVE_GRID` - Grid
- `MESH_PRIMITIVE_CIRCLE` - Circle
- `MESH_PRIMITIVE_LINE` - Line
- `MESH_PRIMITIVE_UV_SPHERE` - UV Sphere
- `MESH_TO_POINTS` - Mesh to Points
- `MESH_TO_CURVE` - Mesh to Curve
- `MESH_TO_VOLUME` - Mesh to Volume
- `POINTS_TO_VERTICES` - Points to Vertices
- `POINTS_TO_VOLUME` - Points to Volume
- `CURVE_TO_MESH` - Curve to Mesh
- `CURVE_TO_POINTS` - Curve to Points
- `VOLUME_TO_MESH` - Volume to Mesh
- `INSTANCE_ON_POINTS` - Instance on Points
- `JOIN_GEOMETRY` - Join Geometry
- `MESH_BOOLEAN` - Mesh Boolean
- `MESH_SUBDIVIDE` - Mesh Subdivide
- `MESH_EXTRUDE` - Mesh Extrude
- `MESH_DELETE` - Mesh Delete
- `MESH_MERGE_BY_DISTANCE` - Merge by Distance
- `MESH_SEPARATE_COMPONENTS` - Separate Components
- `MESH_SEPARATE_GEOMETRY` - Separate Geometry
- `MESH_SPLIT_EDGES` - Split Edges
- `MESH_SUBDIVIDE` - Subdivide
- `MESH_TRIANGULATE` - Triangulate
- `MESH_TO_CURVE` - Mesh to Curve
- `MESH_TO_POINTS` - Mesh to Points
- `MESH_TO_VOLUME` - Mesh to Volume
- `TRANSFORM_GEOMETRY` - Transform Geometry
- `TRANSLATE_INSTANCES` - Translate Instances
- `ROTATE_INSTANCES` - Rotate Instances
- `SCALE_INSTANCES` - Scale Instances
- `TRANSFORM_INSTANCES` - Transform Instances
- `REALIZE_INSTANCES` - Realize Instances
- `ATTRIBUTE_COMBINE_XYZ` - Combine XYZ
- `ATTRIBUTE_SEPARATE_XYZ` - Separate XYZ
- `ATTRIBUTE_MATH` - Math
- `ATTRIBUTE_MIX` - Mix
- `ATTRIBUTE_VECTOR_MATH` - Vector Math
- `ATTRIBUTE_COLOR_RAMP` - Color Ramp
- `ATTRIBUTE_MAP_RANGE` - Map Range
- `ATTRIBUTE_CLAMP` - Clamp
- `ATTRIBUTE_COMPARE` - Compare
- `ATTRIBUTE_FILL` - Fill
- `ATTRIBUTE_RANDOMIZE` - Randomize
- `ATTRIBUTE_REPLACE` - Replace
- `ATTRIBUTE_SAMPLE_TEXTURE` - Sample Texture
- `ATTRIBUTE_TRANSFER` - Transfer
- `ATTRIBUTE_PROXIMITY` - Proximity
- `ATTRIBUTE_CAPTURE` - Capture
- `ATTRIBUTE_STATISTIC` - Statistic
- `ATTRIBUTE_DOMAIN_SIZE` - Domain Size
- `ATTRIBUTE_INDEX` - Index
- `ATTRIBUTE_NORMAL` - Normal
- `ATTRIBUTE_TANGENT` - Tangent
- `ATTRIBUTE_UV_MAP` - UV Map
- `ATTRIBUTE_VERTEX_COLOR` - Vertex Color
- `ATTRIBUTE_WEIGHT` - Weight
- `ATTRIBUTE_EDGE_ANGLE` - Edge Angle
- `ATTRIBUTE_FACE_AREA` - Face Area
- `ATTRIBUTE_FACE_IS_PLANAR` - Face is Planar
- `ATTRIBUTE_FACE_NEIGHBORS` - Face Neighbors
- `ATTRIBUTE_EDGE_NEIGHBORS` - Edge Neighbors
- `ATTRIBUTE_VERTEX_NEIGHBORS` - Vertex Neighbors
- `ATTRIBUTE_EDGE_LENGTH` - Edge Length
- `ATTRIBUTE_EDGE_VERTICES` - Edge Vertices
- `ATTRIBUTE_FACE_CORNERS` - Face Corners
- `ATTRIBUTE_FACE_SET_BOUNDARIES` - Face Set Boundaries
- `ATTRIBUTE_FACE_SET` - Face Set
- `ATTRIBUTE_MATERIAL_INDEX` - Material Index
- `ATTRIBUTE_SHADE_SMOOTH` - Shade Smooth
- `ATTRIBUTE_ISLAND` - Island
- `ATTRIBUTE_EDGE_ANGLE` - Edge Angle
- `ATTRIBUTE_FACE_AREA` - Face Area
- `ATTRIBUTE_FACE_IS_PLANAR` - Face is Planar
- `ATTRIBUTE_FACE_NEIGHBORS` - Face Neighbors
- `ATTRIBUTE_EDGE_NEIGHBORS` - Edge Neighbors
- `ATTRIBUTE_VERTEX_NEIGHBORS` - Vertex Neighbors
- `ATTRIBUTE_EDGE_LENGTH` - Edge Length
- `ATTRIBUTE_EDGE_VERTICES` - Edge Vertices
- `ATTRIBUTE_FACE_CORNERS` - Face Corners
- `ATTRIBUTE_FACE_SET_BOUNDARIES` - Face Set Boundaries
- `ATTRIBUTE_FACE_SET` - Face Set
- `ATTRIBUTE_MATERIAL_INDEX` - Material Index
- `ATTRIBUTE_SHADE_SMOOTH` - Shade Smooth
- `ATTRIBUTE_ISLAND` - Island

### 6.4 Connect Geometry Nodes
**Command**: `connect_geometry_nodes`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_name": "GeometryNodes",
    "from_node": "GroupInput",
    "from_socket": "Geometry",
    "to_node": "Cube",
    "to_socket": "Mesh"
}
```

### 6.5 Set Geometry Node Properties
**Command**: `set_geometry_node_properties`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "modifier_name": "GeometryNodes",
    "node_name": "Cube",
    "properties": {
        "size": [2, 2, 2]
    }
}
```

---

## 7. UV Mapping

### 7.1 Unwrap UV
**Command**: `unwrap_uv`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "method": "ANGLE_BASED|CONFORMAL|LIGHTMAP_PACK|SMART_PROJECT",
    "margin": 0.001,
    "use_seams": true,
    "use_sharp": false
}
```

### 7.2 Get UV Map
**Command**: `get_uv_map`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "uv_map_name": "UVMap"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "name": "UVMap",
        "vertices": [
            {
                "index": 0,
                "uv": [0.0, 0.0]
            }
        ],
        "faces": [
            {
                "index": 0,
                "uv_indices": [0, 1, 2, 3]
            }
        ]
    }
}
```

### 7.3 Set UV Coordinates
**Command**: `set_uv_coordinates`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "uv_map_name": "UVMap",
    "face_index": 0,
    "uv_coordinates": [
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0]
    ]
}
```

### 7.4 Pack UV Islands
**Command**: `pack_uv_islands`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "uv_map_name": "UVMap",
    "margin": 0.001,
    "rotate": true,
    "udim_source_closest": false
}
```

---

## 8. Mesh Analysis

### 8.1 Get Mesh Info
**Command**: `get_mesh_info`

**Parameters**:
```json
{
    "mesh_name": "Cube"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "vertices": 8,
        "edges": 12,
        "faces": 6,
        "loops": 24,
        "materials": 1,
        "uv_layers": 1,
        "vertex_colors": 0,
        "is_manifold": true,
        "has_ngons": false,
        "has_tris": false,
        "has_quads": true
    }
}
```

### 8.2 Analyze Topology
**Command**: `analyze_topology`

**Parameters**:
```json
{
    "mesh_name": "Cube"
}
```

**Response**:
```json
{
    "status": "success",
    "result": {
        "is_manifold": true,
        "is_closed": true,
        "has_boundary": false,
        "genus": 0,
        "euler_characteristic": 2,
        "connected_components": 1
    }
}
```

---

## 9. Mesh Cleanup

### 9.1 Remove Doubles
**Command**: `remove_doubles`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "distance": 0.0001,
    "use_unselected": false
}
```

### 9.2 Decimate Mesh
**Command**: `decimate_mesh`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "ratio": 0.5,
    "method": "COLLAPSE|UNSUBDIV|DISSOLVE"
}
```

### 9.3 Recalculate Normals
**Command**: `recalculate_normals`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "inside": false
}
```

### 9.4 Mark Sharp Edges
**Command**: `mark_sharp_edges`

**Parameters**:
```json
{
    "mesh_name": "Cube",
    "edge_indices": [0, 1, 2],
    "sharp": true
}
```

---

## Error Handling

All modeling commands return standardized error responses:

```json
{
    "status": "error",
    "error_code": "MESH_NOT_FOUND|INVALID_SELECTION|OPERATION_FAILED|...",
    "message": "Human-readable error message",
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2"
    ]
}
```

---

## Performance Considerations

1. **Batch Operations**: Support batch mesh operations
2. **Lazy Evaluation**: Only compute mesh data when needed
3. **Caching**: Cache mesh topology and geometry
4. **Optimization**: Use Blender's built-in optimization tools

---

## Testing Requirements

1. Unit tests for each command type
2. Integration tests for complex modeling workflows
3. Performance tests with large meshes (100k+ vertices)
4. Edge case testing (invalid selections, missing meshes, etc.)
