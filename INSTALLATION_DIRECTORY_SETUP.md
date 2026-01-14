# How to Install Blender MCP as Directory Addon

## The Problem

If you install just `addon_new.py` as a single file, Blender cannot find the `core/`, `handlers/`, and `utils/` directories. This causes:
- ✗ Render handlers NOT registered
- ✗ Sketchfab handlers NOT registered
- Only 24 handlers instead of 28+

## Solution: Install as Directory Addon

### Step 1: Create the Addon Directory

**On macOS:**

1. Open Terminal
2. Navigate to Blender's addons folder:
   ```bash
   cd ~/Library/Application\ Support/Blender/[version]/scripts/addons/
   ```
   Replace `[version]` with your Blender version (e.g., `4.0`, `4.1`, `3.6`)

3. Create the addon directory:
   ```bash
   mkdir -p blender_mcp
   cd blender_mcp
   ```

### Step 2: Copy Files

Copy these from your `blender-mcp-main` directory:

```bash
# From blender-mcp-main directory, copy:
cp addon_new.py ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/__init__.py
cp -r core ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/
cp -r handlers ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/
cp -r utils ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/
```

### Step 3: Verify Structure

Your `blender_mcp` folder should look like:
```
blender_mcp/
├── __init__.py          (this is addon_new.py renamed)
├── core/
│   ├── __init__.py
│   ├── command_router.py
│   ├── context_manager.py
│   ├── response_builder.py
│   └── server.py
├── handlers/
│   ├── __init__.py
│   ├── base_handler.py
│   ├── handler_registry.py
│   ├── animation/
│   ├── integrations/
│   ├── modeling/
│   ├── rendering/
│   ├── rigging/
│   └── scene/
└── utils/
    ├── __init__.py
    ├── cache.py
    ├── error_handler.py
    ├── logger.py
    └── validation.py
```

### Step 4: Install in Blender

1. **Open Blender**
2. Go to **Edit > Preferences > Add-ons**
3. **Search for "Blender MCP"**
4. **Enable** it (check the box)
5. You should see it in the list as "Interface: Blender MCP"

### Step 5: Verify Installation

1. **Restart Blender** (completely close and reopen)
2. **Check the console** - you should see:
   ```
   BlenderMCP: Modular system loaded successfully
   Rendering handlers imported successfully
   Sketchfab handlers imported successfully
   Rendering handlers registered
   Sketchfab handlers registered
   Registered 28 handlers  (or more)
   BlenderMCP: ✓ Render handlers registered
   BlenderMCP: ✓ Sketchfab handlers registered
   ```

## Quick Setup Script

I can create a script to do this automatically. Would you like me to create it?

## Alternative: Use Symbolic Link

If you want to keep files in the original location:

```bash
# Create the addon directory
mkdir -p ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp

# Create symbolic links
ln -s /Users/maghonemi/Desktop/blender-mcp-main/addon_new.py ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/__init__.py
ln -s /Users/maghonemi/Desktop/blender-mcp-main/core ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/
ln -s /Users/maghonemi/Desktop/blender-mcp-main/handlers ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/
ln -s /Users/maghonemi/Desktop/blender-mcp-main/utils ~/Library/Application\ Support/Blender/[version]/scripts/addons/blender_mcp/
```

## Why This Matters

- **Single file install**: Only 24 handlers (missing render & Sketchfab)
- **Directory install**: 28+ handlers (all features work)

The directory install allows Blender to find and import all the modules correctly.
