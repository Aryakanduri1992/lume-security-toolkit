"""
Nmap Plugin - Network scanning and port discovery

Supports:
- Port scanning
- Service version detection
- OS detection
- Network discovery
- Vulnerability scanning
"""

from lume.core.plugin_base import BasePlugin
from lume.core.validators import validate_ip, validate_domain
from typing import List, Dict


class NmapPlugin(BasePlugin):
    """
    Nmap plugin for network scanning.
    
    Default scan: Service version detection (-sV) with timing template 4 (-T4)
    """
    
    @property
    def name(self) -> str:
        return "nmap"
    
    @property
    def command_template(self) -> List[str]:
        return ["nmap", "-sV", "-T4", "{target}"]
    
    def validate_target(self, target: str) -> bool:
        """
        Validate target is IP address or domain.
        
        Args:
            target: Target to validate
            
        Returns:
            bool: True if valid IP or domain
        """
        # Handle CIDR notation for network scans
        if '/' in target:
            base_ip = target.split('/')[0]
            return validate_ip(base_ip)
        
        return validate_ip(target) or validate_domain(target)
    
    def build_command(self, target: str, **kwargs) -> List[str]:
        """
        Build nmap command from template.
        
        Supports kwargs:
        - scan_type: 'fast', 'aggressive', 'os', 'vuln', 'network'
        
        Args:
            target: Validated target
            **kwargs: Additional parameters
            
        Returns:
            List[str]: Command as list
        """
        scan_type = kwargs.get('scan_type', 'default')
        
        if scan_type == 'fast':
            command = ["nmap", "-F", "-T4", target]
        elif scan_type == 'aggressive':
            command = ["nmap", "-A", "-T4", target]
        elif scan_type == 'os':
            command = ["nmap", "-O", target]
        elif scan_type == 'vuln':
            command = ["nmap", "--script", "vuln", target]
        elif scan_type == 'network':
            # Ensure target has CIDR notation
            if '/' not in target:
                target = f"{target}/24"
            command = ["nmap", "-sn", target]
        else:
            # Default: service version scan
            command = ["nmap", "-sV", "-T4", target]
        
        return command
    
    def explain(self, target: str) -> Dict[str, str]:
        """
        Explain what nmap scan does.
        
        Args:
            target: Target for context
            
        Returns:
            Dict with summary, impact, warning
        """
        return {
            'summary': 'Performed a service and version scan on the target',
            'impact': 'Identified open ports and detected running network services for further analysis',
            'warning': 'Port scanning may trigger IDS/IPS systems. Ensure you have authorization.'
        }
