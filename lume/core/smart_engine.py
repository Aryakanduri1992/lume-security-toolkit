"""
Smart Natural Language Engine - Advanced intent detection for v0.4.0

Features:
- Keyword-based intent detection
- Context-aware tool selection
- Flexible pattern matching
- Smart defaults based on target type
"""

import re
from typing import Dict, Optional, List, Tuple


class SmartEngine:
    """
    Advanced natural language understanding engine.
    
    Uses multiple strategies:
    1. Keyword matching (tool names, actions, targets)
    2. Intent detection (what user wants to do)
    3. Target type detection (IP, domain, URL)
    4. Smart defaults based on context
    """
    
    # Tool keywords - if any of these appear, strongly suggest that tool
    TOOL_KEYWORDS = {
        'nmap': ['nmap', 'port', 'scan', 'host', 'network', 'service', 'open'],
        'gobuster': ['gobuster', 'directory', 'dir', 'path', 'page', 'admin', 'hidden', 'subdomain', 'dns'],
        'nikto': ['nikto', 'web', 'vulnerability', 'vuln', 'server', 'misconfiguration'],
        'sqlmap': ['sqlmap', 'sql', 'injection', 'sqli', 'database', 'db'],
        'hydra': ['hydra', 'brute', 'force', 'password', 'crack', 'login', 'auth'],
        'metasploit': ['metasploit', 'msf', 'exploit', 'eternalblue', 'ms17', 'smb'],
        'whatweb': ['whatweb', 'technology', 'tech', 'cms', 'framework', 'identify', 'fingerprint']
    }
    
    # Action keywords - what the user wants to do
    ACTION_KEYWORDS = {
        'scan': ['scan', 'check', 'test', 'examine', 'probe', 'analyze'],
        'find': ['find', 'discover', 'locate', 'search', 'enumerate', 'list'],
        'exploit': ['exploit', 'attack', 'hack', 'penetrate'],
        'brute': ['brute', 'crack', 'force', 'guess'],
        'identify': ['identify', 'detect', 'fingerprint', 'recognize']
    }
    
    # Target type patterns
    TARGET_PATTERNS = {
        'ip': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'domain': r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b',
        'url': r'https?://[^\s]+'
    }
    
    def __init__(self):
        """Initialize smart engine"""
        pass
    
    def detect_intent(self, instruction: str) -> Optional[Dict]:
        """
        Detect user intent from natural language.
        
        Returns dict with:
        - tool: Detected tool name
        - confidence: Confidence score (0-100)
        - target: Extracted target
        - action: Detected action
        - reasoning: Why this tool was chosen
        """
        instruction_lower = instruction.lower().strip()
        
        # Extract target first
        target, target_type = self._extract_target_with_type(instruction_lower)
        
        # Score each tool based on keywords
        tool_scores = self._score_tools(instruction_lower)
        
        # Detect action
        action = self._detect_action(instruction_lower)
        
        # Get best tool
        if tool_scores:
            best_tool = max(tool_scores, key=tool_scores.get)
            confidence = tool_scores[best_tool]
            
            # Apply context-based adjustments
            best_tool, confidence = self._apply_context(
                best_tool, confidence, target_type, action, instruction_lower
            )
            
            if confidence > 0:
                return {
                    'tool': best_tool,
                    'confidence': confidence,
                    'target': target,
                    'target_type': target_type,
                    'action': action,
                    'reasoning': self._explain_choice(best_tool, tool_scores, action)
                }
        
        # Fallback: if we have a target and any action keyword, default to nmap
        if target and action in ['scan', 'check', 'test', 'find']:
            return {
                'tool': 'nmap',
                'confidence': 50,
                'target': target,
                'target_type': target_type,
                'action': action,
                'reasoning': 'Default to nmap for general scanning'
            }
        
        return None
    
    def _extract_target_with_type(self, instruction: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract target and determine its type"""
        # Try URL first (most specific)
        url_match = re.search(self.TARGET_PATTERNS['url'], instruction)
        if url_match:
            return url_match.group(0), 'url'
        
        # Try IP
        ip_match = re.search(self.TARGET_PATTERNS['ip'], instruction)
        if ip_match:
            return ip_match.group(0), 'ip'
        
        # Try domain
        domain_match = re.search(self.TARGET_PATTERNS['domain'], instruction)
        if domain_match:
            return domain_match.group(0), 'domain'
        
        return None, None
    
    def _score_tools(self, instruction: str) -> Dict[str, int]:
        """Score each tool based on keyword matches"""
        scores = {}
        words = set(instruction.split())
        
        for tool, keywords in self.TOOL_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                # Exact word match
                if keyword in words:
                    score += 30
                # Partial match in instruction
                elif keyword in instruction:
                    score += 15
            
            if score > 0:
                scores[tool] = score
        
        return scores
    
    def _detect_action(self, instruction: str) -> Optional[str]:
        """Detect what action the user wants to perform"""
        words = set(instruction.split())
        
        for action, keywords in self.ACTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in words or keyword in instruction:
                    return action
        
        return None
    
    def _apply_context(self, tool: str, confidence: int, target_type: Optional[str], 
                      action: Optional[str], instruction: str) -> Tuple[str, int]:
        """Apply context-based adjustments to tool selection"""
        
        # URL targets strongly suggest web tools
        if target_type == 'url':
            if tool in ['nmap']:
                # Check if user really wants web scanning
                if any(word in instruction for word in ['web', 'site', 'page', 'directory', 'admin']):
                    tool = 'gobuster'
                    confidence = 70
                elif any(word in instruction for word in ['sql', 'injection', 'database']):
                    tool = 'sqlmap'
                    confidence = 80
                elif any(word in instruction for word in ['vuln', 'vulnerability', 'security']):
                    tool = 'nikto'
                    confidence = 75
        
        # Domain targets with specific keywords
        if target_type == 'domain':
            if any(word in instruction for word in ['subdomain', 'dns']):
                tool = 'gobuster'
                confidence = 80
            elif any(word in instruction for word in ['tech', 'cms', 'framework', 'identify']):
                tool = 'whatweb'
                confidence = 80
        
        # Brute force action
        if action == 'brute':
            if any(word in instruction for word in ['ssh', 'ftp', 'login', 'password']):
                tool = 'hydra'
                confidence = 85
        
        # Exploit action
        if action == 'exploit':
            if any(word in instruction for word in ['smb', 'eternalblue', 'ms17']):
                tool = 'metasploit'
                confidence = 90
        
        return tool, confidence
    
    def _explain_choice(self, tool: str, scores: Dict[str, int], action: Optional[str]) -> str:
        """Explain why this tool was chosen"""
        reasons = []
        
        if tool in scores:
            reasons.append(f"Matched {tool} keywords")
        
        if action:
            reasons.append(f"Detected '{action}' action")
        
        if not reasons:
            reasons.append("Default choice")
        
        return ", ".join(reasons)
    
    def get_tool_description(self, tool: str) -> str:
        """Get human-readable description of what the tool does"""
        descriptions = {
            'nmap': 'Network scanning and port discovery',
            'gobuster': 'Directory/subdomain enumeration',
            'nikto': 'Web vulnerability scanning',
            'sqlmap': 'SQL injection testing',
            'hydra': 'Password brute-forcing',
            'metasploit': 'Exploitation framework',
            'whatweb': 'Web technology identification'
        }
        return descriptions.get(tool, 'Security testing')
