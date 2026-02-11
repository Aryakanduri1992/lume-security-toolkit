"""
Tests for BasePlugin
"""

import pytest
from lume.core.plugin_base import BasePlugin
from typing import List, Dict


class MockPlugin(BasePlugin):
    """Mock plugin for testing"""
    
    @property
    def name(self) -> str:
        return "mock"
    
    @property
    def command_template(self) -> List[str]:
        return ["echo", "{target}"]
    
    def validate_target(self, target: str) -> bool:
        return len(target) > 0 and "bad" not in target
    
    def build_command(self, target: str, **kwargs) -> List[str]:
        return ["echo", target]
    
    def explain(self, target: str) -> Dict[str, str]:
        return {
            'summary': 'Test command',
            'impact': 'Test impact',
            'warning': 'Test warning'
        }


class TestBasePlugin:
    """Test BasePlugin functionality"""
    
    def test_plugin_properties(self):
        """Test plugin properties"""
        plugin = MockPlugin()
        assert plugin.name == "mock"
        assert plugin.command_template == ["echo", "{target}"]
    
    def test_valid_target(self):
        """Test execution with valid target"""
        plugin = MockPlugin()
        result = plugin.execute("test")
        
        assert result['success'] == True
        assert 'test' in result['output']
        assert result['command'] == "echo test"
    
    def test_invalid_target(self):
        """Test execution with invalid target"""
        plugin = MockPlugin()
        result = plugin.execute("bad_target")
        
        assert result['success'] == False
        assert 'Invalid target' in result['error']
    
    def test_dry_run(self):
        """Test dry run mode"""
        plugin = MockPlugin()
        result = plugin.execute("test", dry_run=True)
        
        assert result['success'] == True
        assert result['dry_run'] == True
        assert result['command'] == "echo test"
        assert result['output'] == None
    
    def test_explain(self):
        """Test explain method"""
        plugin = MockPlugin()
        explanation = plugin.explain("test")
        
        assert 'summary' in explanation
        assert 'impact' in explanation
        assert 'warning' in explanation
