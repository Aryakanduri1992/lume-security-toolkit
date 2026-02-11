"""
Tests for PluginRegistry
"""

import pytest
from lume.core.plugin_registry import PluginRegistry
from lume.core.plugin_base import BasePlugin
from typing import List, Dict


class TestPlugin(BasePlugin):
    """Test plugin for registry testing"""
    
    @property
    def name(self) -> str:
        return "test"
    
    @property
    def command_template(self) -> List[str]:
        return ["echo", "{target}"]
    
    def validate_target(self, target: str) -> bool:
        return True
    
    def build_command(self, target: str, **kwargs) -> List[str]:
        return ["echo", target]
    
    def explain(self, target: str) -> Dict[str, str]:
        return {
            'summary': 'Test',
            'impact': 'Test',
            'warning': 'Test'
        }


class TestPluginRegistry:
    """Test PluginRegistry functionality"""
    
    def setup_method(self):
        """Reset registry before each test"""
        PluginRegistry.reset()
    
    def test_register_plugin(self):
        """Test registering a plugin"""
        plugin = TestPlugin()
        PluginRegistry.register(plugin)
        
        assert "test" in PluginRegistry.list_all()
    
    def test_get_plugin(self):
        """Test getting a registered plugin"""
        plugin = TestPlugin()
        PluginRegistry.register(plugin)
        
        retrieved = PluginRegistry.get("test")
        assert retrieved is not None
        assert retrieved.name == "test"
    
    def test_get_nonexistent_plugin(self):
        """Test getting a plugin that doesn't exist"""
        result = PluginRegistry.get("nonexistent")
        assert result is None
    
    def test_list_all_plugins(self):
        """Test listing all plugins"""
        plugin1 = TestPlugin()
        PluginRegistry.register(plugin1)
        
        plugins = PluginRegistry.list_all()
        assert isinstance(plugins, list)
        assert "test" in plugins
    
    def test_register_invalid_plugin(self):
        """Test registering invalid plugin"""
        with pytest.raises(TypeError):
            PluginRegistry.register("not a plugin")
