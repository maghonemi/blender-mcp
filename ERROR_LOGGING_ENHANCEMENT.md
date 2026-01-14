# MCP Server Error Logging Enhancement

## Summary
Enhanced error logging throughout the MCP server to capture detailed error information for debugging.

## Changes Made

### 1. Enhanced Command Execution Logging (`core/server.py`)

**Before:**
- Basic error logging
- Limited context about commands

**After:**
- Logs command type before execution
- Logs response status (success/error)
- Logs detailed error information including error codes
- Logs when responses are sent successfully
- Logs send failures with context

**Example logs:**
```
DEBUG - Executing command 'search_sketchfab_models' from ('127.0.0.1', 54321)
ERROR - Command 'search_sketchfab_models' failed: API_ERROR - Sketchfab API key is not configured
DEBUG - Response sent for command 'search_sketchfab_models' to ('127.0.0.1', 54321)
```

### 2. Enhanced Command Validation Logging

- Logs invalid command types with details
- Logs JSON parsing errors with partial content
- Logs command routing attempts

### 3. Enhanced Network Error Logging

- Logs incomplete JSON with buffer size
- Logs buffer content when too large
- Logs receive errors with full exception details
- Logs connection errors with context

### 4. Enhanced Command Router Logging (`core/command_router.py`)

- Logs command type when routing fails
- Includes full exception traceback
- Better error context

## Log Locations

### Console Output
All errors are logged to Blender's console with timestamps:
```
13:47:57 - BlenderMCP - ERROR - Command 'search_sketchfab_models' failed: API_ERROR - ...
```

### Log Files
Detailed logs are saved to:
```
[Blender temp directory]/blendermcp/blendermcp_YYYYMMDD.log
```

Example path on macOS:
```
~/Library/Application Support/Blender/5.0/temp/blendermcp/blendermcp_20250115.log
```

## Log Levels

- **DEBUG**: Detailed execution flow, command routing, response sending
- **INFO**: Normal operations, connections, disconnections
- **WARNING**: Non-critical issues (send failures, incomplete data)
- **ERROR**: Command failures, execution errors, routing errors
- **CRITICAL**: Fatal errors that stop the server

## What Gets Logged

### Command Execution
- Command type and source address
- Response status (success/error)
- Error codes and messages
- Response send status

### Network Operations
- Connection/disconnection events
- Data receive errors
- Send failures
- Buffer size issues
- JSON parsing errors

### Errors
- Full exception tracebacks
- Error context (command type, address)
- Error codes and messages
- Suggestions for resolution

## Benefits

1. **Better Debugging**: Full context about what went wrong
2. **Error Tracking**: All errors logged with timestamps
3. **Performance Monitoring**: Can track command execution times
4. **Troubleshooting**: Detailed logs help identify issues quickly

## Viewing Logs

### In Blender Console
- Run Blender from terminal: `/Applications/Blender.app/Contents/MacOS/Blender`
- Or use: Window → Toggle System Console

### In Log Files
```bash
# Find log directory
ls ~/Library/Application\ Support/Blender/*/temp/blendermcp/

# View latest log
tail -f ~/Library/Application\ Support/Blender/5.0/temp/blendermcp/blendermcp_*.log
```

## Example Error Log

```
2025-01-15 13:47:57 - BlenderMCP - ERROR - Command 'search_sketchfab_models' failed: API_ERROR - Sketchfab API key is not configured
2025-01-15 13:47:57 - BlenderMCP - ERROR - Exception routing command 'search_sketchfab_models': Network error: Connection timeout
Traceback (most recent call last):
  File "core/command_router.py", line 82, in route_command
    return handler.handle(command)
  ...
```

## Files Modified
- `core/server.py` - Enhanced error logging throughout
- `core/command_router.py` - Enhanced routing error logging
