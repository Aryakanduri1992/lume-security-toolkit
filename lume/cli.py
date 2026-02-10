#!/usr/bin/env python3
"""
Lume CLI - Main entry point
"""

import sys
import argparse
from lume.core.engine import LumeEngine
from lume.utils.display import Display
from lume import __version__


def main():
    parser = argparse.ArgumentParser(
        prog='lume',
        description='Lume Security Toolkit - Think in English. Hack in Kali.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lume "scan network for live hosts"
  lume "find admin login page on example.com"
  lume "brute force ssh on 192.168.1.10"
  lume --dry-run "enumerate subdomains"
  lume --explain "scan ports on 192.168.1.1"
  lume --history
  lume "show history"
  
For more information: https://github.com/Aryakanduri1992/lume-security-toolkit
        """
    )
    
    parser.add_argument(
        'instruction',
        nargs='?',
        help='Natural language pentesting instruction'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show command without executing'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'Lume Security Toolkit v{__version__}'
    )
    
    parser.add_argument(
        '--list-tools',
        action='store_true',
        help='List all supported pentesting tools'
    )
    
    parser.add_argument(
        '--explain',
        action='store_true',
        help='Explain what the command does without executing it'
    )
    
    parser.add_argument(
        '--history',
        action='store_true',
        help='Show command execution history'
    )
    
    args = parser.parse_args()
    
    display = Display()
    engine = LumeEngine()
    
    # Show banner
    display.banner()
    
    # List tools if requested
    if args.list_tools:
        display.list_tools(engine.get_supported_tools())
        sys.exit(0)
    
    # Show history if requested
    if args.history:
        display.show_history(engine.log_file)
        sys.exit(0)
    
    # Require instruction
    if not args.instruction:
        parser.print_help()
        sys.exit(1)
    
    # Check for special instructions
    instruction_lower = args.instruction.lower()
    
    # Handle "show history" or "view history" commands
    if 'history' in instruction_lower and ('show' in instruction_lower or 'view' in instruction_lower or 'display' in instruction_lower or 'see' in instruction_lower):
        display.show_history(engine.log_file)
        sys.exit(0)
    
    try:
        # Parse instruction
        result = engine.parse_instruction(args.instruction)
        
        if not result:
            display.error("Could not understand the instruction. Try being more specific.")
            display.info("Example: lume \"scan ports on 192.168.1.1\"")
            sys.exit(1)
        
        # Display the generated command
        display.show_command(result)
        
        # Explain mode
        if args.explain:
            explanation = engine.explain_command(result)
            display.show_explanation(explanation)
            sys.exit(0)
        
        # Dry run mode
        if args.dry_run:
            display.info("Dry-run mode: Command not executed")
            sys.exit(0)
        
        # Ask for confirmation
        if not display.confirm_execution():
            display.warning("Execution cancelled by user")
            sys.exit(0)
        
        # Execute command
        display.info("Executing command...")
        exit_code = engine.execute_command(result['command'])
        
        # Show post-execution summary
        if exit_code == 0:
            display.show_summary(result)
            # Log execution
            target = engine._extract_target(args.instruction)
            engine.log_execution(result['command'], result['summary'], target)
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        display.warning("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        display.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
