#!/usr/bin/env python3
"""
Lume CLI - Main entry point
"""

import sys
import argparse
from lume.core.engine import LumeEngine
from lume.core.legacy_adapter import LegacyAdapter
from lume.core.plugin_registry import PluginRegistry
from lume.utils.display import Display
from lume.ml.normalizer import MLNormalizer
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
    
    parser.add_argument(
        '--ml-normalize',
        action='store_true',
        help='Enable ML-based natural language normalization (requires spaCy)'
    )
    
    parser.add_argument(
        '--ml-confidence',
        type=float,
        default=0.75,
        help='Minimum confidence threshold for ML normalization (default: 0.75)'
    )
    
    parser.add_argument(
        '--list-plugins',
        action='store_true',
        help='List all available plugins (v0.4.0 feature)'
    )
    
    parser.add_argument(
        '--plugin-info',
        type=str,
        metavar='PLUGIN',
        help='Show information about a specific plugin'
    )
    
    args = parser.parse_args()
    
    display = Display()
    engine = LumeEngine()
    
    # Initialize plugin system (v0.4.0)
    adapter = LegacyAdapter()
    registry = PluginRegistry()
    
    # Initialize ML normalizer (with rule engine for validation)
    ml_normalizer = MLNormalizer(rule_engine=engine)
    
    # Show banner
    display.banner()
    
    # List tools if requested
    if args.list_tools:
        display.list_tools(engine.get_supported_tools())
        sys.exit(0)
    
    # List plugins if requested (v0.4.0)
    if args.list_plugins:
        plugins = registry.list_all()
        display.info(f"Available plugins ({len(plugins)}):")
        for plugin_name in plugins:
            print(f"  - {plugin_name}")
        sys.exit(0)
    
    # Show plugin info if requested (v0.4.0)
    if args.plugin_info:
        plugin = registry.get(args.plugin_info)
        if not plugin:
            display.error(f"Plugin not found: {args.plugin_info}")
            sys.exit(1)
        
        display.info(f"Plugin: {plugin.name}")
        display.info(f"Command template: {' '.join(plugin.command_template)}")
        explanation = plugin.explain("<target>")
        display.info(f"Summary: {explanation['summary']}")
        display.info(f"Impact: {explanation['impact']}")
        display.warning(f"Warning: {explanation['warning']}")
        sys.exit(0)
    
    # Show history if requested
    if args.history:
        display.show_history(engine.log_file)
        sys.exit(0)
    
    # Require instruction
    if not args.instruction:
        # Show full welcome screen like SET toolkit
        display.welcome_screen()
        sys.exit(0)
    
    # Check for special instructions
    instruction_lower = args.instruction.lower()
    
    # Handle "show history" or "view history" commands
    if 'history' in instruction_lower and ('show' in instruction_lower or 'view' in instruction_lower or 'display' in instruction_lower or 'see' in instruction_lower):
        display.show_history(engine.log_file)
        sys.exit(0)
    
    try:
        # Store original instruction for logging
        original_instruction = args.instruction
        
        # ML Normalization (if enabled)
        ml_metadata = None
        if args.ml_normalize:
            if not ml_normalizer.is_available():
                display.warning("ML normalization requested but spaCy is not available")
                display.info("Install with: python -m spacy download en_core_web_sm")
                display.info("Falling back to rule-based parsing...")
            else:
                display.info("🤖 ML normalization enabled")
                normalized, confidence, ml_metadata = ml_normalizer.normalize(
                    args.instruction,
                    confidence_threshold=args.ml_confidence
                )
                
                if normalized:
                    display.success(f"ML normalized input (confidence: {confidence:.2f})")
                    display.info(f"Original: {original_instruction}")
                    display.info(f"Normalized: {normalized}")
                    args.instruction = normalized
                else:
                    display.info(f"ML fallback: {ml_metadata.get('fallback_reason', 'Unknown')}")
                    display.info("Using rule-based parsing...")
        
        # Parse and execute via plugin system (v0.4.0 with backward compatibility)
        result = adapter.parse_and_execute(args.instruction, dry_run=args.dry_run or args.explain)
        
        if not result['success'] and result.get('error'):
            display.error(result['error'])
            display.info("Example: lume \"scan ports on 192.168.1.1\"")
            sys.exit(1)
        
        # Display the generated command
        display.show_command(result)
        
        # Explain mode
        if args.explain:
            display.show_explanation(result)
            sys.exit(0)
        
        # Dry run mode
        if args.dry_run:
            display.info("Dry-run mode: Command not executed")
            sys.exit(0)
        
        # Ask for confirmation
        if not display.confirm_execution():
            display.warning("Execution cancelled by user")
            sys.exit(0)
        
        # Execute command via plugin system
        display.info("Executing command...")
        result = adapter.parse_and_execute(args.instruction, dry_run=False)
        
        # Show post-execution summary
        if result['success']:
            display.show_summary(result)
            # Log execution (include ML metadata if used)
            target = engine._extract_target(original_instruction)
            engine.log_execution(
                result['command'], 
                result['summary'], 
                target,
                ml_metadata=ml_metadata
            )
            sys.exit(0)
        else:
            if result.get('error'):
                display.error(f"Execution failed: {result['error']}")
            # Don't show generic example on execution errors
            sys.exit(1)
        
    except KeyboardInterrupt:
        display.warning("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        display.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
