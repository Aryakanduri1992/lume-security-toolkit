"""
Sqlmap Plugin - SQL injection testing

Supports:
- SQL injection detection
- Database enumeration
- Data extraction
"""

from lume.core.plugin_base import BasePlugin
from lume.core.validators import validate_url
from typing import List, Dict


class SqlmapPlugin(BasePlugin):
    """
    Sqlmap plugin for SQL injection testing.
    
    Tests for:
    - SQL injection vulnerabilities
    - Database type and version
    - Exploitable injection points
    """
    
    @property
    def name(self) -> str:
        return "sqlmap"
    
    @property
    def command_template(self) -> List[str]:
        return ["sqlmap", "-u", "{target}", "--batch", "--banner"]
    
    def validate_target(self, target: str) -> bool:
        """
        Validate target is URL.
        
        Args:
            target: Target to validate
            
        Returns:
            bool: True if valid URL or looks like a URL parameter
        """
        # Accept full URLs
        if validate_url(target):
            return True
        
        # Also accept if it looks like a URL with parameters (common for SQL injection)
        if '?' in target or '=' in target:
            return True
        
        # Accept domains that might be part of URLs
        if validate_domain(target):
            return True
        
        return False
    
    def build_command(self, target: str, **kwargs) -> List[str]:
        """
        Build sqlmap command from template.
        
        Args:
            target: Validated target URL
            **kwargs: Additional parameters
            
        Returns:
            List[str]: Command as list
        """
        command = ["sqlmap", "-u", target, "--batch", "--banner"]
        return command
    
    def explain(self, target: str) -> Dict[str, str]:
        """
        Explain what sqlmap does.
        
        Args:
            target: Target for context
            
        Returns:
            Dict with summary, impact, warning
        """
        return {
            'summary': 'Tested target for SQL injection vulnerabilities',
            'impact': 'Assessed database security and identified potential injection points',
            'warning': 'SQL injection testing may damage databases. Only test authorized systems.'
        }
