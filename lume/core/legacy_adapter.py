"""
Legacy Adapter - Backward compatibility layer for v0.4.0

Maintains 100% compatibility with v0.3.0 CLI by:
- Using existing LumeEngine for parsing
- Mapping parsed results to plugins
- Translating old behavior to new plugin execution
"""

from typing import Dict, Optional
from lume.core.engine import LumeEngine
from lume.core.plugin_registry import PluginRegistry


class LegacyAdapter:
    """
    Adapter to maintain backward compatibility with v0.3.0.
    
    Bridges the gap between:
    - Old: Natural language → Rule engine → Shell command
    - New: Natural language → Rule engine → Plugin → Secure execution
    
    Users see no difference in behavior.
    """
    
    def __init__(self):
        """Initialize adapter with engine and registry."""
        self.engine = LumeEngine()
        self.registry = PluginRegistry()
    
    def parse_and_execute(self, instruction: str, dry_run: bool = False) -> Dict:
        """
        Parse instruction using legacy engine and execute via plugins.
        
        This is the main entry point for backward compatibility.
        
        Args:
            instruction: Natural language instruction
            dry_run: If True, don't execute (just show command)
            
        Returns:
            Dict with execution result compatible with v0.3.0 format
        """
        # Step 1: Parse using existing engine (maintains all v0.3.0 logic)
        parsed = self.engine.parse_instruction(instruction)
        
        if not parsed:
            return {
                'success': False,
                'error': 'Could not understand instruction',
                'result': None
            }
        
        # Step 2: Extract target
        target = self.engine._extract_target(instruction)
        
        if not target:
            # Some commands might not need a target, use placeholder
            target = '<TARGET>'
        
        # Step 3: Get plugin for this tool
        plugin = self.registry.get(parsed['tool'])
        
        if not plugin:
            # Fallback to legacy execution if plugin not available
            return self._legacy_execute(parsed, dry_run)
        
        # Step 4: Determine scan type or mode from instruction
        kwargs = self._extract_kwargs(instruction, parsed['tool'])
        
        # Step 5: Execute via plugin
        plugin_result = plugin.execute(target, dry_run=dry_run, **kwargs)
        
        # Step 6: Translate plugin result to v0.3.0 format
        return self._translate_result(plugin_result, parsed)
    
    def _extract_kwargs(self, instruction: str, tool: str) -> Dict:
        """
        Extract additional parameters from instruction.
        
        Maps natural language hints to plugin kwargs.
        
        Args:
            instruction: Original instruction
            tool: Tool name
            
        Returns:
            Dict of kwargs for plugin
        """
        instruction_lower = instruction.lower()
        kwargs = {}
        
        if tool == 'nmap':
            if 'fast' in instruction_lower or 'quick' in instruction_lower:
                kwargs['scan_type'] = 'fast'
            elif 'aggressive' in instruction_lower:
                kwargs['scan_type'] = 'aggressive'
            elif 'os' in instruction_lower or 'operating system' in instruction_lower:
                kwargs['scan_type'] = 'os'
            elif 'vuln' in instruction_lower or 'vulnerability' in instruction_lower:
                kwargs['scan_type'] = 'vuln'
            elif 'network' in instruction_lower or 'live host' in instruction_lower:
                kwargs['scan_type'] = 'network'
        
        elif tool == 'gobuster':
            if 'subdomain' in instruction_lower:
                kwargs['mode'] = 'dns'
            else:
                kwargs['mode'] = 'dir'
            
            if 'common' in instruction_lower:
                kwargs['wordlist'] = '/usr/share/wordlists/dirb/common.txt'
        
        elif tool == 'hydra':
            if 'ssh' in instruction_lower:
                kwargs['service'] = 'ssh'
            elif 'ftp' in instruction_lower:
                kwargs['service'] = 'ftp'
            elif 'http' in instruction_lower or 'web' in instruction_lower:
                kwargs['service'] = 'http-post-form'
        
        return kwargs
    
    def _translate_result(self, plugin_result: Dict, parsed: Dict) -> Dict:
        """
        Translate plugin result to v0.3.0 format.
        
        Ensures backward compatibility with existing code.
        
        Args:
            plugin_result: Result from plugin execution
            parsed: Parsed instruction from engine
            
        Returns:
            Dict in v0.3.0 format
        """
        return {
            'success': plugin_result.get('success', False),
            'tool': parsed['tool'],
            'command': plugin_result.get('command'),
            'description': parsed['description'],
            'warning': parsed['warning'],
            'summary': parsed['summary'],
            'impact': parsed['impact'],
            'output': plugin_result.get('output'),
            'error': plugin_result.get('error'),
            'dry_run': plugin_result.get('dry_run', False)
        }
    
    def _legacy_execute(self, parsed: Dict, dry_run: bool) -> Dict:
        """
        Fallback to legacy execution if plugin not available.
        
        Used during development or if plugin fails to load.
        
        Args:
            parsed: Parsed instruction
            dry_run: Dry run mode
            
        Returns:
            Dict with execution result
        """
        if dry_run:
            return {
                'success': True,
                'tool': parsed['tool'],
                'command': parsed['command'],
                'description': parsed['description'],
                'warning': parsed['warning'],
                'summary': parsed['summary'],
                'impact': parsed['impact'],
                'dry_run': True
            }
        
        # Execute using legacy engine
        exit_code = self.engine.execute_command(parsed['command'])
        
        return {
            'success': exit_code == 0,
            'tool': parsed['tool'],
            'command': parsed['command'],
            'description': parsed['description'],
            'warning': parsed['warning'],
            'summary': parsed['summary'],
            'impact': parsed['impact'],
            'exit_code': exit_code
        }
    
    def explain(self, instruction: str) -> Optional[Dict]:
        """
        Get explanation without executing.
        
        Args:
            instruction: Natural language instruction
            
        Returns:
            Dict with explanation or None
        """
        parsed = self.engine.parse_instruction(instruction)
        
        if not parsed:
            return None
        
        return self.engine.explain_command(parsed)
