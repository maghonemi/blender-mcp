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
from handlers.rigging.skinning import (
    ParentToArmatureHandler,
    AutoWeightAssignHandler
)
from handlers.rigging.auto_rig import (
    RigHandHandler,
    RigBodyHandler
)

# Modeling handlers
from handlers.modeling.mesh_edit import (
    CreatePrimitiveHandler,
    ExtrudeMeshHandler
)

# Rendering handlers
RENDERING_AVAILABLE = False
try:
    from handlers.rendering.render_settings import (
        SetRenderOutputHandler,
        GetRenderSettingsHandler
    )
    RENDERING_AVAILABLE = True
    logger.info("Rendering handlers imported successfully")
except ImportError as e:
    RENDERING_AVAILABLE = False
    logger.warning(f"Could not import rendering handlers: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    RENDERING_AVAILABLE = False
    logger.error(f"Error importing rendering handlers: {e}")
    import traceback
    traceback.print_exc()

# Integration handlers (conditionally imported)
SKETCHFAB_AVAILABLE = False
try:
    from handlers.integrations.sketchfab import (
        GetSketchfabStatusHandler,
        SearchSketchfabModelsHandler,
        GetSketchfabModelPreviewHandler,
        DownloadSketchfabModelHandler
    )
    SKETCHFAB_AVAILABLE = True
    logger.info("Sketchfab handlers imported successfully")
except ImportError as e:
    SKETCHFAB_AVAILABLE = False
    logger.warning(f"Could not import Sketchfab handlers: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    SKETCHFAB_AVAILABLE = False
    logger.error(f"Error importing Sketchfab handlers: {e}")
    import traceback
    traceback.print_exc()

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
    command_router.register_handler(ParentToArmatureHandler())
    command_router.register_handler(AutoWeightAssignHandler())
    command_router.register_handler(RigHandHandler())
    command_router.register_handler(RigBodyHandler())
    
    # Modeling handlers
    command_router.register_handler(CreatePrimitiveHandler())
    command_router.register_handler(ExtrudeMeshHandler())
    
    # Rendering handlers
    if RENDERING_AVAILABLE:
        try:
            command_router.register_handler(SetRenderOutputHandler())
            command_router.register_handler(GetRenderSettingsHandler())
            logger.info("Rendering handlers registered")
        except Exception as e:
            logger.error(f"Could not register rendering handlers: {e}")
            import traceback
            traceback.print_exc()
    else:
        logger.warning("Rendering handlers not available - skipping registration")
    
    # Integration handlers (always register, but handlers check enablement internally)
    if SKETCHFAB_AVAILABLE:
        try:
            command_router.register_handler(GetSketchfabStatusHandler())
            command_router.register_handler(SearchSketchfabModelsHandler())
            command_router.register_handler(GetSketchfabModelPreviewHandler())
            command_router.register_handler(DownloadSketchfabModelHandler())
            logger.info("Sketchfab handlers registered")
        except Exception as e:
            logger.warning(f"Could not register Sketchfab handlers: {e}")
    
    logger.info(f"Registered {len(command_router.get_registered_commands())} handlers")
