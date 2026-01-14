# Quick Start Guide - Blender MCP v2.0

## Which File to Use?

**Yes, use `addon_new.py` as your MCP addon!**

### Option 1: Replace the Old Addon (Recommended)

```bash
# In the blender-mcp-main directory:
cp addon.py addon_old.py          # Backup original
cp addon_new.py addon.py          # Use new version
```

Then install `addon.py` in Blender as usual.

### Option 2: Use addon_new.py Directly

1. Install `addon_new.py` directly in Blender
2. Blender will recognize it as "Blender MCP"
3. Enable it normally

## Installation Steps

### 1. Install in Blender

1. Open Blender
2. **Edit > Preferences > Add-ons**
3. Click **"Install..."**
4. Select **`addon.py`** (or `addon_new.py` if using Option 2)
5. Click **"Install Add-on"**
6. Find **"Interface: Blender MCP"** in the list
7. **Enable** it (check the box)

### 2. Configure in Blender

1. In 3D Viewport, press **N** to open sidebar
2. Click **"BlenderMCP"** tab
3. Click **"Connect to MCP server"**
4. You should see: **"Running on port 9876"**

### 3. Configure MCP Client (Claude/Cursor)

#### For Claude Desktop:

Edit `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add:
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

#### For Cursor:

Go to **Settings > MCP** and add:
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

### 4. Restart and Test

1. **Restart** Claude Desktop or Cursor
2. **Restart** Blender (if needed)
3. In Claude/Cursor, you should see Blender MCP tools available
4. Try: "Get information about the current Blender scene"

## What's New in v2.0?

✅ **24+ New Commands** for animation, rigging, and modeling  
✅ **Modular Architecture** - easier to maintain and extend  
✅ **Better Error Handling** - clearer error messages  
✅ **Performance Improvements** - caching and optimization  
✅ **Comprehensive Logging** - better debugging  

## Troubleshooting

### "Server won't start"
- Check if port 9876 is available
- Try changing the port in BlenderMCP panel
- Check Blender console for errors

### "MCP not connecting"
- Verify Blender shows "Running on port XXXX"
- Check MCP config file syntax
- Make sure `uvx blender-mcp` works in terminal

### "Commands not working"
- Check Blender console for errors
- Verify handler registration (should see "Registered X handlers")
- Check log files in Blender temp directory

## Need More Help?

- See `README_NEW_SYSTEM.md` for detailed documentation
- Check `COMPILATION_REPORT.md` for system status
- Review `IMPLEMENTATION_STATUS.md` for feature list

---

**Ready to use!** The new system is fully functional and ready for Blender control via MCP.
