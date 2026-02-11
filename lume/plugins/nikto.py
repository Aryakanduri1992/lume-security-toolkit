"""
Nikto Plugin - Web vulnerability scanning

Supports:
- Web server vulnerability scanning
- Misconfiguration detection
- Outdated software detection
"""

from lume.core.plugin_base import BasePlugin
from lume.core.validators import validate_url, validate_ip, validate_domain
from typing import List, Dict


class NiktoPlugin(BasePlugin):
    """
    Nikto plugin for web vulnerability scanning.
    
    Scans web servers for:
    - Known vulnerabilities
    - Misconfigurations
    - Outdated software
    - Security issues
    """
    
    @property
    def name(self) -> str:
        return "nikto"
    
    @property
    def command_template(self) -> List[str]:
        return ["nikto", "-h", "{target}"]
    
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
        Build nikto command from template.
        
        Args:
            target: Validated target
            **kwargs: Additional parameters
            
        Returns:
            List[str]: Command as list
        """
        command = ["nikto", "-h", target]
        return command
    
    def explain(self, target: str) -> Dict[str, str]:
        """
        Explain what nikto scan does.
        
        Args:
            target: Target for context
            
        Returns:
            Dict with summary, impact, warning
        """
        return {
            'summary': 'Performed comprehensive web vulnerability scan',
            'impact': 'Identified web server misconfigurations, outdated software, and potential vulnerabilities',
            'warning': 'Nikto scans are noisy and easily detected. Use with caution.'
        }
