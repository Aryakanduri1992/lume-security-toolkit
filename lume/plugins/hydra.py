"""
Hydra Plugin - Password brute-forcing

Supports:
- SSH brute-forcing
- FTP brute-forcing
- HTTP authentication brute-forcing
"""

from lume.core.plugin_base import BasePlugin
from lume.core.validators import validate_ip, validate_domain
from typing import List, Dict


class HydraPlugin(BasePlugin):
    """
    Hydra plugin for password brute-forcing.
    
    Supports services:
    - SSH
    - FTP
    - HTTP
    """
    
    @property
    def name(self) -> str:
        return "hydra"
    
    @property
    def command_template(self) -> List[str]:
        return [
            "hydra",
            "-L", "/usr/share/wordlists/metasploit/unix_users.txt",
            "-P", "/usr/share/wordlists/rockyou.txt",
            "{target}",
            "{service}"
        ]
    
    def validate_target(self, target: str) -> bool:
        """
        Validate target is IP or domain.
        
        Args:
            target: Target to validate
            
        Returns:
            bool: True if valid IP or domain
        """
        return validate_ip(target) or validate_domain(target)
    
    def build_command(self, target: str, **kwargs) -> List[str]:
        """
        Build hydra command from template.
        
        Supports kwargs:
        - service: 'ssh', 'ftp', 'http-post-form'
        
        Args:
            target: Validated target
            **kwargs: Additional parameters
            
        Returns:
            List[str]: Command as list
        """
        service = kwargs.get('service', 'ssh')
        
        command = [
            "hydra",
            "-L", "/usr/share/wordlists/metasploit/unix_users.txt",
            "-P", "/usr/share/wordlists/rockyou.txt",
            target,
            service
        ]
        
        return command
    
    def explain(self, target: str) -> Dict[str, str]:
        """
        Explain what hydra does.
        
        Args:
            target: Target for context
            
        Returns:
            Dict with summary, impact, warning
        """
        return {
            'summary': 'Performed brute force attack on authentication',
            'impact': 'Tested password strength and attempted credential discovery',
            'warning': 'Brute force attacks may lock accounts and are easily detected. Use carefully.'
        }
