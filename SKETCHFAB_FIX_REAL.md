# Sketchfab Fix - The Real Issue

## Problem
Error: "Communication error with Blender: Unknown error from Blender"

## Root Cause
The MCP server client (`src/blender_mcp/server.py`) was looking for the error message in the wrong place:

**Wrong:**
```python
response.get("message")  # Looking at top level
```

**Correct:**
```python
response.get("error", {}).get("message")  # Looking in error object
```

## Error Response Format

The new handler system returns errors in this format:
```json
{
  "status": "error",
  "error": {
    "code": "API_ERROR",
    "message": "Sketchfab API key is not configured"
  }
}
```

But the client code was looking for:
```json
{
  "status": "error",
  "message": "..."  // Wrong location!
}
```

## Fix Applied

Updated `src/blender_mcp/server.py` to:
1. Check for error in both old and new formats
2. Extract message from `error.message` (new format)
3. Fall back to `message` (old format) for backward compatibility
4. Provide proper error message instead of "Unknown error from Blender"

## Files Modified
- `src/blender_mcp/server.py` - Fixed error message extraction

## Testing
After this fix, error messages from Blender handlers will be properly displayed instead of "Unknown error from Blender".
