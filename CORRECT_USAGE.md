# ✅ Correct MCP Server Usage

## How It Works

1. **Install the addon in Blender** (you've done this ✅)
2. **Enable the addon** in Blender Preferences
3. **Start the server from Blender UI** (click "Connect to MCP server")
4. **External tools connect** to the server on port 9876

## Current Setup

You're doing it correctly! The workflow is:

```
Blender (with addon) → MCP Server (port 9876) ← Test Scripts/Claude
```

## Why Tests Are Still Failing

The errors suggest Blender is still using **old cached code**. This happens because:

1. Python caches imported modules
2. Even if files are updated, Blender may use cached versions
3. **Full Blender restart is required** to clear cache

## Solution: Force Reload

### Option 1: Full Restart (Recommended)
1. **Completely quit Blender** (Cmd+Q / Alt+F4)
2. **Restart Blender**
3. **Re-enable addon**
4. **Start server**
5. **Run tests**

### Option 2: Clear Python Cache
If you can't restart, try:
1. In Blender console, run:
   ```python
   import sys
   # Remove cached modules
   modules_to_remove = [k for k in sys.modules.keys() if 'handlers' in k or 'core' in k]
   for mod in modules_to_remove:
       del sys.modules[mod]
   ```
2. Then disable and re-enable the addon

## Verify New Code Is Loaded

After restart, check Blender console for:
- No import errors
- "All handlers registered successfully"
- Handler version 2.0.2 (if logged)

## Test Connection

```bash
# Check if server is running
python3 check_server.py

# Run full test suite
python3 test_all_commands.py
```

---

**Your setup is correct!** The issue is just Python module caching. A full Blender restart should fix it.
