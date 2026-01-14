# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

"""
Handler registry - imports and registers all handlers
"""

from core.command_router import command_router
from utils.logger import logger

# Scene handlers
from handlers.scene.scene_info import GetSceneInfoHandler
from handlers.scene.object_ops import (
    GetObjectInfoHandler,
    GetViewportScreenshotHandler,
    ExecuteCodeHandler
)

# Animation handlers
from handlers.animation.keyframes import (
    CreateKeyframeHandler,
    DeleteKeyframeHandler,
    GetKeyframesHandler,
    BatchKeyframesHandler
)
from handlers.animation.timeline import (
    SetCurrentFrameHandler,
    GetTimelineInfoHandler,
    SetFrameRangeHandler,
    PlaybackControlHandler
)
from handlers.animation.constraints import (
    AddConstraintHandler,
    ModifyConstraintHandler,
    RemoveConstraintHandler
)
from handlers.animation.shape_keys import (
    CreateShapeKeyHandler,
    SetShapeKeyValueHandler,
    GetShapeKeysHandler
)

# Rigging handlers
from handlers.rigging.armatures import (
    CreateArmatureHandler,
    GetArmatureInfoHandler
)
from handlers.rigging.bones import (
    CreateBoneHandler,
    GetBoneInfoHandler
)

# Modeling handlers
from handlers.modeling.mesh_edit import (
    CreatePrimitiveHandler,
    ExtrudeMeshHandler
)

def register_all_handlers():
    """Register all handlers with the command router"""
    logger.info("Registering all handlers...")
    
    # Scene handlers
    command_router.register_handler(GetSceneInfoHandler())
    command_router.register_handler(GetObjectInfoHandler())
    command_router.register_handler(GetViewportScreenshotHandler())
    command_router.register_handler(ExecuteCodeHandler())
    
    # Animation handlers
    command_router.register_handler(CreateKeyframeHandler())
    command_router.register_handler(DeleteKeyframeHandler())
    command_router.register_handler(GetKeyframesHandler())
    command_router.register_handler(BatchKeyframesHandler())
    command_router.register_handler(SetCurrentFrameHandler())
    command_router.register_handler(GetTimelineInfoHandler())
    command_router.register_handler(SetFrameRangeHandler())
    command_router.register_handler(PlaybackControlHandler())
    command_router.register_handler(AddConstraintHandler())
    command_router.register_handler(ModifyConstraintHandler())
    command_router.register_handler(RemoveConstraintHandler())
    command_router.register_handler(CreateShapeKeyHandler())
    command_router.register_handler(SetShapeKeyValueHandler())
    command_router.register_handler(GetShapeKeysHandler())
    
    # Rigging handlers
    command_router.register_handler(CreateArmatureHandler())
    command_router.register_handler(GetArmatureInfoHandler())
    command_router.register_handler(CreateBoneHandler())
    command_router.register_handler(GetBoneInfoHandler())
    
    # Modeling handlers
    command_router.register_handler(CreatePrimitiveHandler())
    command_router.register_handler(ExtrudeMeshHandler())
    
    logger.info(f"Registered {len(command_router.get_registered_commands())} handlers")
