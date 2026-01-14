# MCP Configuration with Filesystem Server

## Adding Blender MCP to Existing Configuration

If you already have MCP servers configured (like filesystem), you need to **add** the blender server to your existing configuration, not replace it.

## Complete Configuration

### For Claude Desktop

Edit `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Add the blender server to your existing config:**

```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": [
                "blender-mcp"
            ]
        },
        "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/path/to/your/Desktop",
              "/path/to/your/Downloads"
            ]
        }
    }
}
```

### For Cursor

**Option 1: Global MCP Server**

Go to **Settings > MCP > Add Server** and add:

```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": [
                "blender-mcp"
            ]
        },
        "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/path/to/your/Desktop",
              "/path/to/your/Downloads"
            ]
        }
    }
}
```

**Option 2: Project-Specific**

Create `.cursor/mcp.json` in your project root:

```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": [
                "blender-mcp"
            ]
        },
        "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/path/to/your/Desktop",
              "/path/to/your/Downloads"
            ]
        }
    }
}
```

## Important Notes

1. **Keep both servers**: Don't remove your existing `filesystem` server
2. **Comma required**: Make sure there's a comma between server entries
3. **Restart required**: After updating the config, restart Claude Desktop or Cursor
4. **Blender must be running**: The blender MCP server requires Blender to be running with the addon enabled

## Verification

After restarting, you should see both servers available:
- ✅ Blender MCP tools (get_scene_info, create_keyframe, etc.)
- ✅ Filesystem tools (read_file, write_file, etc.)

## Troubleshooting

### "Blender MCP not connecting"
- Make sure Blender is running
- Check that the addon is enabled in Blender
- Verify the server is started (check BlenderMCP panel)
- Check Blender console for errors

### "Filesystem server not working"
- Verify the paths exist (replace with your actual paths in the config): `/path/to/your/Desktop` and `/path/to/your/Downloads`
- Check that `npx` is available: `which npx`
- Check Cursor/Claude console for filesystem errors

### "Config file errors"
- Make sure JSON is valid (use a JSON validator)
- Check for missing commas between server entries
- Ensure all quotes are properly escaped

## Example: Adding More Servers

You can add multiple MCP servers:

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
              "/path/to/your/Desktop",
              "/path/to/your/Downloads"
            ]
        },
        "another-server": {
            "command": "npx",
            "args": ["-y", "@some/other-server"]
        }
    }
}
```
