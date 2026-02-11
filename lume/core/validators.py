"""
Lume Validators - Security validation utilities for v0.4.0

Provides validation functions for:
- IP addresses
- Domain names
- URLs
- Command templates
- Target sanitization
"""

import re
from typing import List
from urllib.parse import urlparse


def validate_ip(target: str) -> bool:
    """
    Validate IPv4 address format.
    
    Args:
        target: String to validate as IP
        
    Returns:
        bool: True if valid IPv4 address
    """
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(ip_pattern, target))


def validate_domain(target: str) -> bool:
    """
    Validate domain name format.
    
    Args:
        target: String to validate as domain
        
    Returns:
        bool: True if valid domain name
    """
    # Basic domain pattern
    domain_pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$'
    return bool(re.match(domain_pattern, target.lower()))


def validate_url(target: str) -> bool:
    """
    Validate URL format.
    
    Args:
        target: String to validate as URL
        
    Returns:
        bool: True if valid URL
    """
    try:
        result = urlparse(target)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except Exception:
        return False


def validate_ip_or_domain(target: str) -> bool:
    """
    Validate target is either IP or domain.
    
    Args:
        target: String to validate
        
    Returns:
        bool: True if valid IP or domain
    """
    return validate_ip(target) or validate_domain(target)


def validate_command_template(template: List[str]) -> bool:
    """
    Validate command template is safe.
    
    Checks for:
    - Template is a list
    - No shell operators in first element (command name)
    - No command substitution ($, `)
    - No dangerous shell redirects
    
    Note: Semicolons and other operators are allowed in arguments
    (e.g., msfconsole -x "command1; command2") as they're passed
    as single arguments, not interpreted by shell.
    
    Args:
        template: Command template to validate
        
    Returns:
        bool: True if template is safe
    """
    if not isinstance(template, list):
        return False
    
    if len(template) == 0:
        return False
    
    # Check all parts are strings
    for part in template:
        if not isinstance(part, str):
            return False
    
    # Dangerous patterns that indicate shell interpretation
    # These are dangerous in the command name (first element)
    dangerous_in_command = [
        r'&&',     # AND operator
        r'\|\|',   # OR operator
        r'\|',     # Pipe
        r'`',      # Command substitution
        r'\$\(',   # Command substitution
    ]
    
    # Check command name (first element) is clean
    command_name = template[0]
    for pattern in dangerous_in_command:
        if re.search(pattern, command_name):
            return False
    
    # Check for command substitution in all parts
    for part in template:
        if '`' in part or '$(' in part:
            return False
    
    return True


def sanitize_target(target: str) -> str:
    """
    Sanitize target string by removing dangerous characters.
    
    Removes:
    - Shell operators
    - Command substitution characters
    - Quotes (except in URLs)
    - Whitespace (except in URLs)
    
    Args:
        target: Target string to sanitize
        
    Returns:
        str: Sanitized target
    """
    # If it's a URL, be more lenient
    if validate_url(target):
        # Only remove the most dangerous characters
        dangerous_chars = [';', '&', '|', '`', '$', '\n', '\r']
        for char in dangerous_chars:
            target = target.replace(char, '')
        return target
    
    # For IP/domain, be strict
    # Only allow alphanumeric, dots, hyphens, colons (for ports)
    sanitized = re.sub(r'[^a-zA-Z0-9.\-:]', '', target)
    return sanitized


def validate_port(port: str) -> bool:
    """
    Validate port number.
    
    Args:
        port: Port number as string
        
    Returns:
        bool: True if valid port (1-65535)
    """
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False


def extract_target(instruction: str) -> str:
    """
    Extract target (IP, domain, or URL) from instruction.
    
    Args:
        instruction: Natural language instruction
        
    Returns:
        str: Extracted target or None
    """
    instruction = instruction.strip()
    
    # Try URL first (most specific)
    url_pattern = r'https?://[^\s]+'
    url_match = re.search(url_pattern, instruction)
    if url_match:
        return url_match.group(0)
    
    # Try IP address
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ip_match = re.search(ip_pattern, instruction)
    if ip_match:
        return ip_match.group(0)
    
    # Try domain
    domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b'
    domain_match = re.search(domain_pattern, instruction, re.IGNORECASE)
    if domain_match:
        return domain_match.group(0)
    
    return None
