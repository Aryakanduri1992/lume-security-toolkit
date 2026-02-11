"""
Display utilities for CLI output
"""

import sys
from typing import Dict, List


class Display:
    # ANSI color codes
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m'
    }
    
    def banner(self):
        """Display Lume banner with logo"""
        banner = f"""
{self.COLORS['cyan']}{self.COLORS['bold']}
    ██╗     ██╗   ██╗███╗   ███╗███████╗
    ██║     ██║   ██║████╗ ████║██╔════╝
    ██║     ██║   ██║██╔████╔██║█████╗  
    ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
    ███████╗╚██████╔╝██║ ╚═╝ ██║███████╗
    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
{self.COLORS['reset']}{self.COLORS['magenta']}
    ╔═╗┌─┐┌─┐┬ ┬┬─┐┬┌┬┐┬ ┬  ╔╦╗┌─┐┌─┐┬  ┬┌─┬┌┬┐
    ╚═╗├┤ │  │ │├┬┘│ │ └┬┘   ║ │ ││ ││  ├┴┐│ │ 
    ╚═╝└─┘└─┘└─┘┴└─┴ ┴  ┴    ╩ └─┘└─┘┴─┘┴ ┴┴ ┴ 
{self.COLORS['reset']}
{self.COLORS['white']}  Developed by Lume Security Under {self.COLORS['bold']}Travlume Tech Pvt Ltd{self.COLORS['reset']}
{self.COLORS['green']}      Version 0.4.0 - Plugin Architecture{self.COLORS['reset']}
{self.COLORS['yellow']}      Think in English. Hack in Kali.{self.COLORS['reset']}
{self.COLORS['blue']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{self.COLORS['reset']}
"""
        print(banner)
    
    def welcome_screen(self):
        """Display full welcome screen like SET toolkit"""
        import os
        os.system('clear' if os.name != 'nt' else 'cls')
        
        welcome = f"""
{self.COLORS['cyan']}{self.COLORS['bold']}
    ██╗     ██╗   ██╗███╗   ███╗███████╗
    ██║     ██║   ██║████╗ ████║██╔════╝
    ██║     ██║   ██║██╔████╔██║█████╗  
    ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
    ███████╗╚██████╔╝██║ ╚═╝ ██║███████╗
    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
{self.COLORS['reset']}
{self.COLORS['magenta']}         🔦 SECURITY TOOLKIT 🔦{self.COLORS['reset']}

{self.COLORS['green']}{self.COLORS['bold']}[━━━]  The Natural Language Pentesting Toolkit  [━━━]{self.COLORS['reset']}

{self.COLORS['yellow']}        Created by: Arya Kanduri{self.COLORS['reset']}
{self.COLORS['cyan']}        Version: 0.4.0{self.COLORS['reset']}
{self.COLORS['magenta']}        Codename: 'Maverick'{self.COLORS['reset']}

{self.COLORS['green']}Welcome to the Lume Security Toolkit.
The one stop shop for all of your natural language pentesting needs.{self.COLORS['reset']}

{self.COLORS['blue']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{self.COLORS['reset']}

{self.COLORS['bold']}SUPPORTED TOOLS:{self.COLORS['reset']}

  {self.COLORS['green']}1){self.COLORS['reset']} nmap       - Network scanning and port discovery
  {self.COLORS['green']}2){self.COLORS['reset']} gobuster   - Directory/subdomain enumeration
  {self.COLORS['green']}3){self.COLORS['reset']} nikto      - Web vulnerability scanning
  {self.COLORS['green']}4){self.COLORS['reset']} sqlmap     - SQL injection testing
  {self.COLORS['green']}5){self.COLORS['reset']} hydra      - Password brute-forcing
  {self.COLORS['green']}6){self.COLORS['reset']} metasploit - Exploitation framework
  {self.COLORS['green']}7){self.COLORS['reset']} whatweb    - Web technology identification

{self.COLORS['blue']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{self.COLORS['reset']}

{self.COLORS['bold']}QUICK START EXAMPLES:{self.COLORS['reset']}

  {self.COLORS['cyan']}lume "scan ports on 192.168.1.1"{self.COLORS['reset']}
  {self.COLORS['cyan']}lume "find admin page on example.com"{self.COLORS['reset']}
  {self.COLORS['cyan']}lume "test sql injection on http://target.com/page?id=1"{self.COLORS['reset']}
  {self.COLORS['cyan']}lume --explain "scan ports on target.com"{self.COLORS['reset']}
  {self.COLORS['cyan']}lume --history{self.COLORS['reset']}
  {self.COLORS['cyan']}lume --help{self.COLORS['reset']}

{self.COLORS['blue']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{self.COLORS['reset']}

{self.COLORS['yellow']}{self.COLORS['bold']}⚠️  IMPORTANT:{self.COLORS['reset']}
{self.COLORS['yellow']}   • Only use on authorized systems
   • Get written permission before testing
   • Unauthorized access is illegal
   • Use for ethical hacking only{self.COLORS['reset']}

{self.COLORS['blue']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{self.COLORS['reset']}

{self.COLORS['green']}{self.COLORS['bold']}Think in English. Hack in Kali. 🔦{self.COLORS['reset']}

"""
        print(welcome)
    
    def show_command(self, result: Dict):
        """Display the generated command"""
        print(f"\n{self.COLORS['bold']}[Tool]{self.COLORS['reset']} {result['tool']}")
        print(f"{self.COLORS['bold']}[Description]{self.COLORS['reset']} {result['description']}")
        print(f"\n{self.COLORS['green']}{self.COLORS['bold']}[Command]{self.COLORS['reset']}")
        print(f"  {result['command']}\n")
        
        # Show warning
        print(f"{self.COLORS['yellow']}⚠️  {result['warning']}{self.COLORS['reset']}\n")
    
    def confirm_execution(self) -> bool:
        """Ask user for confirmation"""
        try:
            response = input(f"{self.COLORS['bold']}Execute this command? [y/N]: {self.COLORS['reset']}").strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False
    
    def info(self, message: str):
        """Display info message"""
        print(f"{self.COLORS['blue']}ℹ️  {message}{self.COLORS['reset']}")
    
    def warning(self, message: str):
        """Display warning message"""
        print(f"{self.COLORS['yellow']}⚠️  {message}{self.COLORS['reset']}")
    
    def error(self, message: str):
        """Display error message"""
        print(f"{self.COLORS['red']}❌ {message}{self.COLORS['reset']}", file=sys.stderr)
    
    def success(self, message: str):
        """Display success message"""
        print(f"{self.COLORS['green']}✓ {message}{self.COLORS['reset']}")
    
    def list_tools(self, tools: List[str]):
        """Display supported tools"""
        print(f"\n{self.COLORS['bold']}Supported Pentesting Tools:{self.COLORS['reset']}\n")
        for tool in sorted(tools):
            print(f"  • {tool}")
        print()
    
    def show_explanation(self, result: Dict):
        """Display command explanation without execution"""
        print(f"\n{self.COLORS['cyan']}{self.COLORS['bold']}[Explanation Mode]{self.COLORS['reset']}\n")
        print(f"{self.COLORS['bold']}Tool:{self.COLORS['reset']} {result['tool']}")
        print(f"{self.COLORS['bold']}Command:{self.COLORS['reset']} {result['command']}\n")
        print(f"{self.COLORS['bold']}What it does:{self.COLORS['reset']}")
        print(f"  • {result['summary']}")
        print(f"  • {result['impact']}\n")
        print(f"{self.COLORS['yellow']}⚠️  {result['warning']}{self.COLORS['reset']}\n")
    
    def show_summary(self, result: Dict):
        """Display post-execution summary"""
        print(f"\n{self.COLORS['green']}{self.COLORS['bold']}✔ Action Summary:{self.COLORS['reset']}")
        print(f"{self.COLORS['green']}  • {result['summary']}{self.COLORS['reset']}")
        print(f"{self.COLORS['green']}  • {result['impact']}{self.COLORS['reset']}\n")
    
    def show_history(self, log_file):
        """Display command execution history"""
        from pathlib import Path
        
        log_path = Path(log_file)
        
        if not log_path.exists():
            print(f"\n{self.COLORS['yellow']}No command history found.{self.COLORS['reset']}")
            print(f"{self.COLORS['blue']}History will be created after your first command execution.{self.COLORS['reset']}\n")
            return
        
        try:
            with open(log_path, 'r') as f:
                content = f.read()
            
            if not content.strip():
                print(f"\n{self.COLORS['yellow']}Command history is empty.{self.COLORS['reset']}\n")
                return
            
            print(f"\n{self.COLORS['cyan']}{self.COLORS['bold']}📜 Command Execution History{self.COLORS['reset']}")
            print(f"{self.COLORS['blue']}{'━' * 60}{self.COLORS['reset']}\n")
            
            # Parse and display history entries
            entries = content.strip().split('\n\n')
            for i, entry in enumerate(entries, 1):
                if entry.strip():
                    lines = entry.strip().split('\n')
                    print(f"{self.COLORS['bold']}Entry #{i}:{self.COLORS['reset']}")
                    for line in lines:
                        if line.startswith('['):
                            # Timestamp line
                            print(f"{self.COLORS['cyan']}{line}{self.COLORS['reset']}")
                        elif 'Command:' in line:
                            print(f"{self.COLORS['green']}{line}{self.COLORS['reset']}")
                        elif 'Target:' in line:
                            print(f"{self.COLORS['yellow']}{line}{self.COLORS['reset']}")
                        elif 'Summary:' in line:
                            print(f"{self.COLORS['magenta']}{line}{self.COLORS['reset']}")
                        else:
                            print(line)
                    print()
            
            print(f"{self.COLORS['blue']}{'━' * 60}{self.COLORS['reset']}")
            print(f"{self.COLORS['green']}Total commands executed: {len(entries)}{self.COLORS['reset']}\n")
            
        except Exception as e:
            print(f"\n{self.COLORS['red']}Error reading history: {str(e)}{self.COLORS['reset']}\n")
