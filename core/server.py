# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import json
import socket
import threading
import time
import traceback
import os
from datetime import datetime
import bpy
from core.command_router import command_router
from utils.logger import logger

class BlenderMCPServer:
    """Socket server for Blender MCP communication"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None
        self.server_thread = None
        self.active_clients = []
    
    def start(self):
        """Start the MCP server"""
        if self.running:
            logger.warning("Server is already running")
            return
        
        self.running = True
        
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)  # Allow multiple connections
            
            # Start server thread
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            logger.info(f"BlenderMCP server started on {self.host}:{self.port}")
            # Log file location
            try:
                log_dir = os.path.join(bpy.app.tempdir, "blendermcp")
                log_file = os.path.join(log_dir, f"blendermcp_{datetime.now().strftime('%Y%m%d')}.log")
                logger.info(f"Error logs saved to: {log_file}")
                print(f"BlenderMCP: Error logs saved to: {log_file}")
            except:
                pass
        except Exception as e:
            logger.error(f"Failed to start server: {str(e)}")
            self.stop()
            raise
    
    def stop(self):
        """Stop the MCP server"""
        self.running = False
        
        # Close all active client connections
        for client in self.active_clients[:]:
            try:
                client.close()
            except:
                pass
        self.active_clients.clear()
        
        # Close socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        # Wait for thread to finish
        if self.server_thread:
            try:
                if self.server_thread.is_alive():
                    self.server_thread.join(timeout=2.0)
            except:
                pass
            self.server_thread = None
        
        logger.info("BlenderMCP server stopped")
    
    def _server_loop(self):
        """Main server loop in a separate thread"""
        logger.info("Server thread started")
        if self.socket:
            self.socket.settimeout(1.0)  # Timeout to allow for stopping
        
        while self.running:
            try:
                # Accept new connection
                try:
                    if self.socket:
                        client, address = self.socket.accept()
                        logger.info(f"Connected to client: {address}")
                        
                        # Handle client in a separate thread
                        client_thread = threading.Thread(
                            target=self._handle_client,
                            args=(client, address)
                        )
                        client_thread.daemon = True
                        client_thread.start()
                except socket.timeout:
                    # Just check running condition
                    continue
                except Exception as e:
                    logger.error(f"Error accepting connection: {str(e)}")
                    logger.exception("Accept connection error details:")
                    time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error in server loop: {str(e)}")
                logger.exception("Server loop error details:")
                if not self.running:
                    break
                time.sleep(0.5)
        
        logger.info("Server thread stopped")
    
    def _handle_client(self, client, address):
        """Handle connected client"""
        logger.info(f"Client handler started for {address}")
        self.active_clients.append(client)
        client.settimeout(None)  # No timeout
        buffer = b''
        
        try:
            while self.running:
                # Receive data
                try:
                    data = client.recv(8192)
                    if not data:
                        logger.info(f"Client {address} disconnected")
                        break
                    
                    buffer += data
                    try:
                        # Try to parse command
                        command = json.loads(buffer.decode('utf-8'))
                        buffer = b''
                        
                        # Execute command in Blender's main thread
                        def execute_wrapper():
                            command_type = command.get("type", "unknown") if isinstance(command, dict) else "unknown"
                            try:
                                logger.debug(f"Executing command '{command_type}' from {address}")
                                response = self.execute_command(command)
                                
                                # Log response status
                                response_status = response.get("status", "unknown")
                                if response_status == "error":
                                    error_info = response.get("error", {})
                                    logger.error(
                                        f"Command '{command_type}' failed: {error_info.get('code', 'UNKNOWN')} - "
                                        f"{error_info.get('message', 'No message')}"
                                    )
                                else:
                                    logger.debug(f"Command '{command_type}' succeeded")
                                
                                response_json = json.dumps(response)
                                try:
                                    client.sendall(response_json.encode('utf-8'))
                                    logger.debug(f"Response sent for command '{command_type}' to {address}")
                                except Exception as e:
                                    logger.error(f"Failed to send response to {address} for command '{command_type}': {str(e)}")
                                    logger.exception("Send error details:")
                            except Exception as e:
                                logger.error(f"Exception executing command '{command_type}' from {address}: {str(e)}")
                                logger.exception("Command execution error details:")
                                try:
                                    error_response = {
                                        "status": "error",
                                        "error": {
                                            "code": "EXECUTION_ERROR",
                                            "message": str(e)
                                        }
                                    }
                                    client.sendall(json.dumps(error_response).encode('utf-8'))
                                    logger.debug(f"Error response sent to {address}")
                                except Exception as send_error:
                                    logger.error(f"Failed to send error response to {address}: {str(send_error)}")
                            return None
                        
                        # Schedule execution in main thread
                        bpy.app.timers.register(execute_wrapper, first_interval=0.0)
                    except json.JSONDecodeError as json_error:
                        # Incomplete data, wait for more
                        # But limit buffer size to prevent memory issues
                        if len(buffer) > 1024 * 1024:  # 1MB limit
                            logger.error(f"Buffer too large from {address} ({len(buffer)} bytes), closing connection")
                            logger.debug(f"Buffer content (first 500 chars): {buffer.decode('utf-8', errors='ignore')[:500]}")
                            break
                        # Log incomplete JSON attempts (but not too frequently)
                        if len(buffer) % 8192 == 0:  # Log every 8KB
                            logger.debug(f"Incomplete JSON from {address}, waiting for more data (current size: {len(buffer)} bytes)")
                        pass
                except Exception as e:
                    logger.error(f"Error receiving data from {address}: {str(e)}")
                    logger.exception("Receive error details:")
                    break
        except Exception as e:
            logger.error(f"Fatal error in client handler for {address}: {str(e)}")
            logger.exception("Client handler error details:")
        finally:
            try:
                client.close()
            except:
                pass
            if client in self.active_clients:
                self.active_clients.remove(client)
            logger.info(f"Client handler stopped for {address}")
    
    def execute_command(self, command):
        """Execute a command using the command router"""
        try:
            # Validate command is a dictionary
            if not isinstance(command, dict):
                error_msg = f"Command must be a dictionary, got: {type(command).__name__}"
                if isinstance(command, str):
                    # Try to parse if it's a JSON string
                    try:
                        import json
                        command = json.loads(command)
                        logger.debug("Parsed JSON string command successfully")
                    except json.JSONDecodeError as json_error:
                        logger.error(f"Invalid JSON command: {str(json_error)}")
                        logger.debug(f"Failed JSON string: {command[:200]}")  # Log first 200 chars
                        return {
                            "status": "error",
                            "error": {
                                "code": "INVALID_COMMAND",
                                "message": f"Command must be a dictionary or valid JSON, got: {type(command).__name__}",
                                "details": {"json_error": str(json_error)}
                            }
                        }
                else:
                    logger.error(f"Invalid command type: {error_msg}")
                    return {
                        "status": "error",
                        "error": {
                            "code": "INVALID_COMMAND",
                            "message": error_msg
                        }
                    }
            
            # Log command details
            command_type = command.get("type", "unknown")
            logger.debug(f"Routing command: {command_type}")
            
            # Execute via router
            response = command_router.route_command(command)
            
            # Log response
            if response.get("status") == "error":
                error_info = response.get("error", {})
                logger.error(
                    f"Command '{command_type}' routing failed: {error_info.get('code', 'UNKNOWN')} - "
                    f"{error_info.get('message', 'No message')}"
                )
            else:
                logger.debug(f"Command '{command_type}' routed successfully")
            
            return response
        except Exception as e:
            command_type = command.get("type", "unknown") if isinstance(command, dict) else "unknown"
            logger.error(f"Exception in execute_command for '{command_type}': {str(e)}")
            logger.exception("Execute command error details:")
            return {
                "status": "error",
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }
