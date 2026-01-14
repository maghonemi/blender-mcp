# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import logging
import os
import bpy
from datetime import datetime

class BlenderMCPLogger:
    """Centralized logging system for Blender MCP"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BlenderMCPLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger("BlenderMCP")
            self.logger.setLevel(logging.DEBUG)
            self._setup_handlers()
            BlenderMCPLogger._initialized = True
    
    def _setup_handlers(self):
        """Setup console and file handlers"""
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        try:
            log_dir = os.path.join(bpy.app.tempdir, "blendermcp")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"blendermcp_{datetime.now().strftime('%Y%m%d')}.log")
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            # Fallback if file logging fails
            print(f"Warning: Could not setup file logging: {e}")
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
    
    def exception(self, message):
        self.logger.exception(message)

# Global logger instance
logger = BlenderMCPLogger()
