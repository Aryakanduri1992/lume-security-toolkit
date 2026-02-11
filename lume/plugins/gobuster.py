"""
Gobuster Plugin - Directory and subdomain enumeration

Supports:
- Directory brute-forcing
- Subdomain enumeration
- DNS enumeration
"""

from lume.core.plugin_base import BasePlugin
from lume.core.validators import validate_url, validate_domain
from typing import List, Dict


class GobusterPlugin(BasePlugin):
    """
    Gobuster plugin for directory and subdomain enumeration.
    
    Modes:
    - dir: Directory/file enumeration
    - dns: Subdomain enumeration
    """
    
    @property
    def name(self) -> str:
        return "gobuster"
    
    @property
    def command_template(self) -> List[str]:
        return ["gobuster", "dir", "-u", "{target}", "-w", "{wordlist}", "-t", "50"]
    
    def validate_target(self, target: str) -> bool:
        """
        Validate target is URL (for dir mode) or domain (for dns mode).
        
        Args:
            target: Target to validate
            
        Returns:
            bool: True if valid URL or domain
        """
        return validate_url(target) or validate_domain(target)
    
    def build_command(self, target: str, **kwargs) -> List[str]:
        """
        Build gobuster command from template.
        
        Supports kwargs:
        - mode: 'dir' or 'dns'
        - wordlist: Path to wordlist (optional)
        
        Args:
            target: Validated target
            **kwargs: Additional parameters
            
        Returns:
            List[str]: Command as list
        """
        mode = kwargs.get('mode', 'dir')
        
        # Determine wordlist
        if 'wordlist' in kwargs:
            wordlist = kwargs['wordlist']
        elif mode == 'dns':
            wordlist = '/usr/share/wordlists/dnsmap.txt'
        else:
            # Default for directory enumeration
            wordlist = '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt'
        
        if mode == 'dns':
            # DNS/subdomain enumeration
            command = ["gobuster", "dns", "-d", target, "-w", wordlist, "-t", "50"]
        else:
            # Directory enumeration
            command = ["gobuster", "dir", "-u", target, "-w", wordlist, "-t", "50"]
        
        return command
    
    def explain(self, target: str) -> Dict[str, str]:
        """
        Explain what gobuster does.
        
        Args:
            target: Target for context
            
        Returns:
            Dict with summary, impact, warning
        """
        if validate_url(target):
            return {
                'summary': 'Performed directory and file enumeration on web server',
                'impact': 'Discovered hidden paths, admin panels, and accessible web resources',
                'warning': 'Directory brute-forcing generates significant traffic. Use responsibly.'
            }
        else:
            return {
                'summary': 'Performed subdomain enumeration on target domain',
                'impact': 'Identified additional subdomains and expanded attack surface',
                'warning': 'DNS enumeration may be logged. Ensure you have authorization.'
            }
