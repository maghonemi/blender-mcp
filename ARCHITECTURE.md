# Blender MCP Architecture Plan

## Overview
This document outlines the architectural design for the enhanced Blender MCP addon, focusing on modularity, extensibility, and comprehensive Blender control.

---

## Directory Structure

```
blender-mcp/
├── addon.py                    # Main entry point (minimal)
├── core/
│   ├── __init__.py
│   ├── server.py              # Socket server implementation
│   ├── command_router.py      # Command routing and validation
│   ├── context_manager.py     # Blender context management
│   └── response_builder.py    # Standardized response formatting
├── handlers/
│   ├── __init__.py
│   ├── base_handler.py        # Base class for all handlers
│   ├── scene/
│   │   ├── __init__.py
│   │   ├── scene_info.py
│   │   ├── object_ops.py
│   │   └── collection_ops.py
│   ├── animation/
│   │   ├── __init__.py
│   │   ├── keyframes.py
│   │   ├── fcurves.py
│   │   ├── timeline.py
│   │   ├── constraints.py
│   │   └── shape_keys.py
│   ├── rigging/
│   │   ├── __init__.py
│   │   ├── armatures.py
│   │   ├── bones.py
│   │   └── weights.py
│   ├── modeling/
│   │   ├── __init__.py
│   │   ├── mesh_edit.py
│   │   ├── modifiers.py
│   │   ├── geometry_nodes.py
│   │   └── uv_mapping.py
│   ├── materials/
│   │   ├── __init__.py
│   │   ├── shaders.py
│   │   ├── textures.py
│   │   └── node_editor.py
│   ├── rendering/
│   │   ├── __init__.py
│   │   ├── render_settings.py
│   │   ├── cameras.py
│   │   ├── lighting.py
│   │   └── compositing.py
│   ├── physics/
│   │   ├── __init__.py
│   │   ├── rigid_body.py
│   │   ├── cloth.py
│   │   ├── fluid.py
│   │   └── particles.py
│   └── integrations/
│       ├── __init__.py
│       ├── polyhaven.py
│       ├── hyper3d.py
│       ├── sketchfab.py
│       └── hunyuan3d.py
├── utils/
│   ├── __init__.py
│   ├── validation.py          # Parameter validation
│   ├── context_helpers.py    # Context utilities
│   ├── error_handler.py      # Error handling utilities
│   ├── logger.py             # Logging system
│   └── cache.py              # Caching utilities
├── ui/
│   ├── __init__.py
│   ├── panel.py              # Main UI panel
│   ├── preferences.py        # Addon preferences
│   └── operators.py          # UI operators
└── tests/
    ├── __init__.py
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

## Core Components

### 1. Server (`core/server.py`)

**Responsibilities**:
- Socket server management
- Client connection handling
- Thread management
- Command reception and response sending

**Key Classes**:
```python
class BlenderMCPServer:
    def __init__(self, host='localhost', port=9876)
    def start(self)
    def stop(self)
    def _server_loop(self)
    def _handle_client(self, client)
```

### 2. Command Router (`core/command_router.py`)

**Responsibilities**:
- Command validation
- Handler lookup
- Parameter parsing
- Response routing

**Key Classes**:
```python
class CommandRouter:
    def __init__(self)
    def register_handler(self, command_type, handler)
    def route_command(self, command)
    def validate_command(self, command)
```

### 3. Base Handler (`handlers/base_handler.py`)

**Responsibilities**:
- Common handler functionality
- Error handling
- Context management
- Response formatting

**Key Classes**:
```python
class BaseHandler:
    def __init__(self, context_manager)
    def execute(self, command)
    def validate_params(self, params)
    def build_response(self, result, status="success")
    def handle_error(self, error)
```

### 4. Context Manager (`core/context_manager.py`)

**Responsibilities**:
- Blender context management
- Object lookup
- Scene state management
- Thread-safe context operations

**Key Classes**:
```python
class ContextManager:
    def get_object(self, name)
    def get_scene(self, name=None)
    def get_active_object(self)
    def get_selected_objects(self)
    def set_active_object(self, obj)
    def ensure_context(self, context_override)
```

---

## Handler Architecture

### Handler Registration

Handlers are registered using a decorator pattern:

```python
@register_handler("create_keyframe")
class KeyframeHandler(BaseHandler):
    def execute(self, command):
        params = command.get("params", {})
        # Implementation
        return self.build_response(result)
```

### Handler Interface

All handlers must implement:

```python
class HandlerInterface:
    def validate_params(self, params) -> bool
    def execute(self, command) -> dict
    def get_help(self) -> str
    def get_examples(self) -> list
```

---

## Command Protocol

### Request Format

```json
{
    "type": "command_name",
    "params": {
        "param1": "value1",
        "param2": "value2"
    },
    "context": {
        "scene": "Scene",
        "active_object": "ObjectName",
        "selected_objects": ["Obj1", "Obj2"]
    },
    "options": {
        "async": false,
        "timeout": 30
    }
}
```

### Response Format

```json
{
    "status": "success|error|partial",
    "result": {
        // Command-specific result
    },
    "warnings": [
        {
            "code": "WARNING_CODE",
            "message": "Warning message"
        }
    ],
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2"
    ],
    "context": {
        "scene": "Scene",
        "active_object": "ObjectName",
        "timestamp": "2025-01-01T00:00:00Z"
    },
    "metadata": {
        "execution_time": 0.123,
        "command_id": "uuid"
    }
}
```

---

## Error Handling System

### Error Codes

```python
class ErrorCode(Enum):
    # General
    INVALID_COMMAND = "INVALID_COMMAND"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    
    # Objects
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    INVALID_OBJECT_TYPE = "INVALID_OBJECT_TYPE"
    
    # Animation
    INVALID_FRAME = "INVALID_FRAME"
    INVALID_DATA_PATH = "INVALID_DATA_PATH"
    KEYFRAME_EXISTS = "KEYFRAME_EXISTS"
    
    # Rigging
    NO_ARMATURE = "NO_ARMATURE"
    BONE_NOT_FOUND = "BONE_NOT_FOUND"
    
    # Network
    CONNECTION_ERROR = "CONNECTION_ERROR"
    TIMEOUT = "TIMEOUT"
```

### Error Response Format

```json
{
    "status": "error",
    "error": {
        "code": "OBJECT_NOT_FOUND",
        "message": "Object 'Cube' not found in scene",
        "details": {
            "object_name": "Cube",
            "available_objects": ["Sphere", "Plane"]
        }
    },
    "suggestions": [
        "Check object name spelling",
        "Ensure object exists in current scene"
    ]
}
```

---

## Context Management

### Thread Safety

Blender operations must run in the main thread. The context manager ensures this:

```python
class ContextManager:
    def execute_in_main_thread(self, func, *args, **kwargs):
        """Execute function in Blender's main thread"""
        result = [None]
        exception = [None]
        
        def wrapper():
            try:
                result[0] = func(*args, **kwargs)
            except Exception as e:
                exception[0] = e
        
        bpy.app.timers.register(wrapper, first_interval=0.0)
        # Wait for execution...
        
        if exception[0]:
            raise exception[0]
        return result[0]
```

### Context Override

For operations requiring specific context:

```python
def with_context(context_override):
    """Decorator for context-specific operations"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with bpy.context.temp_override(**context_override):
                return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## Caching System

### Cache Strategy

```python
class CacheManager:
    def __init__(self):
        self._cache = {}
        self._ttl = {}
    
    def get(self, key, default=None):
        if key in self._cache:
            if time.time() < self._ttl.get(key, 0):
                return self._cache[key]
            else:
                del self._cache[key]
                del self._ttl[key]
        return default
    
    def set(self, key, value, ttl=60):
        self._cache[key] = value
        self._ttl[key] = time.time() + ttl
    
    def invalidate(self, pattern=None):
        # Invalidate cache entries
        pass
```

### Cacheable Operations

- Scene info (TTL: 5 seconds)
- Object info (TTL: 10 seconds)
- Material info (TTL: 30 seconds)
- F-curve data (TTL: 60 seconds)

---

## Validation System

### Parameter Validation

```python
class ParameterValidator:
    def validate(self, params, schema):
        """Validate parameters against schema"""
        errors = []
        
        for field, rules in schema.items():
            value = params.get(field)
            
            # Required check
            if rules.get("required") and value is None:
                errors.append(f"{field} is required")
                continue
            
            # Type check
            if value is not None:
                expected_type = rules.get("type")
                if not isinstance(value, expected_type):
                    errors.append(f"{field} must be {expected_type.__name__}")
                    continue
            
            # Custom validation
            validator = rules.get("validator")
            if validator:
                try:
                    validator(value)
                except Exception as e:
                    errors.append(f"{field}: {str(e)}")
        
        return errors
```

### Schema Example

```python
KEYFRAME_SCHEMA = {
    "object_name": {
        "type": str,
        "required": True,
        "validator": validate_object_exists
    },
    "data_path": {
        "type": str,
        "required": True,
        "validator": validate_data_path
    },
    "frame": {
        "type": int,
        "required": True,
        "validator": lambda x: x >= 1
    },
    "value": {
        "type": (int, float, list),
        "required": True
    }
}
```

---

## Logging System

### Logger Configuration

```python
class BlenderMCPLogger:
    def __init__(self):
        self.logger = logging.getLogger("BlenderMCP")
        self.setup_handlers()
    
    def setup_handlers(self):
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(
            os.path.join(bpy.app.tempdir, "blendermcp.log")
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
```

---

## Performance Optimization

### Lazy Loading

```python
class LazySceneInfo:
    def __init__(self):
        self._cache = None
        self._dirty = True
    
    def get(self):
        if self._dirty or self._cache is None:
            self._cache = self._compute_scene_info()
            self._dirty = False
        return self._cache
    
    def invalidate(self):
        self._dirty = True
```

### Batch Operations

```python
class BatchOperation:
    def __init__(self):
        self.operations = []
    
    def add(self, operation):
        self.operations.append(operation)
    
    def execute(self):
        # Execute all operations in single context
        with bpy.context.temp_override(...):
            results = []
            for op in self.operations:
                results.append(op.execute())
            return results
```

---

## Extension System

### Plugin Architecture

```python
class HandlerPlugin:
    def register_handlers(self, router):
        """Register custom handlers"""
        pass
    
    def get_metadata(self):
        """Return plugin metadata"""
        return {
            "name": "Plugin Name",
            "version": "1.0.0",
            "handlers": ["command1", "command2"]
        }
```

### Handler Discovery

```python
def discover_handlers():
    """Auto-discover handlers in handlers/ directory"""
    handlers = {}
    
    for module_name in os.listdir("handlers"):
        if module_name.endswith(".py"):
            module = importlib.import_module(f"handlers.{module_name}")
            if hasattr(module, "register_handlers"):
                module.register_handlers(handlers)
    
    return handlers
```

---

## Testing Architecture

### Test Structure

```python
class HandlerTestCase(unittest.TestCase):
    def setUp(self):
        # Setup test scene
        self.scene = bpy.context.scene
        self.test_object = self.create_test_object()
    
    def tearDown(self):
        # Cleanup
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
    
    def test_handler(self):
        # Test handler
        handler = KeyframeHandler(self.context_manager)
        result = handler.execute({
            "type": "create_keyframe",
            "params": {...}
        })
        self.assertEqual(result["status"], "success")
```

---

## Security Considerations

### Code Execution Safety

```python
class SafeCodeExecutor:
    ALLOWED_MODULES = ["bpy", "mathutils", "math"]
    BLOCKED_OPERATIONS = ["__import__", "eval", "exec", "open"]
    
    def execute(self, code):
        # Validate code
        if not self.is_safe(code):
            raise SecurityError("Unsafe code detected")
        
        # Execute in restricted environment
        return self._execute_safe(code)
```

### Input Validation

- All user inputs validated
- Object names sanitized
- File paths restricted
- API keys encrypted

---

## Migration Strategy

### Version Compatibility

```python
class VersionManager:
    def __init__(self):
        self.current_version = "2.0.0"
        self.supported_versions = ["1.0.0", "1.1.0", "2.0.0"]
    
    def migrate_command(self, command, from_version, to_version):
        """Migrate command format between versions"""
        # Migration logic
        pass
```

---

## Documentation Generation

### Auto-Documentation

```python
def generate_api_docs():
    """Generate API documentation from handler metadata"""
    docs = {}
    
    for handler_name, handler_class in handlers.items():
        docs[handler_name] = {
            "description": handler_class.__doc__,
            "parameters": handler_class.get_parameter_schema(),
            "examples": handler_class.get_examples()
        }
    
    return docs
```

---

## Implementation Phases

### Phase 1: Core Refactoring
- Split monolithic file
- Implement base architecture
- Create handler system
- Add validation framework

### Phase 2: Animation System
- Implement animation handlers
- Add F-curve support
- Timeline control
- Constraint management

### Phase 3: Advanced Features
- Rigging system
- Advanced modeling
- Rendering control
- Physics simulation

### Phase 4: Polish
- Performance optimization
- Comprehensive testing
- Documentation
- User experience improvements
