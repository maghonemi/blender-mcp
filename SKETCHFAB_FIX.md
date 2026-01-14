# Sketchfab Handler Fix

## Issue
Error: "Communication error with Blender: Unknown error from Blender" when searching Sketchfab models.

## Root Cause
The `requests` library may not be available in Blender's Python environment, causing an ImportError that was being caught but not properly reported.

## Fix Applied

### 1. Added Import Error Handling
- Check if `requests` is available before using it
- Provide clear error message if `requests` is missing
- Added `REQUESTS_AVAILABLE` flag to track availability

### 2. Improved Error Reporting
- Added specific error handling for network errors
- Better exception chaining to preserve original error context
- More descriptive error messages

### 3. Changes Made
- Added `REQUESTS_AVAILABLE` check in all Sketchfab handlers
- Improved error messages to indicate missing `requests` library
- Added `requests.exceptions.RequestException` handling

## Files Modified
- `handlers/integrations/sketchfab.py`

## Testing
After this fix, if `requests` is not available, you'll get a clear error message:
```
The 'requests' library is not available in Blender's Python environment. 
Please install it or use Blender's built-in Python with requests support.
```

## Solution Options

### Option 1: Install requests in Blender's Python
```bash
# Find Blender's Python executable
# Usually at: /path/to/blender/3.x/python/bin/python3.x

# Install requests
/path/to/blender/3.x/python/bin/python3.x -m pip install requests
```

### Option 2: Use Blender's built-in urllib (Future Enhancement)
We could modify the handlers to use `urllib` as a fallback, but this would require significant refactoring.

### Option 3: Bundle requests with addon
Include `requests` as part of the addon package (more complex).

## Next Steps
1. Test the error message to confirm `requests` is the issue
2. If confirmed, install `requests` in Blender's Python environment
3. Re-test Sketchfab functionality
