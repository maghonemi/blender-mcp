# Code created by Siddharth Ahuja: www.github.com/ahujasid © 2025

import time
from typing import Any, Optional, Dict
from utils.logger import logger

class CacheManager:
    """Simple TTL-based cache manager"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._ttl: Dict[str, float] = {}
        self._default_ttl = 60  # Default TTL in seconds
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache if not expired"""
        if key in self._cache:
            if time.time() < self._ttl.get(key, 0):
                logger.debug(f"Cache hit: {key}")
                return self._cache[key]
            else:
                # Expired, remove it
                logger.debug(f"Cache expired: {key}")
                del self._cache[key]
                del self._ttl[key]
        return default
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set value in cache with TTL"""
        ttl = ttl or self._default_ttl
        self._cache[key] = value
        self._ttl[key] = time.time() + ttl
        logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
    
    def invalidate(self, pattern: Optional[str] = None) -> int:
        """Invalidate cache entries. If pattern provided, only invalidate matching keys."""
        if pattern is None:
            count = len(self._cache)
            self._cache.clear()
            self._ttl.clear()
            logger.debug(f"Cache cleared: {count} entries")
            return count
        
        # Pattern matching
        count = 0
        keys_to_remove = [k for k in self._cache.keys() if pattern in k]
        for key in keys_to_remove:
            del self._cache[key]
            del self._ttl[key]
            count += 1
        
        logger.debug(f"Cache invalidated: {count} entries matching '{pattern}'")
        return count
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.invalidate()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "entries": len(self._cache),
            "keys": list(self._cache.keys())
        }

# Global cache instance
cache = CacheManager()
