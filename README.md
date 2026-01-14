# BlenderMCP - Blender Model Context Protocol Integration

BlenderMCP connects Blender to AI assistants (Claude, Cursor, VS Code) through the Model Context Protocol (MCP), enabling AI-powered 3D modeling, animation, rigging, rendering, and scene creation. This integration allows you to control Blender through natural language commands and automate complex workflows.

**We have no official website. Any website you see online is unofficial and has no affiliation with this project. Use them at your own risk.**

## Credits

This project is based on the original work by [Siddharth Ahuja](https://github.com/ahujasid). The project has been significantly expanded with comprehensive animation, rigging, rendering, camera, lighting, and modeling capabilities. Special thanks to the original creator for establishing the foundation of this powerful Blender-MCP integration.

### Original Project
- **Creator**: Siddharth Ahuja
- **Original Repository**: [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)
- **License**: See LICENSE file

### Community & Support
- **Discord**: [Join the Community](https://discord.gg/z5apgR8TFU)
- **Tutorial Video**: [Full Tutorial](https://www.youtube.com/watch?v=lCyQ717DuzQ)
- **Supporters**: [CodeRabbit](https://www.coderabbit.ai/), [Satish Goda](https://github.com/satishgoda)
- [Support this project](https://github.com/sponsors/ahujasid)

---

## Features

### 🎬 Complete Animation System
- **Keyframe Management**: Create, delete, and query keyframes with full interpolation control
- **Timeline Control**: Frame range, playback, and timeline navigation
- **F-Curves**: Advanced curve editing, interpolation, and modifiers
- **Actions**: Create, assign, duplicate, and manage animation actions
- **Shape Keys**: Create and animate shape keys for morphing
- **Constraints**: Add and manage object constraints
- **Baking**: Bake animations, clean keyframes, and sample curves

### 🦴 Advanced Rigging System
- **Armatures**: Create and manage armature objects
- **Bones**: Full bone creation, transformation, parenting, and hierarchy management
- **Weight Painting**: Vertex group creation, weight assignment, normalization, and transfer
- **Pose Mode**: Set, get, clear, and copy bone poses
- **Bone Constraints**: IK chains, constraints, and advanced rigging features
- **Rig Templates**: Humanoid rigs, simple rigs, and bone mirroring
- **Auto-Rigging**: Automatic hand and body rigging with intelligent bone placement
- **Skinning**: Automatic weight assignment and mesh-to-armature parenting

### 🎥 Rendering & Production
- **Render Engines**: Cycles, Eevee, and Workbench support
- **Render Settings**: Resolution, samples, output formats, and quality controls
- **Camera Control**: Create cameras, set properties, depth of field, and constraints
- **Lighting**: Create lights, three-point lighting setups, and world lighting
- **Render Operations**: Render images and animations with progress tracking

### 🎨 Modeling & Mesh Editing
- **Primitives**: Create cubes, spheres, cylinders, planes, torus, and more
- **Mesh Operations**: Extrude, transform, and edit mesh geometry
- **Project Setup**: Automated project configuration with collections and settings

### 🔍 Scene Management
- **Scene Inspection**: Get detailed information about objects, materials, and scene state
- **Object Operations**: Query object properties, get viewport screenshots
- **Code Execution**: Run arbitrary Python code in Blender with full error reporting
- **Project Setup**: One-command project configuration for video production

### 🌐 Integrations
- **Poly Haven**: Search and download models, textures, and HDRIs
- **Sketchfab**: Search and download 3D models
- **Hyper3D Rodin**: Generate 3D models using AI
- **Hunyuan3D**: AI-powered 3D model generation

---

## Installation

### Prerequisites

- **Blender 3.0 or newer**
- **Python 3.10 or newer**
- **uv package manager** (required for MCP server)

#### Installing uv

**macOS:**
```bash
brew install uv
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then add uv to your user path:
```powershell
$localBin = "$env:USERPROFILE\.local\bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;$localBin", "User")
```

**Linux/Other:**
See [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)

⚠️ **Do not proceed before installing uv**

### Step 1: Install Blender Addon

#### Quick Install (Recommended for macOS/Linux)

```bash
cd blender-mcp-main
./setup_blender_addon.sh
```

This script will:
- Find your Blender installation automatically
- Create the proper directory structure
- Copy all necessary files
- Set up the addon correctly

#### Manual Installation

1. **Download the addon files** from this repository
2. **Open Blender**
3. Go to **Edit > Preferences > Add-ons**
4. Click **"Install..."** and select `addon_new.py` (or `addon.py`)
5. **Enable** the addon by checking the box next to "Interface: Blender MCP"
6. **Restart Blender completely**

### Step 2: Start the Blender MCP Server

1. In Blender, open the **3D Viewport sidebar** (press `N` if not visible)
2. Find the **"BlenderMCP"** tab
3. (Optional) Enable **Poly Haven** checkbox if you want asset integration
4. Click **"Connect to Claude"** or **"Start Server"**
5. You should see: **"Running on port 9876"** (or your configured port)

### Step 3: Configure MCP Client

#### Claude Desktop

1. Open Claude Desktop
2. Go to **Settings > Developer > Edit Config**
3. Edit `claude_desktop_config.json`

**If this is your first MCP server:**
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["blender-mcp"]
        }
    }
}
```

**If you already have other MCP servers:**
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["blender-mcp"]
        },
        "filesystem": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "/path/to/directory"
            ]
        }
    }
}
```

4. **Restart Claude Desktop**

**Setup Video**: [Watch the tutorial](https://www.youtube.com/watch?v=neoK_WMq92g)

#### Cursor IDE

**For Mac users:**
- Go to **Settings > MCP > Add Server**
- Or create `.cursor/mcp.json` in your project root

**For Windows users:**
- Go to **Settings > MCP > Add Server**

**Configuration:**
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["blender-mcp"]
        }
    }
}
```

**Windows alternative:**
```json
{
    "mcpServers": {
        "blender": {
            "command": "cmd",
            "args": ["/c", "uvx", "blender-mcp"]
        }
    }
}
```

**Setup Video**: [Cursor setup tutorial](https://www.youtube.com/watch?v=wgWsJshecac)

#### Visual Studio Code

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_blender--mcp_server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=ffffff)](vscode:mcp/install?%7B%22name%22%3A%22blender-mcp%22%2C%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22blender-mcp%22%5D%7D)

Or manually add to your VS Code MCP configuration.

### Step 4: Verify Installation

1. **Restart** your AI client (Claude/Cursor/VS Code)
2. **Restart** Blender (if needed)
3. In your AI client, you should see Blender MCP tools available (hammer icon in Claude)
4. Try asking: **"Get information about the current Blender scene"**

**Check Blender Console:**
- Look for: `Registered 80+ handlers` (or similar)
- If you see errors, check the troubleshooting section

---

## Complete Command Reference

### Scene Management

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `get_scene_info` | Get detailed scene information | `user_prompt` (required) |
| `get_object_info` | Get information about a specific object | `object_name` |
| `get_viewport_screenshot` | Capture current viewport as image | `width`, `height` (optional) |
| `execute_code` | Execute Python code in Blender | `code` (required) |
| `setup_project` | Configure project settings | `frame_start`, `frame_end`, `fps`, `resolution_x`, `resolution_y`, `render_engine`, `collections` |

### Animation - Keyframes

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_keyframe` | Create a keyframe | `object_name`, `data_path`, `frame`, `value`, `interpolation` |
| `delete_keyframe` | Delete keyframe(s) | `object_name`, `data_path`, `frame`, `frame_range` (optional) |
| `get_keyframes` | Get all keyframes for an object | `object_name`, `data_path`, `frame_range` (optional) |
| `batch_keyframes` | Create multiple keyframes at once | `object_name`, `keyframes` (array) |

### Animation - Timeline

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `set_current_frame` | Set the current frame | `frame` |
| `get_timeline_info` | Get timeline information | None |
| `set_frame_range` | Set frame range | `frame_start`, `frame_end` |
| `playback_control` | Control playback | `action`: `PLAY`, `PAUSE`, `STOP`, `REWIND`, `FORWARD` |

### Animation - F-Curves

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `get_fcurves` | Get F-curve information | `object_name` |
| `set_fcurve_interpolation` | Set interpolation type | `object_name`, `data_path`, `interpolation` |
| `set_fcurve_handles` | Modify curve handles | `object_name`, `data_path`, `frame`, `handle_type` |
| `add_fcurve_modifier` | Add modifier to F-curve | `object_name`, `data_path`, `modifier_type`, `modifier_params` |
| `remove_fcurve_modifier` | Remove F-curve modifier | `object_name`, `data_path`, `modifier_name` |
| `smooth_fcurve` | Smooth F-curve | `object_name`, `data_path`, `factor` |

### Animation - Actions

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_action` | Create new action | `action_name` |
| `assign_action` | Assign action to object | `object_name`, `action_name` |
| `get_action_info` | Get action information | `action_name` |
| `list_actions` | List all actions | None |
| `duplicate_action` | Duplicate an action | `source_action`, `new_action_name` |
| `delete_action` | Delete an action | `action_name` |
| `push_down_action` | Push action to NLA | `object_name`, `action_name` |
| `get_object_action` | Get object's current action | `object_name` |

### Animation - Constraints

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `add_constraint` | Add constraint to object | `object_name`, `constraint_type`, `target`, `constraint_params` |
| `modify_constraint` | Modify existing constraint | `object_name`, `constraint_name`, `constraint_params` |
| `remove_constraint` | Remove constraint | `object_name`, `constraint_name` |

### Animation - Shape Keys

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_shape_key` | Create shape key | `mesh_name`, `shape_key_name`, `value` (optional) |
| `set_shape_key_value` | Set shape key value | `mesh_name`, `shape_key_name`, `value` |
| `get_shape_keys` | Get all shape keys | `mesh_name` |

### Animation - Baking

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `bake_animation` | Bake animation to keyframes | `object_name`, `frame_start`, `frame_end`, `data_paths` (optional) |
| `bake_armature_animation` | Bake armature animation | `armature_name`, `frame_start`, `frame_end` |
| `sample_animation` | Sample animation at intervals | `object_name`, `frame_start`, `frame_end`, `step` |
| `clean_keyframes` | Remove redundant keyframes | `object_name`, `data_path`, `threshold` |

### Rigging - Armatures

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_armature` | Create armature object | `name`, `location`, `add_bones` (optional) |
| `get_armature_info` | Get armature information | `armature_name` |

### Rigging - Bones

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_bone` | Create bone in armature | `armature_name`, `bone_name`, `head`, `tail`, `parent` (optional) |
| `get_bone_info` | Get bone information | `armature_name`, `bone_name` |
| `transform_bone` | Transform bone | `armature_name`, `bone_name`, `location`, `rotation`, `scale` |
| `delete_bone` | Delete bone | `armature_name`, `bone_name`, `delete_children` (optional) |
| `set_bone_parent` | Set bone parent | `armature_name`, `bone_name`, `parent_name` |
| `duplicate_bone` | Duplicate bone | `armature_name`, `bone_name`, `new_bone_name` |

### Rigging - Weights & Skinning

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `parent_to_armature` | Parent mesh to armature | `mesh_name`, `armature_name`, `type`: `ARMATURE` |
| `create_vertex_group` | Create vertex group | `mesh_name`, `group_name` |
| `set_vertex_weights` | Set vertex weights | `mesh_name`, `group_name`, `weights` (array of {index, weight}) |
| `get_vertex_weights` | Get vertex weights | `mesh_name`, `group_name` |
| `normalize_weights` | Normalize vertex weights | `mesh_name`, `group_name` |
| `transfer_weights` | Transfer weights between meshes | `source_mesh`, `target_mesh`, `method` |
| `get_vertex_groups` | Get all vertex groups | `mesh_name` |
| `auto_weight_assign` | Automatically assign weights | `mesh_name`, `armature_name`, `method` (optional) |

### Rigging - Pose

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `set_bone_pose` | Set bone pose | `armature_name`, `bone_name`, `location`, `rotation`, `scale` |
| `get_bone_pose` | Get bone pose | `armature_name`, `bone_name` |
| `clear_pose` | Clear all poses | `armature_name` |
| `apply_pose_as_rest` | Apply pose as rest pose | `armature_name` |
| `copy_pose` | Copy pose from another armature | `source_armature`, `target_armature` |
| `get_all_bone_poses` | Get all bone poses | `armature_name` |

### Rigging - Bone Constraints

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `add_bone_constraint` | Add constraint to bone | `armature_name`, `bone_name`, `constraint_type`, `target`, `constraint_params` |
| `setup_ik_chain` | Setup IK chain | `armature_name`, `chain_bones`, `target_bone`, `pole_target` (optional) |
| `modify_bone_constraint` | Modify bone constraint | `armature_name`, `bone_name`, `constraint_name`, `constraint_params` |
| `remove_bone_constraint` | Remove bone constraint | `armature_name`, `bone_name`, `constraint_name` |
| `get_bone_constraints` | Get bone constraints | `armature_name`, `bone_name` |

### Rigging - Templates & Auto-Rigging

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_humanoid_rig` | Create humanoid rig template | `armature_name`, `scale` (optional) |
| `create_simple_rig` | Create simple rig | `armature_name`, `bone_count`, `bone_length` |
| `mirror_bones` | Mirror bones | `armature_name`, `axis`: `X`, `Y`, or `Z` |
| `rig_hand` | Auto-rig a hand mesh | `mesh_name`, `finger_count` (optional), `bone_scale` (optional) |
| `rig_body` | Auto-rig a body mesh | `mesh_name`, `scale` (optional) |

### Modeling

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_primitive` | Create primitive mesh | `type`: `MESH_CUBE`, `MESH_SPHERE`, `MESH_CYLINDER`, etc., `name`, `location`, `scale` |
| `extrude_mesh` | Extrude mesh faces | `mesh_name`, `face_indices`, `distance`, `direction` (optional) |

### Rendering - Settings

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `set_render_engine` | Set render engine | `engine`: `CYCLES`, `EEVEE`, `WORKBENCH` |
| `set_render_resolution` | Set resolution | `resolution_x`, `resolution_y`, `resolution_percentage` |
| `set_render_output` | Set output path and format | `filepath`, `file_format`: `PNG`, `JPEG`, `OPEN_EXR`, `TIFF` |
| `set_render_samples` | Set render samples | `engine`, `samples`, `use_denoising` (optional) |
| `get_render_settings` | Get current render settings | None |

### Rendering - Operations

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `render_image` | Render single image | `filepath` (optional) |
| `render_animation` | Render animation | `filepath` (optional), `frame_start`, `frame_end` (optional) |
| `get_render_progress` | Get render progress | None |

### Camera

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_camera` | Create camera | `name`, `location`, `rotation`, `type`: `PERSP`, `ORTHO`, `PANO` |
| `set_active_camera` | Set active camera | `camera_name` |
| `set_camera_properties` | Set camera properties | `camera_name`, `lens`, `sensor_width`, `clip_start`, `clip_end` |
| `set_camera_dof` | Set depth of field | `camera_name`, `focus_distance`, `fstop`, `focus_object` (optional) |
| `get_camera_info` | Get camera information | `camera_name` |
| `add_camera_constraint` | Add constraint to camera | `camera_name`, `constraint_type`, `target` |

### Lighting

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `create_light` | Create light | `name`, `type`: `SUN`, `AREA`, `POINT`, `SPOT`, `location`, `energy` |
| `set_light_properties` | Set light properties | `light_name`, `energy`, `color`, `size` (for area lights) |
| `get_light_info` | Get light information | `light_name` |
| `create_three_point_lighting` | Create three-point lighting setup | `key_location`, `fill_location`, `rim_location` (optional) |
| `set_world_lighting` | Set world/environment lighting | `strength`, `color`, `use_nodes` (optional) |

### Integrations

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `get_polyhaven_status` | Check Poly Haven status | None |
| `get_polyhaven_categories` | Get Poly Haven categories | None |
| `search_polyhaven_assets` | Search Poly Haven assets | `category`, `query` (optional) |
| `download_polyhaven_asset` | Download Poly Haven asset | `asset_id`, `asset_type` |
| `get_sketchfab_status` | Check Sketchfab status | None |
| `search_sketchfab_models` | Search Sketchfab models | `query`, `limit` (optional) |
| `get_sketchfab_model_preview` | Get model preview | `model_id` |
| `download_sketchfab_model` | Download Sketchfab model | `model_id` |
| `get_hyper3d_status` | Check Hyper3D status | None |
| `create_rodin_job` | Create Hyper3D generation job | `prompt`, `style` (optional) |
| `poll_rodin_job_status` | Check job status | `job_id` |
| `import_generated_asset` | Import generated asset | `job_id` |
| `get_hunyuan3d_status` | Check Hunyuan3D status | None |

---

## Usage Examples

### Basic Scene Creation

```
"Create a low poly scene in a dungeon, with a dragon guarding a pot of gold"
```

### Animation Workflow

```
"Create a bouncing ball animation. The ball should start at frame 1 at position (0, 0, 5), 
bounce at frame 15 at (0, 0, 0), and return to (0, 0, 5) at frame 30"
```

### Rigging Workflow

```
"Rig the hand mesh with 5 fingers. Create an armature, add bones for each finger, 
parent the mesh to the armature, and apply automatic weights"
```

### Rendering Setup

```
"Set up the scene for a 30-second video at 30fps, 1920x1080 resolution, using Eevee 
with bloom and volumetric lighting. Create collections for ENV, CHAR, PROPS, FX, CAM, and LIGHTS"
```

### Camera and Lighting

```
"Create a three-point lighting setup, add a camera pointing at the scene, 
set depth of field with the cube as the focus object"
```

### Project Setup

```
"Set up a new project: 900 frames at 30fps, 1920x1080 resolution, Eevee engine with 
bloom enabled, and create organized collections"
```

### Using Assets

```
"Search Poly Haven for rock models and download one. Then search for a beach HDRI 
and apply it to the world"
```

### Code Execution

```
"Execute Python code to create 10 cubes in a circle pattern"
```

---

## Use Cases

### 🎬 Video Production
- **Teaser Videos**: Quick project setup with proper frame rates, resolution, and collections
- **Animation**: Full keyframe and timeline control for character and object animation
- **Rendering**: Automated render setup and batch rendering

### 🎮 Game Development
- **Character Rigging**: Auto-rig characters with proper bone hierarchies
- **Asset Creation**: Generate and import 3D models from various sources
- **Scene Building**: Rapid prototyping and scene assembly

### 🎨 3D Art & Design
- **Concept Art**: Generate 3D scenes from reference images
- **Product Visualization**: Set up studio lighting and camera angles
- **Architectural Visualization**: Create environments with proper lighting and materials

### 🔬 Technical Workflows
- **Automation**: Script complex Blender operations through natural language
- **Batch Processing**: Set up multiple renders or animations
- **Pipeline Integration**: Integrate Blender into larger production pipelines

### 📚 Education & Learning
- **Tutorial Creation**: Generate example scenes and animations
- **Experimentation**: Quickly test ideas and iterate on designs
- **Learning Tool**: Understand Blender operations through AI assistance

---

## Environment Variables

Configure the Blender connection with environment variables:

```bash
export BLENDER_HOST='localhost'      # Default: localhost
export BLENDER_PORT=9876             # Default: 9876
```

For remote Blender instances:
```bash
export BLENDER_HOST='192.168.1.100'  # Remote IP address
export BLENDER_PORT=9876
```

---

## Troubleshooting

### Connection Issues

**Problem**: "Could not connect to Blender"

**Solutions**:
1. Verify Blender addon is enabled and server is running
2. Check that port 9876 (or your configured port) is not blocked
3. Ensure MCP server is configured correctly in your AI client
4. Try restarting both Blender and your AI client
5. Check Blender console for error messages

### Commands Not Working

**Problem**: Only basic commands work, new features don't

**Solutions**:
1. **Full Blender restart** (not just reload) - completely close and reopen Blender
2. Check Blender console for: `Registered 80+ handlers` (or similar)
3. Verify all files were copied correctly (check `core/`, `handlers/`, `utils/` directories exist)
4. Check for import errors in Blender console
5. Re-run `setup_blender_addon.sh` if using automated setup

### Timeout Errors

**Problem**: Commands timeout or fail on large operations

**Solutions**:
1. Break complex operations into smaller steps
2. Use dedicated handlers (e.g., `setup_project`) instead of long `execute_code` scripts
3. Increase timeout settings if available
4. Simplify your requests

### Handler Registration Issues

**Problem**: Console shows "Registered 2 handlers" instead of 80+

**Solutions**:
1. Modular system not loaded - check that `core/`, `handlers/`, `utils/` directories are in Blender's addon folder
2. Check for import errors in Blender console
3. Verify all `__init__.py` files exist
4. Restart Blender completely (clears Python cache)

### Integration Issues

**Problem**: Poly Haven, Sketchfab, or other integrations not working

**Solutions**:
1. Check that the integration is enabled in BlenderMCP panel
2. Verify internet connection
3. Check API keys if required (Hyper3D, Hunyuan3D)
4. Review integration-specific error messages in Blender console

---

## Technical Details

### Architecture

The system consists of:

1. **Blender Addon** (`addon_new.py`): Socket server within Blender that receives and executes commands
2. **MCP Server** (`src/blender_mcp/server.py`): Python server implementing Model Context Protocol
3. **Handler System**: Modular handlers organized by category (animation, rigging, rendering, etc.)
4. **Command Router**: Routes commands to appropriate handlers with validation and error handling

### Communication Protocol

- **Protocol**: JSON over TCP sockets
- **Port**: 9876 (configurable)
- **Commands**: JSON objects with `type` and `params`
- **Responses**: JSON objects with `status` and `result` or `error`

### Handler System

Handlers are organized into categories:
- `handlers/scene/` - Scene management and object operations
- `handlers/animation/` - Animation, keyframes, F-curves, actions
- `handlers/rigging/` - Armatures, bones, weights, constraints
- `handlers/modeling/` - Mesh creation and editing
- `handlers/rendering/` - Render settings, cameras, lighting
- `handlers/integrations/` - Third-party service integrations

Each handler extends `BaseHandler` and implements:
- `get_command_name()` - Returns the command name
- `get_parameter_schema()` - Defines required/optional parameters
- `execute(params)` - Executes the command

---

## Limitations & Security

### Security Considerations

- **Code Execution**: The `execute_code` command allows running arbitrary Python code in Blender. Use with caution in production environments.
- **Network Access**: The socket server listens on localhost by default but can be configured for remote access.
- **File System Access**: Commands can read/write files through Blender's Python API.

### Best Practices

1. **Always save your work** before using `execute_code` or making major changes
2. **Test in a separate Blender file** before applying to important projects
3. **Review generated code** when possible, especially for complex operations
4. **Use dedicated handlers** instead of raw `execute_code` when available (more reliable and type-safe)

### Known Limitations

- Complex operations might need to be broken into smaller steps
- Some Blender operations require specific context (object selection, mode, etc.)
- Large code blocks in `execute_code` may timeout - use dedicated handlers instead
- Integration features (Poly Haven, Sketchfab) require internet connection

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Clone the repository
2. Install dependencies
3. Set up development environment
4. Make your changes
5. Test thoroughly
6. Submit a PR

---

## Release Notes

### Version 2.1.0 (Current)
- ✅ Complete animation system (keyframes, F-curves, actions, baking)
- ✅ Advanced rigging system (bones, weights, constraints, auto-rigging)
- ✅ Rendering system (engines, cameras, lighting)
- ✅ Modeling operations
- ✅ Project setup handler
- ✅ Enhanced error handling and logging
- ✅ Improved `execute_code` with better imports and error reporting

### Version 1.4.0
- Added Hunyuan3D support
- View screenshots for Blender viewport
- Search and download Sketchfab models
- Support for Poly Haven assets
- Support for Hyper3D Rodin
- Run Blender MCP on remote host
- Telemetry for tools executed

---

## License

See LICENSE file for details.

---

## Disclaimer

This is a third-party integration and not made by Blender. This project extends the original work by Siddharth Ahuja with significant additional features and capabilities.

---

## Support

- **Discord Community**: [Join us](https://discord.gg/z5apgR8TFU)
- **GitHub Issues**: Report bugs and request features
- **Documentation**: See spec files (`*_SPEC.md`) for detailed command documentation

---

**Made with ❤️ for the Blender and AI communities**
