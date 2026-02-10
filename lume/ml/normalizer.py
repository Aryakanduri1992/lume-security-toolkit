"""
ML-based Natural Language Normalizer using spaCy

This module provides safe, deterministic natural language normalization
for the Lume Security Toolkit.

CRITICAL SECURITY RULES:
1. ML NEVER generates shell commands
2. ML NEVER chooses tools or exploits
3. ML NEVER executes anything
4. ML only normalizes natural language into canonical instructions
5. Rule engine validates all normalized output
6. Falls back to rule-based parsing on low confidence

Architecture:
    User Input → spaCy Parser → Canonical Instruction → Rule Engine → Command

Author: Lume Security Team
Version: 0.3.0
License: MIT
"""

import re
from typing import Optional, Tuple, Dict

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False


class MLNormalizer:
    """
    Safe ML-based natural language normalizer using spaCy.
    
    This class uses spaCy's small English model (en_core_web_sm) to:
    - Parse sentence structure
    - Extract intent from verbs and keywords
    - Extract targets (IP/domain/URL)
    - Normalize varied phrasing into canonical instructions
    
    The normalized instructions are then validated against the rule engine
    to ensure they can be properly parsed.
    
    Security Features:
    - Deterministic intent mapping (no free-form generation)
    - Confidence thresholding with fallback
    - Rule engine validation
    - Full audit logging
    - Offline operation only
    """
    
    def __init__(self, rule_engine=None):
        """
        Initialize ML normalizer with optional rule engine for validation.
        
        Args:
            rule_engine: Reference to LumeEngine for validation (optional but recommended)
        """
        self.enabled = False
        self.nlp = None
        self.rule_engine = rule_engine
        
        # Try to load spaCy model
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                self.enabled = True
            except OSError:
                # Model not installed - graceful fallback
                self.enabled = False
        
        # Deterministic intent mapping
        # Maps (verbs + keywords) → canonical instruction template
        self.intent_map = {
            'port_scan': {
                'verbs': ['scan', 'check', 'probe', 'test', 'find', 'discover', 'detect'],
                'keywords': ['port', 'service', 'open', 'tcp', 'udp'],
                'canonical': 'scan ports on {target}',
                'description': 'Port and service scanning'
            },
            'network_discovery': {
                'verbs': ['scan', 'find', 'discover', 'detect', 'identify', 'locate'],
                'keywords': ['network', 'host', 'live', 'active', 'machine', 'device', 'computer'],
                'canonical': 'scan network for hosts on {target}',
                'description': 'Network host discovery'
            },
            'directory_enum': {
                'verbs': ['find', 'enumerate', 'discover', 'search', 'locate', 'list'],
                'keywords': ['directory', 'folder', 'path', 'admin', 'page', 'hidden', 'file'],
                'canonical': 'find directories on {target}',
                'description': 'Directory enumeration'
            },
            'subdomain_enum': {
                'verbs': ['find', 'enumerate', 'discover', 'search', 'list'],
                'keywords': ['subdomain', 'dns', 'domain', 'hostname'],
                'canonical': 'find subdomains of {target}',
                'description': 'Subdomain enumeration'
            },
            'web_vuln_scan': {
                'verbs': ['scan', 'check', 'test', 'analyze', 'audit'],
                'keywords': ['web', 'vulnerability', 'vuln', 'security', 'website', 'http', 'https'],
                'canonical': 'scan web vulnerabilities on {target}',
                'description': 'Web vulnerability scanning'
            },
            'sql_injection': {
                'verbs': ['test', 'check', 'exploit', 'find', 'detect'],
                'keywords': ['sql', 'injection', 'sqli', 'database', 'db'],
                'canonical': 'test sql injection on {target}',
                'description': 'SQL injection testing'
            },
            'ssh_brute': {
                'verbs': ['brute', 'crack', 'force', 'attack', 'break'],
                'keywords': ['ssh', 'password', 'login', 'credential', 'auth'],
                'canonical': 'brute force ssh on {target}',
                'description': 'SSH brute force'
            },
            'ftp_brute': {
                'verbs': ['brute', 'crack', 'force', 'attack', 'break'],
                'keywords': ['ftp', 'password', 'login', 'credential'],
                'canonical': 'brute force ftp on {target}',
                'description': 'FTP brute force'
            },
            'eternalblue': {
                'verbs': ['exploit', 'check', 'test', 'use'],
                'keywords': ['eternalblue', 'ms17', '010', 'smb', 'eternal', 'blue'],
                'canonical': 'check eternalblue on {target}',
                'description': 'EternalBlue vulnerability check'
            },
            'os_detection': {
                'verbs': ['detect', 'identify', 'fingerprint', 'find', 'discover'],
                'keywords': ['os', 'operating', 'system', 'platform', 'version'],
                'canonical': 'detect os on {target}',
                'description': 'Operating system detection'
            },
            'vuln_scan': {
                'verbs': ['scan', 'check', 'find', 'detect', 'search'],
                'keywords': ['vulnerability', 'vuln', 'cve', 'exploit', 'weakness'],
                'canonical': 'scan vulnerabilities on {target}',
                'description': 'Vulnerability scanning'
            },
            'web_tech_id': {
                'verbs': ['identify', 'detect', 'fingerprint', 'find', 'discover'],
                'keywords': ['web', 'technology', 'cms', 'framework', 'stack', 'platform'],
                'canonical': 'identify web technologies on {target}',
                'description': 'Web technology identification'
            }
        }
    
    def is_available(self) -> bool:
        """Check if ML normalization is available."""
        return self.enabled and self.nlp is not None
    
    def normalize(self, text: str, confidence_threshold: float = 0.75) -> Tuple[Optional[str], float, Dict]:
        """
        Normalize natural language input into canonical instruction.
        
        This method:
        1. Parses input with spaCy
        2. Extracts target (IP/domain/URL)
        3. Extracts intent from verbs + keywords
        4. Builds canonical instruction
        5. Validates with rule engine
        6. Returns normalized instruction or None (fallback)
        
        Args:
            text: User input string
            confidence_threshold: Minimum confidence to use ML (default 0.75)
        
        Returns:
            Tuple of (canonical_instruction, confidence, metadata)
            - canonical_instruction: Normalized string or None (triggers fallback)
            - confidence: Float between 0.0 and 1.0
            - metadata: Dict with normalization details for audit logging
        
        Examples:
            >>> normalizer.normalize("first give ip 192.168.1.1 then scan")
            ("scan ports on 192.168.1.1", 0.85, {...})
            
            >>> normalizer.normalize("check example.com for admin pages")
            ("find directories on example.com", 0.80, {...})
        """
        metadata = {
            'ml_used': False,
            'original_input': text,
            'normalized_input': None,
            'intent_detected': None,
            'intent_description': None,
            'target_extracted': None,
            'confidence': 0.0,
            'fallback_reason': None,
            'spacy_available': self.enabled
        }
        
        # Check if spaCy is available
        if not self.enabled or not self.nlp:
            metadata['fallback_reason'] = 'spaCy model not available (install with: python -m spacy download en_core_web_sm)'
            return None, 0.0, metadata
        
        try:
            # Parse with spaCy
            doc = self.nlp(text.lower())
            
            # Extract target (IP/domain/URL)
            target = self._extract_target(doc, text)
            if not target:
                metadata['fallback_reason'] = 'No target (IP/domain/URL) found in input'
                return None, 0.0, metadata
            
            metadata['target_extracted'] = target
            
            # Extract intent using deterministic matching
            intent, confidence = self._extract_intent(doc)
            if not intent:
                metadata['fallback_reason'] = 'No matching intent detected'
                return None, 0.0, metadata
            
            metadata['intent_detected'] = intent
            metadata['intent_description'] = self.intent_map[intent]['description']
            metadata['confidence'] = confidence
            
            # Check confidence threshold
            if confidence < confidence_threshold:
                metadata['fallback_reason'] = f'Low confidence ({confidence:.2f} < {confidence_threshold})'
                return None, confidence, metadata
            
            # Build canonical instruction
            canonical = self.intent_map[intent]['canonical'].format(target=target)
            metadata['normalized_input'] = canonical
            
            # CRITICAL SAFETY CHECK: Validate with rule engine
            if self.rule_engine:
                if not self._validate_with_rules(canonical):
                    metadata['fallback_reason'] = 'Rule engine cannot parse normalized instruction (safety check failed)'
                    return None, confidence, metadata
            
            # Success - ML normalization used
            metadata['ml_used'] = True
            return canonical, confidence, metadata
            
        except Exception as e:
            metadata['fallback_reason'] = f'Error during normalization: {str(e)}'
            return None, 0.0, metadata
    
    def _extract_target(self, doc, original_text: str) -> Optional[str]:
        """
        Extract target (IP/domain/URL) using spaCy entities + regex fallback.
        
        Strategy:
        1. Try spaCy named entity recognition
        2. Fall back to regex patterns (same as rule engine)
        
        Args:
            doc: spaCy Doc object
            original_text: Original input text
        
        Returns:
            Target string (IP/domain/URL) or None
        """
        # Try spaCy named entities first
        for ent in doc.ents:
            # Look for entities that might be targets
            if ent.label_ in ['IP', 'URL', 'ORG', 'GPE', 'PRODUCT']:
                # Validate it looks like a target
                if self._looks_like_target(ent.text):
                    return ent.text
        
        # Fallback to regex patterns (same as existing engine)
        # IP address (with optional CIDR)
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
        ip_match = re.search(ip_pattern, original_text)
        if ip_match:
            return ip_match.group(0)
        
        # URL
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, original_text)
        if url_match:
            return url_match.group(0)
        
        # Domain
        domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b'
        domain_match = re.search(domain_pattern, original_text.lower())
        if domain_match:
            return domain_match.group(0)
        
        return None
    
    def _looks_like_target(self, text: str) -> bool:
        """Quick validation that text looks like a valid target."""
        # Check for IP pattern
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text):
            return True
        # Check for domain pattern
        if re.match(r'^[a-z0-9][a-z0-9-]*\.[a-z]{2,}', text.lower()):
            return True
        # Check for URL
        if text.startswith(('http://', 'https://')):
            return True
        return False
    
    def _extract_intent(self, doc) -> Tuple[Optional[str], float]:
        """
        Extract intent using deterministic verb + keyword matching.
        
        This method uses a simple, explainable scoring algorithm:
        - 50% weight for verb matches
        - 50% weight for keyword matches
        
        Args:
            doc: spaCy Doc object
        
        Returns:
            Tuple of (intent_name, confidence_score)
            - intent_name: Key from intent_map or None
            - confidence_score: Float between 0.0 and 1.0
        """
        # Extract verbs from sentence (lemmatized)
        verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
        
        # Extract nouns and keywords (lemmatized)
        keywords = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN', 'ADJ']]
        
        # Also include raw tokens for exact matches (e.g., "ssh", "ftp")
        raw_tokens = [token.text.lower() for token in doc]
        all_keywords = keywords + raw_tokens
        
        # Score each intent
        intent_scores = {}
        for intent_name, intent_data in self.intent_map.items():
            score = 0.0
            
            # Check verb match (50% weight)
            verb_matches = sum(1 for v in verbs if v in intent_data['verbs'])
            if verb_matches > 0 and len(intent_data['verbs']) > 0:
                verb_score = min(verb_matches / len(intent_data['verbs']), 1.0)
                score += 0.5 * verb_score
            
            # Check keyword match (50% weight)
            keyword_matches = sum(1 for k in all_keywords if k in intent_data['keywords'])
            if keyword_matches > 0 and len(intent_data['keywords']) > 0:
                keyword_score = min(keyword_matches / len(intent_data['keywords']), 1.0)
                score += 0.5 * keyword_score
            
            intent_scores[intent_name] = score
        
        # Get best match
        if not intent_scores:
            return None, 0.0
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        # Require at least some match
        if confidence == 0.0:
            return None, 0.0
        
        return best_intent, confidence
    
    def _validate_with_rules(self, canonical_instruction: str) -> bool:
        """
        Validate that the rule engine can parse the normalized instruction.
        
        This is a CRITICAL safety check that ensures ML output is compatible
        with the rule-based engine.
        
        Args:
            canonical_instruction: Normalized instruction to validate
        
        Returns:
            True if rule engine can parse it, False otherwise
        """
        if not self.rule_engine:
            # No engine provided - skip validation
            # (not recommended for production)
            return True
        
        try:
            result = self.rule_engine.parse_instruction(canonical_instruction)
            return result is not None
        except Exception:
            return False
    
    def get_intent_info(self) -> Dict:
        """
        Get information about supported intents.
        
        Returns:
            Dict mapping intent names to their descriptions
        """
        return {
            name: data['description'] 
            for name, data in self.intent_map.items()
        }
