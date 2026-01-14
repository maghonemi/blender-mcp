# Blender MCP - Comprehensive Edition v2.0

## Overview

This is the enhanced, modular version of Blender MCP with comprehensive Blender control capabilities including animation, rigging, modeling, and more. The new system features:

- ✅ **Modular Architecture**: Clean, maintainable code structure
- ✅ **Comprehensive Handlers**: 24+ commands for full Blender control
- ✅ **Animation System**: Keyframes, timeline, constraints, shape keys
- ✅ **Rigging System**: Armatures, bones, and bone operations
- ✅ **Modeling Tools**: Mesh creation, editing, and manipulation
- ✅ **Enhanced Error Handling**: Better error messages and validation
- ✅ **Improved Logging**: Comprehensive logging system
- ✅ **Performance**: Caching and optimization features

## Installation

### ⚠️ IMPORTANT: Directory Installation Required

The new modular system **requires the entire directory structure** to be installed. You **cannot** install just `addon_new.py` as a single file - it needs access to `core/`, `handlers/`, and `utils/` directories.

### Step 1: Prepare the Addon

**Option A: Install as Directory Addon (RECOMMENDED)**

1. **Copy the entire `blender-mcp-main` directory** to Blender's addons folder:
   - **macOS**: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - **Linux**: `~/.config/blender/[version]/scripts/addons/`

2. **Rename the directory** to `blender_mcp` (remove spaces, use underscore)

3. **Rename `addon_new.py` to `addon.py`** inside the directory

**Option B: Copy Required Files**

If you want to keep the original structure, copy these to Blender's addons folder:
- `addon_new.py` → rename to `addon.py`
- `core/` directory (entire directory)
- `handlers/` directory (entire directory)
- `utils/` directory (entire directory)

All should be in the same folder: `blender_mcp/`

### Step 2: Install in Blender

1. **Open Blender**
2. Go to **Edit > Preferences > Add-ons**
3. Click **Install...** button
4. Navigate to the `blender-mcp-main` directory
5. Select **`addon.py`** (or `addon_new.py` if you kept both)
6. Click **Install Add-on**
7. Find **"Interface: Blender MCP"** in the addon list
8. **Enable** the addon by checking the box

### Step 3: Verify Installation

1. In Blender's 3D Viewport, press **N** to open the sidebar
2. Look for the **"BlenderMCP"** tab
3. You should see the control panel

## Configuration

### Basic Setup

1. **Open the BlenderMCP Panel**
   - In 3D Viewport, press **N** (or View > Sidebar)
   - Click the **"BlenderMCP"** tab

2. **Configure Port** (optional)
   - Default port is `9876`
   - Change if needed (must be between 1024-65535)

3. **Enable Integrations** (optional)
   - Check **"Use assets from Poly Haven"** for Poly Haven integration
   - Check **"Use Hyper3D Rodin 3D model generation"** for AI model generation
   - Check **"Use assets from Sketchfab"** for Sketchfab models
   - Check **"Use Tencent Hunyuan 3D model generation"** for Hunyuan3D

4. **Configure API Keys** (if using integrations)
   - Enter API keys in the respective fields
   - For Hyper3D, you can use the **"Set Free Trial API Key"** button

### Connect to MCP Server

1. **Start the Server**
   - In the BlenderMCP panel, click **"Connect to MCP server"**
   - You should see: "BlenderMCP server started on localhost:9876" in the console

2. **Verify Connection**
   - The panel should show: "Running on port 9876"
   - The button changes to **"Disconnect from MCP server"**

## MCP Server Configuration

### For Claude Desktop

1. **Open Claude Desktop Settings**
   - Click the settings icon
   - Go to **"Developer"** or **"MCP"** section

2. **Add MCP Server**
   - Click **"Add Server"** or edit `claude_desktop_config.json`
   - Location: 
     - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
     - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

3. **Add Configuration**
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

4. **Restart Claude Desktop**

### For Cursor IDE

1. **Open Cursor Settings**
   - Go to **Settings > MCP**

2. **Add Global MCP Server** (or project-specific)
   - For global: Use "add new global MCP server"
   - For project: Create `.cursor/mcp.json` in project root

3. **Add Configuration**
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

4. **Restart Cursor**

## Available Commands

### Scene Operations
- `get_scene_info` - Get information about the current scene
- `get_object_info` - Get detailed information about an object
- `get_viewport_screenshot` - Capture a screenshot of the viewport
- `execute_code` - Execute arbitrary Python code in Blender

### Animation Operations
- `create_keyframe` - Create a keyframe
- `delete_keyframe` - Delete keyframe(s)
- `get_keyframes` - Get all keyframes for a data path
- `batch_keyframes` - Batch keyframe operations
- `set_current_frame` - Set the current timeline frame
- `get_timeline_info` - Get timeline information
- `set_frame_range` - Set animation frame range
- `playback_control` - Control playback (play/pause/stop)
- `add_constraint` - Add a constraint to an object
- `modify_constraint` - Modify constraint properties
- `remove_constraint` - Remove a constraint
- `create_shape_key` - Create a shape key
- `set_shape_key_value` - Set shape key value
- `get_shape_keys` - Get all shape keys for an object

### Rigging Operations
- `create_armature` - Create a new armature
- `get_armature_info` - Get armature information
- `create_bone` - Create a bone in an armature
- `get_bone_info` - Get bone information

### Modeling Operations
- `create_primitive` - Create a primitive mesh (cube, sphere, etc.)
- `extrude_mesh` - Extrude mesh elements

## Usage Examples

### Example 1: Get Scene Information
```json
{
  "type": "get_scene_info",
  "params": {}
}
```

### Example 2: Create a Keyframe
```json
{
  "type": "create_keyframe",
  "params": {
    "object_name": "Cube",
    "data_path": "location",
    "frame": 1,
    "value": [0, 0, 0],
    "interpolation": "BEZIER"
  }
}
```

### Example 3: Create an Armature
```json
{
  "type": "create_armature",
  "params": {
    "name": "MyArmature",
    "location": [0, 0, 0],
    "add_bones": true
  }
}
```

### Example 4: Create a Primitive
```json
{
  "type": "create_primitive",
  "params": {
    "type": "MESH_SPHERE",
    "name": "MySphere",
    "location": [0, 0, 0],
    "scale": [1, 1, 1]
  }
}
```

## Architecture

The new system uses a modular architecture:

```
blender-mcp/
├── core/                    # Core server and routing
│   ├── server.py            # Socket server
│   ├── command_router.py    # Command routing
│   ├── context_manager.py   # Context management
│   └── response_builder.py  # Response formatting
├── handlers/                 # Command handlers
│   ├── base_handler.py      # Base handler class
│   ├── handler_registry.py  # Handler registration
│   ├── scene/               # Scene handlers
│   ├── animation/           # Animation handlers
│   ├── rigging/             # Rigging handlers
│   ├── modeling/            # Modeling handlers
│   └── integrations/        # Integration handlers
├── utils/                    # Utilities
│   ├── logger.py            # Logging system
│   ├── error_handler.py     # Error handling
│   ├── cache.py             # Caching
│   └── validation.py        # Parameter validation
└── addon.py                  # Main addon file (or addon_new.py)
```

## Troubleshooting

### Server Won't Start

1. **Check Port Availability**
   - Make sure port 9876 (or your configured port) is not in use
   - Try changing the port in the BlenderMCP panel

2. **Check Console**
   - Open Blender's console (Window > Toggle System Console)
   - Look for error messages

3. **Check Logs**
   - Logs are saved to: `{Blender temp directory}/blendermcp/blendermcp_YYYYMMDD.log`

### MCP Server Not Connecting

1. **Verify Blender Server is Running**
   - Check that "Running on port XXXX" is shown in the panel
   - The "Connect" button should say "Disconnect"

2. **Check MCP Configuration**
   - Verify the MCP server config in Claude/Cursor
   - Make sure `uvx blender-mcp` command works in terminal

3. **Test Connection**
   - Try connecting from terminal: `telnet localhost 9876`
   - Should connect (though you'll need to send JSON)

### Commands Not Working

1. **Check Handler Registration**
   - Open Blender console
   - Look for "Registered X handlers" message
   - Should see handler registration messages

2. **Check Error Messages**
   - Check Blender console for error messages
   - Check log files for detailed errors

3. **Verify Command Format**
   - Commands must be valid JSON
   - Required parameters must be provided
   - Check command documentation

### Import Errors

If you see import errors:

1. **Check File Structure**
   - Ensure all directories exist (core/, handlers/, utils/)
   - All `__init__.py` files should be present

2. **Check Python Path**
   - Blender should automatically add the addon directory to Python path
   - If not, check Blender's Python console: `import sys; print(sys.path)`

## Migration from Old System

If you're upgrading from the old addon:

1. **Backup Your Settings**
   - Note your API keys and preferences
   - The new system uses the same property names

2. **Uninstall Old Addon**
   - Disable and remove the old addon
   - Restart Blender

3. **Install New Addon**
   - Follow installation steps above
   - Re-enter your API keys and preferences

4. **Test**
   - Start with basic commands
   - Verify integrations work

## Differences from Old System

### Improvements

1. **Modular Structure**: Code is organized into logical modules
2. **Better Error Handling**: More descriptive error messages
3. **Validation**: Parameter validation before execution
4. **Logging**: Comprehensive logging system
5. **Caching**: Performance improvements with caching
6. **Extensibility**: Easy to add new handlers

### Backward Compatibility

- ✅ Same command protocol
- ✅ Same response format
- ✅ Same UI and preferences
- ✅ Same integration APIs

### New Features

- ✅ More animation commands
- ✅ Rigging support
- ✅ Enhanced modeling tools
- ✅ Better error messages
- ✅ Performance optimizations

## Development

### Adding New Handlers

1. **Create Handler Class**
   ```python
   from handlers.base_handler import BaseHandler
   
   class MyHandler(BaseHandler):
       def get_command_name(self) -> str:
           return "my_command"
       
       def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
           return {
               "param1": {
                   "type": str,
                   "required": True
               }
           }
       
       def execute(self, params: Dict[str, Any]) -> Any:
           # Your implementation
           return {"result": "success"}
   ```

2. **Register Handler**
   - Add import to `handlers/handler_registry.py`
   - Add registration in `register_all_handlers()`

3. **Test**
   - Test in Blender
   - Check logs for errors

## Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: See `PLANNING.md`, `ARCHITECTURE.md`, and spec files
- **Logs**: Check log files for detailed error information

## License

Same as original project (see LICENSE file)

---

**Version**: 2.0.0  
**Last Updated**: 2025-01-14
