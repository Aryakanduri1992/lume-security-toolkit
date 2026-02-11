"""
Lume Plugin Base - Secure plugin interface for v0.4.0

Security Features:
- Command template locking (no dynamic injection)
- shell=False enforcement (no shell interpretation)
- Target validation required
- No string concatenation for commands
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import subprocess


class BasePlugin(ABC):
    """
    Abstract base class for all Lume security plugins.
    
    All plugins must implement this interface to ensure:
    1. Secure command execution (shell=False)
    2. Target validation
    3. Command template locking
    4. Explainability
    
    Security Model:
    - Commands are built from fixed templates (lists)
    - No shell=True execution allowed
    - Targets are validated before use
    - No string concatenation for command building
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Plugin name (e.g., 'nmap', 'gobuster')
        
        Returns:
            str: Lowercase plugin identifier
        """
        pass
    
    @property
    @abstractmethod
    def command_template(self) -> List[str]:
        """
        Command template with {target} placeholder.
        
        Template is a list of strings (not a single string).
        Placeholders like {target} will be replaced during build_command().
        
        Example:
            ["nmap", "-sV", "-T4", "{target}"]
        
        Returns:
            List[str]: Command template as list
        """
        pass
    
    @abstractmethod
    def validate_target(self, target: str) -> bool:
        """
        Validate that target is safe and appropriate for this plugin.
        
        Should check:
        - Target format (IP, domain, URL)
        - No dangerous characters
        - Appropriate for this tool
        
        Args:
            target: Target string to validate
            
        Returns:
            bool: True if target is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def build_command(self, target: str, **kwargs) -> List[str]:
        """
        Build command list from template.
        
        Must return a list (not string) for shell=False execution.
        Replace {target} and other placeholders in template.
        
        Args:
            target: Validated target string
            **kwargs: Additional parameters for command customization
            
        Returns:
            List[str]: Command as list of strings
        """
        pass
    
    @abstractmethod
    def explain(self, target: str) -> Dict[str, str]:
        """
        Return explanation of what this command does.
        
        Used for --explain mode and educational purposes.
        
        Args:
            target: Target for context
            
        Returns:
            Dict with keys:
                - summary: Brief description of action
                - impact: What information is gathered
                - warning: Security/safety warning
        """
        pass
    
    def execute(self, target: str, dry_run: bool = False, **kwargs) -> Dict:
        """
        Execute command securely.
        
        This method is FINAL - do not override in subclasses.
        
        Security guarantees:
        - Target is validated before execution
        - Command is built as list (not string)
        - Executed with shell=False (no shell interpretation)
        - Timeout enforced (5 minutes default)
        
        Args:
            target: Target to execute against
            dry_run: If True, return command without executing
            **kwargs: Additional parameters passed to build_command()
            
        Returns:
            Dict with keys:
                - success: bool
                - command: str (for display)
                - output: str (stdout, if executed)
                - error: str (stderr or error message)
                - dry_run: bool (if dry run mode)
        """
        # Validate target
        if not self.validate_target(target):
            return {
                'success': False,
                'error': f'Invalid target for {self.name}: {target}',
                'command': None
            }
        
        # Build command
        try:
            command_list = self.build_command(target, **kwargs)
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to build command: {str(e)}',
                'command': None
            }
        
        # Validate command is a list
        if not isinstance(command_list, list):
            return {
                'success': False,
                'error': 'Command must be a list, not string',
                'command': None
            }
        
        # Dry run mode
        if dry_run:
            return {
                'success': True,
                'command': ' '.join(command_list),
                'dry_run': True,
                'output': None,
                'error': None
            }
        
        # Execute with shell=False (SECURE)
        try:
            result = subprocess.run(
                command_list,
                shell=False,  # CRITICAL: Never use shell=True
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                'success': result.returncode == 0,
                'command': ' '.join(command_list),
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'command': ' '.join(command_list),
                'error': 'Command timed out after 5 minutes',
                'output': None
            }
        except Exception as e:
            return {
                'success': False,
                'command': ' '.join(command_list),
                'error': f'Execution error: {str(e)}',
                'output': None
            }
