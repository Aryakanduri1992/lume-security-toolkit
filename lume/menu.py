"""
Lume Interactive Menu - SET-style interface
"""

import sys
from lume.core.engine import LumeEngine
from lume.utils.display import Display


class InteractiveMenu:
    def __init__(self):
        self.engine = LumeEngine()
        self.display = Display()
        self.running = True
    
    def show_main_menu(self):
        """Display the main interactive menu"""
        self.display.clear_screen()
        self.display.banner()
        
        print(f"\n{self.display.COLORS['cyan']}Welcome to the Lume Security Toolkit.{self.display.COLORS['reset']}")
        print(f"{self.display.COLORS['cyan']}The one stop shop for all your pentesting needs.{self.display.COLORS['reset']}\n")
        
        print(f"{self.display.COLORS['green']}The Lume Security Toolkit is a product of ethical hacking community.{self.display.COLORS['reset']}\n")
        
        print(f"{self.display.COLORS['blue']}Select from the menu:{self.display.COLORS['reset']}\n")
        
        print(f"   {self.display.COLORS['bold']}1){self.display.COLORS['reset']} Port Scanning & Network Discovery")
        print(f"   {self.display.COLORS['bold']}2){self.display.COLORS['reset']} Web Application Testing")
        print(f"   {self.display.COLORS['bold']}3){self.display.COLORS['reset']} Password Attacks")
        print(f"   {self.display.COLORS['bold']}4){self.display.COLORS['reset']} Exploitation & Vulnerability Assessment")
        print(f"   {self.display.COLORS['bold']}5){self.display.COLORS['reset']} View Command History")
        print(f"   {self.display.COLORS['bold']}6){self.display.COLORS['reset']} Help, Credits, and About")
        print()
        print(f"  {self.display.COLORS['bold']}99){self.display.COLORS['reset']} Exit Lume Security Toolkit")
        print()
    
    def show_port_scanning_menu(self):
        """Port scanning submenu"""
        self.display.clear_screen()
        self.display.banner()
        
        print(f"\n{self.display.COLORS['cyan']}Port Scanning & Network Discovery{self.display.COLORS['reset']}\n")
        
        print(f"   {self.display.COLORS['bold']}1){self.display.COLORS['reset']} Quick Port Scan (Fast)")
        print(f"   {self.display.COLORS['bold']}2){self.display.COLORS['reset']} Service Version Detection")
        print(f"   {self.display.COLORS['bold']}3){self.display.COLORS['reset']} Network Discovery (Find Live Hosts)")
        print(f"   {self.display.COLORS['bold']}4){self.display.COLORS['reset']} OS Detection")
        print(f"   {self.display.COLORS['bold']}5){self.display.COLORS['reset']} Vulnerability Scan")
        print()
        print(f"  {self.display.COLORS['bold']}99){self.display.COLORS['reset']} Return to Main Menu")
        print()
    
    def show_web_testing_menu(self):
        """Web testing submenu"""
        self.display.clear_screen()
        self.display.banner()
        
        print(f"\n{self.display.COLORS['cyan']}Web Application Testing{self.display.COLORS['reset']}\n")
        
        print(f"   {self.display.COLORS['bold']}1){self.display.COLORS['reset']} Directory & File Enumeration")
        print(f"   {self.display.COLORS['bold']}2){self.display.COLORS['reset']} Subdomain Enumeration")
        print(f"   {self.display.COLORS['bold']}3){self.display.COLORS['reset']} Web Vulnerability Scan (Nikto)")
        print(f"   {self.display.COLORS['bold']}4){self.display.COLORS['reset']} SQL Injection Testing")
        print(f"   {self.display.COLORS['bold']}5){self.display.COLORS['reset']} Web Technology Fingerprinting")
        print()
        print(f"  {self.display.COLORS['bold']}99){self.display.COLORS['reset']} Return to Main Menu")
        print()
    
    def show_password_attacks_menu(self):
        """Password attacks submenu"""
        self.display.clear_screen()
        self.display.banner()
        
        print(f"\n{self.display.COLORS['cyan']}Password Attacks{self.display.COLORS['reset']}\n")
        
        print(f"   {self.display.COLORS['bold']}1){self.display.COLORS['reset']} SSH Brute Force")
        print(f"   {self.display.COLORS['bold']}2){self.display.COLORS['reset']} FTP Brute Force")
        print()
        print(f"  {self.display.COLORS['bold']}99){self.display.COLORS['reset']} Return to Main Menu")
        print()
    
    def show_exploitation_menu(self):
        """Exploitation submenu"""
        self.display.clear_screen()
        self.display.banner()
        
        print(f"\n{self.display.COLORS['cyan']}Exploitation & Vulnerability Assessment{self.display.COLORS['reset']}\n")
        
        print(f"   {self.display.COLORS['bold']}1){self.display.COLORS['reset']} Check for EternalBlue (MS17-010)")
        print()
        print(f"  {self.display.COLORS['bold']}99){self.display.COLORS['reset']} Return to Main Menu")
        print()
    
    def get_target(self):
        """Get target from user"""
        target = input(f"\n{self.display.COLORS['yellow']}Enter target (IP/Domain/URL): {self.display.COLORS['reset']}").strip()
        return target
    
    def execute_command(self, instruction):
        """Execute a command based on instruction"""
        result = self.engine.parse_instruction(instruction)
        
    def show_vuln_menu(self):
        """Display vulnerability scanning menu"""
        menu = f"""
{self.display.COLORS['cyan']}Vulnerability Scanning:{self.d