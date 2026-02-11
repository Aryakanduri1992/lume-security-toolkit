"""
Lume Plugin Registry - Simple plugin management for v0.4.0

Provides:
- Plugin registration
- Plugin discovery
- Plugin validation
- Built-in plugin initialization
"""

from typing import Dict, Optional, List
from lume.core.plugin_base import BasePlugin
from lume.core.validators import validate_command_template


class PluginRegistry:
    """
    Simple registry for Lume plugins.
    
    Design:
    - Dictionary-based storage
    - Explicit registration only (no auto-discovery)
    - Validation on registration
    - Internal plugins only (no external loading)
    """
    
    _plugins: Dict[str, BasePlugin] = {}
    _initialized: bool = False
    
    @classmethod
    def register(cls, plugin: BasePlugin) -> None:
        """
        Register a plugin.
        
        Validates plugin before registration:
        - Must be BasePlugin instance
        - Must have valid name
        - Must have valid command template
        
        Args:
            plugin: Plugin instance to register
            
        Raises:
            TypeError: If plugin is not BasePlugin instance
            ValueError: If plugin validation fails
        """
        # Type check
        if not isinstance(plugin, BasePlugin):
            raise TypeError(f"Plugin must be BasePlugin instance, got {type(plugin)}")
        
        # Validate plugin
        if not cls._validate_plugin(plugin):
            raise ValueError(f"Plugin validation failed: {plugin.name}")
        
        # Register
        cls._plugins[plugin.name] = plugin
    
    @classmethod
    def get(cls, name: str) -> Optional[BasePlugin]:
        """
        Get plugin by name.
        
        Args:
            name: Plugin name (e.g., 'nmap')
            
        Returns:
            BasePlugin instance or None if not found
        """
        # Initialize if needed
        if not cls._initialized:
            cls.initialize()
        
        return cls._plugins.get(name)
    
    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all registered plugin names.
        
        Returns:
            List of plugin names
        """
        # Initialize if needed
        if not cls._initialized:
            cls.initialize()
        
        return sorted(cls._plugins.keys())
    
    @classmethod
    def get_all(cls) -> Dict[str, BasePlugin]:
        """
        Get all registered plugins.
        
        Returns:
            Dict mapping plugin names to instances
        """
        # Initialize if needed
        if not cls._initialized:
            cls.initialize()
        
        return cls._plugins.copy()
    
    @classmethod
    def _validate_plugin(cls, plugin: BasePlugin) -> bool:
        """
        Validate plugin meets requirements.
        
        Checks:
        - Has valid name (non-empty string)
        - Has valid command template (list, no shell operators)
        - Has required methods
        
        Args:
            plugin: Plugin to validate
            
        Returns:
            bool: True if valid
        """
        # Check name
        if not plugin.name or not isinstance(plugin.name, str):
            return False
        
        # Check command template
        try:
            template = plugin.command_template
            if not validate_command_template(template):
                return False
        except Exception:
            return False
        
        # Check required methods exist
        required_methods = ['validate_target', 'build_command', 'explain', 'execute']
        for method in required_methods:
            if not hasattr(plugin, method) or not callable(getattr(plugin, method)):
                return False
        
        return True
    
    @classmethod
    def initialize(cls) -> None:
        """
        Initialize built-in plugins.
        
        Registers all 7 core plugins:
        - nmap
        - gobuster
        - nikto
        - sqlmap
        - hydra
        - metasploit
        - whatweb
        """
        if cls._initialized:
            return
        
        # Import and register plugins
        try:
            from lume.plugins.nmap import NmapPlugin
            from lume.plugins.gobuster import GobusterPlugin
            from lume.plugins.nikto import NiktoPlugin
            from lume.plugins.sqlmap import SqlmapPlugin
            from lume.plugins.hydra import HydraPlugin
            from lume.plugins.metasploit import MetasploitPlugin
            from lume.plugins.whatweb import WhatwebPlugin
            
            cls.register(NmapPlugin())
            cls.register(GobusterPlugin())
            cls.register(NiktoPlugin())
            cls.register(SqlmapPlugin())
            cls.register(HydraPlugin())
            cls.register(MetasploitPlugin())
            cls.register(WhatwebPlugin())
            
            cls._initialized = True
            
        except ImportError as e:
            # Plugins not yet implemented - this is OK during development
            pass
    
    @classmethod
    def reset(cls) -> None:
        """
        Reset registry (for testing).
        
        Clears all registered plugins and resets initialization flag.
        """
        cls._plugins.clear()
        cls._initialized = False
