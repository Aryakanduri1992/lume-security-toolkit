"""
Tests for validators module
"""

import pytest
from lume.core.validators import (
    validate_ip,
    validate_domain,
    validate_url,
    validate_command_template,
    sanitize_target,
    validate_port,
    extract_target
)


class TestIPValidation:
    """Test IP address validation"""
    
    def test_valid_ips(self):
        """Test valid IP addresses"""
        assert validate_ip("192.168.1.1") == True
        assert validate_ip("10.0.0.1") == True
        assert validate_ip("8.8.8.8") == True
        assert validate_ip("255.255.255.255") == True
    
    def test_invalid_ips(self):
        """Test invalid IP addresses"""
        assert validate_ip("256.1.1.1") == False
        assert validate_ip("192.168.1") == False
        assert validate_ip("not.an.ip.address") == False
        assert validate_ip("192.168.1.1.1") == False


class TestDomainValidation:
    """Test domain name validation"""
    
    def test_valid_domains(self):
        """Test valid domain names"""
        assert validate_domain("example.com") == True
        assert validate_domain("sub.example.com") == True
        assert validate_domain("test.co.uk") == True
    
    def test_invalid_domains(self):
        """Test invalid domain names"""
        assert validate_domain("not a domain") == False
        assert validate_domain("192.168.1.1") == False
        assert validate_domain("") == False


class TestURLValidation:
    """Test URL validation"""
    
    def test_valid_urls(self):
        """Test valid URLs"""
        assert validate_url("http://example.com") == True
        assert validate_url("https://example.com") == True
        assert validate_url("https://example.com/path") == True
    
    def test_invalid_urls(self):
        """Test invalid URLs"""
        assert validate_url("ftp://example.com") == False
        assert validate_url("example.com") == False
        assert validate_url("not a url") == False


class TestCommandTemplateValidation:
    """Test command template validation"""
    
    def test_valid_templates(self):
        """Test valid command templates"""
        assert validate_command_template(["nmap", "-sV", "{target}"]) == True
        assert validate_command_template(["gobuster", "dir", "-u", "{target}"]) == True
    
    def test_invalid_templates(self):
        """Test invalid command templates"""
        assert validate_command_template(["nmap", "-sV", "{target}; rm -rf /"]) == False
        assert validate_command_template(["nmap", "&&", "echo"]) == False
        assert validate_command_template(["nmap", "|", "grep"]) == False
        assert validate_command_template("not a list") == False
        assert validate_command_template([]) == False


class TestTargetSanitization:
    """Test target sanitization"""
    
    def test_sanitize_ip(self):
        """Test sanitizing IP addresses"""
        assert sanitize_target("192.168.1.1") == "192.168.1.1"
        assert sanitize_target("192.168.1.1; rm -rf /") == "192.168.1.1"
    
    def test_sanitize_domain(self):
        """Test sanitizing domains"""
        assert sanitize_target("example.com") == "example.com"
        assert sanitize_target("example.com && echo") == "example.com"


class TestPortValidation:
    """Test port validation"""
    
    def test_valid_ports(self):
        """Test valid port numbers"""
        assert validate_port("80") == True
        assert validate_port("443") == True
        assert validate_port("8080") == True
        assert validate_port("65535") == True
    
    def test_invalid_ports(self):
        """Test invalid port numbers"""
        assert validate_port("0") == False
        assert validate_port("65536") == False
        assert validate_port("not a port") == False


class TestTargetExtraction:
    """Test target extraction from instructions"""
    
    def test_extract_ip(self):
        """Test extracting IP from instruction"""
        assert extract_target("scan ports on 192.168.1.1") == "192.168.1.1"
    
    def test_extract_domain(self):
        """Test extracting domain from instruction"""
        assert extract_target("scan example.com") == "example.com"
    
    def test_extract_url(self):
        """Test extracting URL from instruction"""
        assert extract_target("test http://example.com") == "http://example.com"
    
    def test_no_target(self):
        """Test instruction with no target"""
        assert extract_target("just some text") == None
