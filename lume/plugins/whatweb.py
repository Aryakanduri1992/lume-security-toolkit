"""
Whatweb Plugin - Web technology identification

Supports:
- Web technology fingerprinting
- CMS detection
- Framework identification
"""

from lume.core.plugin_base import BasePlugin
from lume.core.validators import validate_url, validate_ip, validate_domain
from typing import List, Dict


class WhatwebPlugin(BasePlugin):
    """
    Whatweb plugin for web technology identification.
    
    Identifies:
    - Web servers
    - CMS platforms
    - Frameworks
    - Technologies
    """
    
    @property
    def name(self) -> str:
        return "whatweb"
    
    @property
    def command_template(self) -> List[str]:
        return ["whatweb", "{target}"]
    
    def validate_target(self, target: str) -> bool:
        """
        Validate target is URL, IP, or domain.
        
        Args:
            target: Target to validate
            
        Returns:
            bool: True if valid target
        """
        return validate_url(target) or validate_ip(target) or validate_domain(target)
    
    def build_command(self, target: str, **kwargs) -> List[str]:
        """
        Build whatweb command from template.
        
        Args:
            target: Validated target
            **kwargs: Additional parameters
            
        Returns:
            List[str]: Command as list
        """
        command = ["whatweb", target]
        return command
    
    def explain(self, target: str) -> Dict[str, str]:
        """
        Explain what whatweb does.
        
        Args:
            target: Target for context
            
        Returns:
            Dict with summary, impact, warning
        """
        return {
            'summary': 'Identified web technologies, frameworks, and CMS platform',
            'impact': 'Gathered intelligence on web stack for targeted vulnerability research',
            'warning': 'Web fingerprinting is generally safe but may be logged.'
        }
