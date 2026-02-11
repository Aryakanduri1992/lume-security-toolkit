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
        import os
        
        service = kwargs.get('service', 'ssh')
        
        # Check for wordlists and use available ones
        user_wordlist = '/usr/share/wordlists/metasploit/unix_users.txt'
        pass_wordlist = '/usr/share/wordlists/rockyou.txt'
        
        # Fallback wordlists if primary ones don't exist
        if not os.path.exists(user_wordlist):
            # Try common alternatives
            alternatives = [
                '/usr/share/wordlists/metasploit/namelist.txt',
                '/usr/share/seclists/Usernames/top-usernames-shortlist.txt',
                '/usr/share/wordlists/dirb/others/names.txt'
            ]
            for alt in alternatives:
                if os.path.exists(alt):
                    user_wordlist = alt
                    break
            else:
                # Use single common username as last resort
                user_wordlist = 'root'  # Will use -l instead of -L
        
        if not os.path.exists(pass_wordlist):
            # Try common alternatives
            alternatives = [
                '/usr/share/wordlists/rockyou.txt.gz',
                '/usr/share/wordlists/fasttrack.txt',
                '/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-100.txt',
                '/usr/share/wordlists/dirb/others/best110.txt'
            ]
            for alt in alternatives:
                if os.path.exists(alt):
                    pass_wordlist = alt
                    break
            else:
                # Use common passwords as last resort
                pass_wordlist = 'password'  # Will use -p instead of -P
        
        # Build command based on available wordlists
        command = ["hydra"]
        
        # Add user wordlist
        if os.path.exists(user_wordlist):
            command.extend(["-L", user_wordlist])
        else:
            command.extend(["-l", user_wordlist])  # Single username
        
        # Add password wordlist
        if os.path.exists(pass_wordlist):
            command.extend(["-P", pass_wordlist])
        else:
            command.extend(["-p", pass_wordlist])  # Single password
        
        command.extend([target, service])
        
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
