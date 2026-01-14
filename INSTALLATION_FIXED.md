# Installation Guide - Fixed Version

## Important: How to Install

The new modular system requires the `core/`, `handlers/`, and `utils/` directories to be accessible. You have **two installation options**:

### Option 1: Install as Directory Addon (RECOMMENDED)

**This is the recommended method** - install the entire directory structure:

1. **Copy the entire `blender-mcp-main` directory** to Blender's addons folder:
   - **macOS**: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - **Linux**: `~/.config/blender/[version]/scripts/addons/`

2. **Rename it** to `blender_mcp` (remove spaces, use underscore)

3. **In Blender**:
   - Go to **Edit > Preferences > Add-ons**
   - Search for "Blender MCP"
   - Enable it

### Option 2: Install Single File (Requires Modules)

If you want to install just `addon_new.py`:

1. **Copy the entire directory structure** to Blender's addons folder:
   ```
   blender_mcp/
   ├── addon_new.py  (rename to addon.py)
   ├── core/
   ├── handlers/
   └── utils/
   ```

2. **Rename `addon_new.py` to `addon.py`**

3. **Install in Blender** as a directory addon

## Quick Fix for Current Error

If you're getting "No module named 'core'" error:

1. **Don't install just `addon_new.py` as a single file**
2. **Install the entire directory structure** instead

### Steps:

1. **Copy these directories** to Blender's addons folder:
   - `core/` (entire directory)
   - `handlers/` (entire directory)  
   - `utils/` (entire directory)
   - `addon_new.py` (rename to `addon.py`)

2. **Structure should look like:**
   ```
   [Blender addons folder]/
   └── blender_mcp/
       ├── addon.py  (renamed from addon_new.py)
       ├── core/
       │   ├── __init__.py
       │   ├── server.py
       │   ├── command_router.py
       │   ├── context_manager.py
       │   └── response_builder.py
       ├── handlers/
       │   ├── __init__.py
       │   ├── base_handler.py
       │   ├── handler_registry.py
       │   ├── scene/
       │   ├── animation/
       │   ├── rigging/
       │   ├── modeling/
       │   └── integrations/
       └── utils/
           ├── __init__.py
           ├── logger.py
           ├── error_handler.py
           ├── cache.py
           └── validation.py
   ```

3. **In Blender**:
   - Go to **Edit > Preferences > Add-ons**
   - Click **"Refresh"** if needed
   - Search for "Blender MCP"
   - Enable it

## Verification

After installation, check Blender's console (Window > Toggle System Console):

- ✅ Should see: "All handlers registered successfully"
- ✅ Should see: "BlenderMCP addon registered (v2.0)"
- ❌ Should NOT see: "No module named 'core'"

## Alternative: Use Original addon.py

If you need a quick solution and don't need the new features yet:

1. Use the original `addon.py` (it's a single file, works immediately)
2. The new modular system will be available once properly installed

## Troubleshooting

### Still Getting Import Errors?

1. **Check directory structure** - all `__init__.py` files must exist
2. **Check Blender console** - look for the actual error message
3. **Verify paths** - the addon should be in Blender's addons folder
4. **Check permissions** - ensure Blender can read all files

### Module Not Found Errors?

The error message will show which module is missing. Ensure:
- `core/` directory exists with all files
- `handlers/` directory exists with all files
- `utils/` directory exists with all files
- All `__init__.py` files are present

## Next Steps

Once installed correctly:
1. Open BlenderMCP panel (N key in 3D viewport)
2. Click "Connect to MCP server"
3. Configure MCP client (Claude/Cursor)
4. Start using the new commands!

---

**Remember**: The modular system requires the directory structure. Install as a directory addon, not a single file!
