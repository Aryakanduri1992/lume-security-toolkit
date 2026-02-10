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
        """Display Lume banner"""
        banner = f"""
{self.COLORS['cyan']}{self.COLORS['bold']}
╦  ╦ ╦╔╦╗╔═╗  ╔═╗┌─┐┌─┐┬ ┬┬─┐┬┌┬┐┬ ┬  ╔╦╗┌─┐┌─┐┬  ┬┌─┬┌┬┐
║  ║ ║║║║║╣   ╚═╗├┤ │  │ │├┬┘│ │ └┬┘   ║ │ ││ ││  ├┴┐│ │ 
╩═╝╚═╝╩ ╩╚═╝  ╚═╝└─┘└─┘└─┘┴└─┴ ┴  ┴    ╩ └─┘└─┘┴─┘┴ ┴┴ ┴ 
{self.COLORS['reset']}
{self.COLORS['green']}                    Version 0.2.0 - Production Ready{self.COLORS['reset']}
{self.COLORS['yellow']}              Think in English. Hack in Kali.{self.COLORS['reset']}
{self.COLORS['blue']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{self.COLORS['reset']}
"""
        print(banner)
    
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
