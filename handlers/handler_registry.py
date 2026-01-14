# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

"""
Handler registry - imports and registers all handlers
Version: 2.1.0 - Added movie production workflow handlers
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

# Animation handlers - Core
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

# Animation handlers - Advanced (F-curves, Actions, Baking)
from handlers.animation.fcurves import (
    GetFCurvesHandler,
    SetFCurveInterpolationHandler,
    SetFCurveHandlesHandler,
    AddFCurveModifierHandler,
    RemoveFCurveModifierHandler,
    SmoothFCurveHandler
)
from handlers.animation.actions import (
    CreateActionHandler,
    AssignActionHandler,
    GetActionInfoHandler,
    ListActionsHandler,
    DuplicateActionHandler,
    DeleteActionHandler,
    PushDownActionHandler,
    GetObjectActionHandler
)
from handlers.animation.baking import (
    BakeAnimationHandler,
    BakeArmatureAnimationHandler,
    SampleAnimationHandler,
    CleanKeyframesHandler
)

# Rigging handlers - Core
from handlers.rigging.armatures import (
    CreateArmatureHandler,
    GetArmatureInfoHandler
)
from handlers.rigging.bones import (
    CreateBoneHandler,
    GetBoneInfoHandler,
    TransformBoneHandler,
    DeleteBoneHandler,
    SetBoneParentHandler,
    DuplicateBoneHandler
)

# Rigging handlers - Advanced (Weights, Pose, Constraints, Templates)
from handlers.rigging.weights import (
    ParentToArmatureHandler,
    CreateVertexGroupHandler,
    SetVertexWeightsHandler,
    GetVertexWeightsHandler,
    NormalizeWeightsHandler,
    TransferWeightsHandler,
    GetVertexGroupsHandler
)
from handlers.rigging.pose import (
    SetBonePoseHandler,
    GetBonePoseHandler,
    ClearPoseHandler,
    ApplyPoseAsRestHandler,
    CopyPoseHandler,
    GetAllBonePosesHandler
)
from handlers.rigging.bone_constraints import (
    AddBoneConstraintHandler,
    SetupIKChainHandler,
    ModifyBoneConstraintHandler,
    RemoveBoneConstraintHandler,
    GetBoneConstraintsHandler
)
from handlers.rigging.templates import (
    CreateHumanoidRigHandler,
    CreateSimpleRigHandler,
    MirrorBonesHandler
)

# Modeling handlers
from handlers.modeling.mesh_edit import (
    CreatePrimitiveHandler,
    ExtrudeMeshHandler
)

# Rendering handlers - Core settings
RENDERING_AVAILABLE = False
try:
    from handlers.rendering.render_settings import (
        SetRenderOutputHandler,
        GetRenderSettingsHandler
    )
    RENDERING_AVAILABLE = True
    logger.info("Rendering settings handlers imported successfully")
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

# Rendering handlers - Operations (render, engine, resolution, samples)
RENDER_OPS_AVAILABLE = False
try:
    from handlers.rendering.render_operations import (
        SetRenderEngineHandler,
        SetRenderResolutionHandler,
        SetRenderSamplesHandler,
        RenderImageHandler,
        RenderAnimationHandler,
        GetRenderProgressHandler
    )
    RENDER_OPS_AVAILABLE = True
    logger.info("Render operations handlers imported successfully")
except ImportError as e:
    RENDER_OPS_AVAILABLE = False
    logger.warning(f"Could not import render operations handlers: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    RENDER_OPS_AVAILABLE = False
    logger.error(f"Error importing render operations handlers: {e}")
    import traceback
    traceback.print_exc()

# Camera handlers
CAMERAS_AVAILABLE = False
try:
    from handlers.rendering.cameras import (
        CreateCameraHandler,
        SetActiveCameraHandler,
        SetCameraPropertiesHandler,
        SetCameraDOFHandler,
        GetCameraInfoHandler,
        AddCameraConstraintHandler
    )
    CAMERAS_AVAILABLE = True
    logger.info("Camera handlers imported successfully")
except ImportError as e:
    CAMERAS_AVAILABLE = False
    logger.warning(f"Could not import camera handlers: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    CAMERAS_AVAILABLE = False
    logger.error(f"Error importing camera handlers: {e}")
    import traceback
    traceback.print_exc()

# Lighting handlers
LIGHTING_AVAILABLE = False
try:
    from handlers.rendering.lighting import (
        CreateLightHandler,
        SetLightPropertiesHandler,
        GetLightInfoHandler,
        CreateThreePointLightingHandler,
        SetWorldLightingHandler
    )
    LIGHTING_AVAILABLE = True
    logger.info("Lighting handlers imported successfully")
except ImportError as e:
    LIGHTING_AVAILABLE = False
    logger.warning(f"Could not import lighting handlers: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    LIGHTING_AVAILABLE = False
    logger.error(f"Error importing lighting handlers: {e}")
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

    # Animation handlers - Core
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

    # Animation handlers - F-curves
    command_router.register_handler(GetFCurvesHandler())
    command_router.register_handler(SetFCurveInterpolationHandler())
    command_router.register_handler(SetFCurveHandlesHandler())
    command_router.register_handler(AddFCurveModifierHandler())
    command_router.register_handler(RemoveFCurveModifierHandler())
    command_router.register_handler(SmoothFCurveHandler())

    # Animation handlers - Actions
    command_router.register_handler(CreateActionHandler())
    command_router.register_handler(AssignActionHandler())
    command_router.register_handler(GetActionInfoHandler())
    command_router.register_handler(ListActionsHandler())
    command_router.register_handler(DuplicateActionHandler())
    command_router.register_handler(DeleteActionHandler())
    command_router.register_handler(PushDownActionHandler())
    command_router.register_handler(GetObjectActionHandler())

    # Animation handlers - Baking
    command_router.register_handler(BakeAnimationHandler())
    command_router.register_handler(BakeArmatureAnimationHandler())
    command_router.register_handler(SampleAnimationHandler())
    command_router.register_handler(CleanKeyframesHandler())

    # Rigging handlers - Core
    command_router.register_handler(CreateArmatureHandler())
    command_router.register_handler(GetArmatureInfoHandler())
    command_router.register_handler(CreateBoneHandler())
    command_router.register_handler(GetBoneInfoHandler())
    command_router.register_handler(TransformBoneHandler())
    command_router.register_handler(DeleteBoneHandler())
    command_router.register_handler(SetBoneParentHandler())
    command_router.register_handler(DuplicateBoneHandler())

    # Rigging handlers - Weights
    command_router.register_handler(ParentToArmatureHandler())
    command_router.register_handler(CreateVertexGroupHandler())
    command_router.register_handler(SetVertexWeightsHandler())
    command_router.register_handler(GetVertexWeightsHandler())
    command_router.register_handler(NormalizeWeightsHandler())
    command_router.register_handler(TransferWeightsHandler())
    command_router.register_handler(GetVertexGroupsHandler())

    # Rigging handlers - Pose
    command_router.register_handler(SetBonePoseHandler())
    command_router.register_handler(GetBonePoseHandler())
    command_router.register_handler(ClearPoseHandler())
    command_router.register_handler(ApplyPoseAsRestHandler())
    command_router.register_handler(CopyPoseHandler())
    command_router.register_handler(GetAllBonePosesHandler())

    # Rigging handlers - Bone Constraints
    command_router.register_handler(AddBoneConstraintHandler())
    command_router.register_handler(SetupIKChainHandler())
    command_router.register_handler(ModifyBoneConstraintHandler())
    command_router.register_handler(RemoveBoneConstraintHandler())
    command_router.register_handler(GetBoneConstraintsHandler())

    # Rigging handlers - Templates
    command_router.register_handler(CreateHumanoidRigHandler())
    command_router.register_handler(CreateSimpleRigHandler())
    command_router.register_handler(MirrorBonesHandler())

    # Modeling handlers
    command_router.register_handler(CreatePrimitiveHandler())
    command_router.register_handler(ExtrudeMeshHandler())

    # Rendering handlers - Core settings
    if RENDERING_AVAILABLE:
        try:
            command_router.register_handler(SetRenderOutputHandler())
            command_router.register_handler(GetRenderSettingsHandler())
            logger.info("Rendering settings handlers registered")
        except Exception as e:
            logger.error(f"Could not register rendering handlers: {e}")
            import traceback
            traceback.print_exc()
    else:
        logger.warning("Rendering settings handlers not available - skipping registration")

    # Rendering handlers - Operations
    if RENDER_OPS_AVAILABLE:
        try:
            command_router.register_handler(SetRenderEngineHandler())
            command_router.register_handler(SetRenderResolutionHandler())
            command_router.register_handler(SetRenderSamplesHandler())
            command_router.register_handler(RenderImageHandler())
            command_router.register_handler(RenderAnimationHandler())
            command_router.register_handler(GetRenderProgressHandler())
            logger.info("Render operations handlers registered")
        except Exception as e:
            logger.error(f"Could not register render operations handlers: {e}")
            import traceback
            traceback.print_exc()
    else:
        logger.warning("Render operations handlers not available - skipping registration")

    # Camera handlers
    if CAMERAS_AVAILABLE:
        try:
            command_router.register_handler(CreateCameraHandler())
            command_router.register_handler(SetActiveCameraHandler())
            command_router.register_handler(SetCameraPropertiesHandler())
            command_router.register_handler(SetCameraDOFHandler())
            command_router.register_handler(GetCameraInfoHandler())
            command_router.register_handler(AddCameraConstraintHandler())
            logger.info("Camera handlers registered")
        except Exception as e:
            logger.error(f"Could not register camera handlers: {e}")
            import traceback
            traceback.print_exc()
    else:
        logger.warning("Camera handlers not available - skipping registration")

    # Lighting handlers
    if LIGHTING_AVAILABLE:
        try:
            command_router.register_handler(CreateLightHandler())
            command_router.register_handler(SetLightPropertiesHandler())
            command_router.register_handler(GetLightInfoHandler())
            command_router.register_handler(CreateThreePointLightingHandler())
            command_router.register_handler(SetWorldLightingHandler())
            logger.info("Lighting handlers registered")
        except Exception as e:
            logger.error(f"Could not register lighting handlers: {e}")
            import traceback
            traceback.print_exc()
    else:
        logger.warning("Lighting handlers not available - skipping registration")

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
