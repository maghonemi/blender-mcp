# Setup Instructions - Modular System

## Important: Directory Structure Required

The new modular system **requires** the following directory structure in Blender's addon folder:

```
[Blender addons folder]/
├── addon_new.py (or addon.py)
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

## Quick Setup

### Option 1: Copy Entire Directory (Recommended)

1. Copy the entire `blender-mcp-main` directory to Blender's addons folder
2. Rename it to `blender_mcp` (remove spaces, use underscore)
3. Rename `addon_new.py` to `addon.py`

### Option 2: Copy Required Files

```bash
# Copy main addon file
cp addon_new.py "[Blender addons]/addon.py"

# Copy modular system directories
cp -r core "[Blender addons]/"
cp -r handlers "[Blender addons]/"
cp -r utils "[Blender addons]/"
```

## Verification

After copying, restart Blender and check the console:

**If modular system loads:**
```
BlenderMCP: Modular system loaded successfully
All handlers registered successfully
BlenderMCP addon registered (v2.0)
```

**If fallback mode (modules missing):**
```
BlenderMCP: Modular system not available (No module named 'core')
BlenderMCP: Using fallback server with basic functionality
BlenderMCP addon registered (v2.0)
```

## Testing

Once set up, run the test script:
```bash
python3 test_mcp_actions.py
```

You should see most commands passing (not just 2/11).

## Troubleshooting

### Only 2 commands work (get_scene_info, execute_code)

**Problem**: Modular system not loaded - only fallback server is active

**Solution**: 
1. Ensure `core/`, `handlers/`, and `utils/` directories are in the addon folder
2. Restart Blender completely
3. Check console for import errors

### "No module named 'core'"

**Problem**: Python can't find the core module

**Solution**:
1. Verify directories are in the same folder as `addon_new.py`
2. Check all `__init__.py` files exist
3. Restart Blender (clears Python cache)

---

**Status**: Setup complete after copying directories ✅
