# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

"""
Sketchfab integration handlers
"""

from typing import Any, Dict
import bpy
import mathutils
import json
import tempfile
import os
import zipfile
from handlers.base_handler import BaseHandler
from utils.logger import logger

# Try to import requests, fallback to urllib if not available
REQUESTS_AVAILABLE = False
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    try:
        import urllib.request
        import urllib.parse
        import urllib.error
    except ImportError:
        pass


class GetSketchfabStatusHandler(BaseHandler):
    """Handler for getting Sketchfab integration status"""
    
    def get_command_name(self) -> str:
        return "get_sketchfab_status"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {}
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get the current status of Sketchfab integration"""
        if not REQUESTS_AVAILABLE:
            raise ValueError(
                "The 'requests' library is not available in Blender's Python environment. "
                "Please install it or use Blender's built-in Python with requests support."
            )
        
        enabled = bpy.context.scene.blendermcp_use_sketchfab
        api_key = bpy.context.scene.blendermcp_sketchfab_api_key

        # Test the API key if present
        if api_key:
            try:
                headers = {
                    "Authorization": f"Token {api_key}"
                }

                response = requests.get(
                    "https://api.sketchfab.com/v3/me",
                    headers=headers,
                    timeout=30
                )

                if response.status_code == 200:
                    user_data = response.json()
                    username = user_data.get("username", "Unknown user")
                    return {
                        "enabled": True,
                        "message": f"Sketchfab integration is enabled and ready to use. Logged in as: {username}"
                    }
                else:
                    return {
                        "enabled": False,
                        "message": f"Sketchfab API key seems invalid. Status code: {response.status_code}"
                    }
            except requests.exceptions.Timeout:
                return {
                    "enabled": False,
                    "message": "Timeout connecting to Sketchfab API. Check your internet connection."
                }
            except Exception as e:
                return {
                    "enabled": False,
                    "message": f"Error testing Sketchfab API key: {str(e)}"
                }

        if enabled and api_key:
            return {"enabled": True, "message": "Sketchfab integration is enabled and ready to use."}
        elif enabled and not api_key:
            return {
                "enabled": False,
                "message": """Sketchfab integration is currently enabled, but API key is not given. To enable it:
                            1. In the 3D Viewport, find the BlenderMCP panel in the sidebar (press N if hidden)
                            2. Keep the 'Use Sketchfab' checkbox checked
                            3. Enter your Sketchfab API Key
                            4. Restart the connection to Claude"""
            }
        else:
            return {
                "enabled": False,
                "message": """Sketchfab integration is currently disabled. To enable it:
                            1. In the 3D Viewport, find the BlenderMCP panel in the sidebar (press N if hidden)
                            2. Check the 'Use assets from Sketchfab' checkbox
                            3. Enter your Sketchfab API Key
                            4. Restart the connection to Claude"""
            }


class SearchSketchfabModelsHandler(BaseHandler):
    """Handler for searching Sketchfab models"""
    
    def get_command_name(self) -> str:
        return "search_sketchfab_models"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "query": {
                "type": str,
                "required": True
            },
            "categories": {
                "type": str,
                "required": False
            },
            "count": {
                "type": int,
                "required": False
            },
            "downloadable": {
                "type": bool,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Search for models on Sketchfab - matches original addon.py behavior"""
        try:
            api_key = bpy.context.scene.blendermcp_sketchfab_api_key
            if not api_key:
                return {"error": "Sketchfab API key is not configured"}

            query = params["query"]
            categories = params.get("categories")
            count = params.get("count", 20)
            downloadable = params.get("downloadable", True)

            # Build search parameters with exact fields from Sketchfab API docs
            search_params = {
                "type": "models",
                "q": query,
                "count": count,
                "downloadable": downloadable,
                "archives_flavours": False
            }

            if categories:
                search_params["categories"] = categories

            # Make API request to Sketchfab search endpoint
            # The proper format according to Sketchfab API docs for API key auth
            headers = {
                "Authorization": f"Token {api_key}"
            }

            # Use the search endpoint as specified in the API documentation
            response = requests.get(
                "https://api.sketchfab.com/v3/search",
                headers=headers,
                params=search_params,
                timeout=30  # Add timeout of 30 seconds
            )

            if response.status_code == 401:
                return {"error": "Authentication failed (401). Check your API key."}

            if response.status_code != 200:
                return {"error": f"API request failed with status code {response.status_code}"}

            response_data = response.json()

            # Safety check on the response structure
            if response_data is None:
                return {"error": "Received empty response from Sketchfab API"}

            # Handle 'results' potentially missing from response
            results = response_data.get("results", [])
            if not isinstance(results, list):
                return {"error": f"Unexpected response format from Sketchfab API: {response_data}"}

            return response_data

        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Check your internet connection."}
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON response from Sketchfab API: {str(e)}"}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}


class GetSketchfabModelPreviewHandler(BaseHandler):
    """Handler for getting Sketchfab model preview"""
    
    def get_command_name(self) -> str:
        return "get_sketchfab_model_preview"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "uid": {
                "type": str,
                "required": True
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Get thumbnail preview image of a Sketchfab model"""
        if not REQUESTS_AVAILABLE:
            raise ValueError(
                "The 'requests' library is not available in Blender's Python environment. "
                "Please install it or use Blender's built-in Python with requests support."
            )
        
        try:
            import base64
            
            api_key = bpy.context.scene.blendermcp_sketchfab_api_key
            if not api_key:
                raise ValueError("Sketchfab API key is not configured")

            uid = params["uid"]
            headers = {"Authorization": f"Token {api_key}"}
            
            # Get model info which includes thumbnails
            response = requests.get(
                f"https://api.sketchfab.com/v3/models/{uid}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 401:
                raise ValueError("Authentication failed (401). Check your API key.")
            
            if response.status_code == 404:
                raise ValueError(f"Model not found: {uid}")
            
            if response.status_code != 200:
                raise ValueError(f"Failed to get model info: {response.status_code}")
            
            data = response.json()
            thumbnails = data.get("thumbnails", {}).get("images", [])
            
            if not thumbnails:
                raise ValueError("No thumbnail available for this model")
            
            # Find a suitable thumbnail (prefer medium size ~640px)
            selected_thumbnail = None
            for thumb in thumbnails:
                width = thumb.get("width", 0)
                if 400 <= width <= 800:
                    selected_thumbnail = thumb
                    break
            
            # Fallback to the first available thumbnail
            if not selected_thumbnail:
                selected_thumbnail = thumbnails[0]
            
            thumbnail_url = selected_thumbnail.get("url")
            if not thumbnail_url:
                raise ValueError("Thumbnail URL not found")
            
            # Download the thumbnail image
            img_response = requests.get(thumbnail_url, timeout=30)
            if img_response.status_code != 200:
                raise ValueError(f"Failed to download thumbnail: {img_response.status_code}")
            
            # Encode image as base64
            image_data = base64.b64encode(img_response.content).decode('ascii')
            
            # Determine format from content type or URL
            content_type = img_response.headers.get("Content-Type", "")
            if "png" in content_type or thumbnail_url.endswith(".png"):
                img_format = "png"
            else:
                img_format = "jpeg"
            
            # Get additional model info for context
            model_name = data.get("name", "Unknown")
            author = data.get("user", {}).get("username", "Unknown")
            
            return {
                "success": True,
                "image_data": image_data,
                "format": img_format,
                "model_name": model_name,
                "author": author,
                "uid": uid,
                "thumbnail_width": selected_thumbnail.get("width"),
                "thumbnail_height": selected_thumbnail.get("height")
            }
            
        except requests.exceptions.Timeout:
            raise ValueError("Request timed out. Check your internet connection.")
        except Exception as e:
            logger.exception(f"Error getting Sketchfab preview: {str(e)}")
            raise


class DownloadSketchfabModelHandler(BaseHandler):
    """Handler for downloading Sketchfab models"""
    
    def get_command_name(self) -> str:
        return "download_sketchfab_model"
    
    def get_parameter_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "uid": {
                "type": str,
                "required": True
            },
            "normalize_size": {
                "type": bool,
                "required": False
            },
            "target_size": {
                "type": float,
                "required": False
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Any:
        """Download and import a Sketchfab model"""
        if not REQUESTS_AVAILABLE:
            raise ValueError(
                "The 'requests' library is not available in Blender's Python environment. "
                "Please install it or use Blender's built-in Python with requests support."
            )
        
        try:
            api_key = bpy.context.scene.blendermcp_sketchfab_api_key
            if not api_key:
                raise ValueError("Sketchfab API key is not configured")

            uid = params["uid"]
            normalize_size = params.get("normalize_size", False)
            target_size = params.get("target_size", 1.0)

            headers = {
                "Authorization": f"Token {api_key}"
            }

            # Request download URL
            download_endpoint = f"https://api.sketchfab.com/v3/models/{uid}/download"
            response = requests.get(
                download_endpoint,
                headers=headers,
                timeout=30
            )

            if response.status_code == 401:
                raise ValueError("Authentication failed (401). Check your API key.")

            if response.status_code != 200:
                raise ValueError(f"Download request failed with status code {response.status_code}")

            data = response.json()

            if data is None:
                raise ValueError("Received empty response from Sketchfab API for download request")

            # Get the GLB download URL
            glb_url = data.get("glb", {}).get("url")
            if not glb_url:
                # Try alternative formats
                formats = data.get("formats", [])
                for fmt in formats:
                    if fmt.get("formatType") == "glb":
                        glb_url = fmt.get("root", {}).get("url")
                        break
                
                if not glb_url:
                    raise ValueError("No GLB download URL available for this model")

            # Download the GLB file
            logger.info(f"Downloading GLB from: {glb_url}")
            glb_response = requests.get(glb_url, timeout=120, stream=True)
            
            if glb_response.status_code != 200:
                raise ValueError(f"Failed to download GLB file: {glb_response.status_code}")

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".glb") as temp_file:
                temp_file.write(glb_response.content)
                temp_file_path = temp_file.name

            try:
                # Import the GLB file
                bpy.ops.import_scene.gltf(filepath=temp_file_path)
                
                # Get the imported objects
                imported_objects = [obj for obj in bpy.context.selected_objects]
                
                if not imported_objects:
                    raise ValueError("No objects were imported from the GLB file")

                # Normalize size if requested
                if normalize_size:
                    # Calculate bounding box
                    all_coords = []
                    for obj in imported_objects:
                        if obj.type == 'MESH':
                            for vertex in obj.bound_box:
                                world_vertex = obj.matrix_world @ mathutils.Vector(vertex)
                                all_coords.append(world_vertex)
                    
                    if all_coords:
                        min_coords = [min(coord[i] for coord in all_coords) for i in range(3)]
                        max_coords = [max(coord[i] for coord in all_coords) for i in range(3)]
                        dimensions = [max_coords[i] - min_coords[i] for i in range(3)]
                        max_dimension = max(dimensions)
                        
                        if max_dimension > 0:
                            scale_factor = target_size / max_dimension
                            for obj in imported_objects:
                                obj.scale = [scale_factor, scale_factor, scale_factor]

                return {
                    "success": True,
                    "uid": uid,
                    "imported_objects": [obj.name for obj in imported_objects],
                    "object_count": len(imported_objects)
                }
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                except:
                    pass

        except requests.exceptions.Timeout:
            raise ValueError("Request timed out. Check your internet connection.")
        except Exception as e:
            logger.exception(f"Error downloading Sketchfab model: {str(e)}")
            raise
