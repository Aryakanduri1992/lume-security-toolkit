"""
Lume Engine - Core command parsing and execution logic
"""

import re
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
from lume.core.smart_engine import SmartEngine


class LumeEngine:
    def __init__(self):
        self.rules = self._load_rules()
        self.log_file = Path.home() / '.lume' / 'history.log'
        self._ensure_log_directory()
        self.smart_engine = SmartEngine()  # Advanced NL understanding
    
    def _load_rules(self) -> Dict:
        """Load command mapping rules from JSON file"""
        rules_path = Path(__file__).parent.parent / 'data' / 'rules.json'
        with open(rules_path, 'r') as f:
            return json.load(f)
    
    def parse_instruction(self, instruction: str) -> Optional[Dict]:
        """
        Parse natural language instruction into a command.
        
        Uses optimized two-stage approach:
        1. Try fast pattern matching first
        2. Fall back to smart engine if no match
        
        Returns: {
            'tool': str,
            'command': str,
            'description': str,
            'warning': str,
            'summary': str,
            'impact': str
        }
        """
        instruction = instruction.lower().strip()
        target = self._extract_target(instruction)
        
        # Stage 1: Fast pattern matching (most common case)
        for rule in self.rules['rules']:
            for pattern in rule['patterns']:
                if re.search(pattern, instruction, re.IGNORECASE):
                    command = self._build_command(rule, target, instruction)
                    return {
                        'tool': rule['tool'],
                        'command': command,
                        'description': rule['description'],
                        'warning': rule.get('warning', 'This command will interact with the target system.'),
                        'summary': rule.get('summary', 'Executed security testing command'),
                        'impact': rule.get('impact', 'Gathered information about the target system')
                    }
        
        # Stage 2: Smart engine for complex/ambiguous queries
        intent = self.smart_engine.detect_intent(instruction)
        
        if intent and intent['confidence'] >= 40:
            tool_name = intent['tool']
            target = intent['target']
            
            for rule in self.rules['rules']:
                if rule['tool'] == tool_name:
                    command = self._build_command(rule, target, instruction)
                    return {
                        'tool': rule['tool'],
                        'command': command,
                        'description': rule['description'],
                        'warning': rule.get('warning', 'This command will interact with the target system.'),
                        'summary': rule.get('summary', 'Executed security testing command'),
                        'impact': rule.get('impact', 'Gathered information about the target system')
                    }
        
        # Stage 3: Smart fallback - if we have a target and action keywords
        if target:
            if any(word in instruction for word in ['scan', 'check', 'test', 'find', 'discover', 'probe', 'analyze']):
                return {
                    'tool': 'nmap',
                    'command': f'nmap -sV -T4 {target}',
                    'description': 'Scan target for open ports and services',
                    'warning': 'Port scanning may trigger IDS/IPS systems. Ensure you have authorization.',
                    'summary': 'Performed a service and version scan on the target',
                    'impact': 'Identified open ports and detected running network services for further analysis'
                }
            else:
                return {
                    'tool': 'nmap',
                    'command': f'nmap -sV -T4 {target}',
                    'description': 'Scan target for open ports and services',
                    'warning': 'Port scanning may trigger IDS/IPS systems. Ensure you have authorization.',
                    'summary': 'Performed a service and version scan on the target',
                    'impact': 'Identified open ports and detected running network services for further analysis'
                }
        
        return None
    
    def _extract_target(self, instruction: str) -> Optional[str]:
        """Extract IP address, domain, or URL from instruction"""
        # IP address pattern
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip_match = re.search(ip_pattern, instruction)
        if ip_match:
            return ip_match.group(0)
        
        # Domain pattern
        domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b'
        domain_match = re.search(domain_pattern, instruction)
        if domain_match:
            return domain_match.group(0)
        
        # URL pattern
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, instruction)
        if url_match:
            return url_match.group(0)
        
        return None
    
    def _build_command(self, rule: Dict, target: Optional[str], instruction: str) -> str:
        """Build the actual command from rule template"""
        command = rule['command']
        
        # Replace target placeholder
        if target:
            command = command.replace('{target}', target)
        else:
            # Use placeholder if no target found
            command = command.replace('{target}', '<TARGET>')
        
        # Handle special cases based on instruction keywords
        if rule['tool'] == 'nmap':
            if 'fast' in instruction or 'quick' in instruction:
                command = command.replace('-sV', '-F')
            elif 'aggressive' in instruction:
                command = command.replace('-sV', '-A')
        
        elif rule['tool'] == 'gobuster':
            # Extract wordlist if mentioned
            if 'common' in instruction:
                command = command.replace('{wordlist}', '/usr/share/wordlists/dirb/common.txt')
            else:
                command = command.replace('{wordlist}', '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt')
        
        elif rule['tool'] == 'hydra':
            # Extract service
            if 'ssh' in instruction:
                command = command.replace('{service}', 'ssh')
            elif 'ftp' in instruction:
                command = command.replace('{service}', 'ftp')
            elif 'http' in instruction or 'web' in instruction:
                command = command.replace('{service}', 'http-post-form')
        
        return command
    
    def execute_command(self, command: str) -> int:
        """Execute the command and return exit code"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                text=True
            )
            return result.returncode
        except Exception as e:
            print(f"Execution error: {str(e)}")
            return 1
    
    def get_supported_tools(self) -> List[str]:
        """Return list of supported tools"""
        return list(set(rule['tool'] for rule in self.rules['rules']))
    
    def _ensure_log_directory(self):
        """Ensure the log directory exists"""
        log_dir = self.log_file.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_execution(self, command: str, summary: str, target: str = None, ml_metadata: dict = None):
        """Log command execution to history file"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] Command: {command}\n"
            if target:
                log_entry += f"            Target: {target}\n"
            log_entry += f"            Summary: {summary}\n"
            
            # Log ML metadata if ML was used
            if ml_metadata and ml_metadata.get('ml_used'):
                log_entry += f"            ML Normalized: Yes (confidence: {ml_metadata.get('confidence', 0):.2f})\n"
                log_entry += f"            Original Input: {ml_metadata.get('original_input', 'N/A')}\n"
            
            log_entry += "\n"
            
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            # Silently fail if logging doesn't work
            pass
    
    def explain_command(self, result: Dict) -> Dict:
        """Return explanation without executing"""
        return {
            'command': result['command'],
            'tool': result['tool'],
            'description': result['description'],
            'summary': result['summary'],
            'impact': result['impact'],
            'warning': result['warning']
        }
