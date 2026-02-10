# Lume Security Toolkit - Project Structure

## Overview

Lume is a modular, extensible CLI tool that translates natural language into pentesting commands.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Input                            │
│              "scan ports on 192.168.1.1"                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   CLI Layer (cli.py)                     │
│  - Argument parsing                                      │
│  - User interaction                                      │
│  - Display coordination                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Engine Layer (core/engine.py)               │
│  - Instruction parsing                                   │
│  - Pattern matching                                      │
│  - Target extraction                                     │
│  - Command building                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Rules Database (data/rules.json)            │
│  - Pattern definitions                                   │
│  - Command templates                                     │
│  - Tool configurations                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Display Layer (utils/display.py)              │
│  - Formatted output                                      │
│  - Color coding                                          │
│  - User prompts                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Command Execution                         │
│              nmap -sV -T4 192.168.1.1                    │
└─────────────────────────────────────────────────────────┘
```

## Directory Structure

```
lume-security-toolkit/
│
├── lume/                          # Main package
│   ├── __init__.py               # Package initialization
│   ├── cli.py                    # CLI entry point
│   │
│   ├── core/                     # Core logic
│   │   ├── __init__.py
│   │   └── engine.py             # Command parsing engine
│   │
│   ├── utils/                    # Utilities
│   │   ├── __init__.py
│   │   └── display.py            # Output formatting
│   │
│   └── data/                     # Data files
│       └── rules.json            # Command mapping rules
│
├── setup.py                      # Installation script
├── MANIFEST.in                   # Package data inclusion
├── .gitignore                    # Git ignore rules
│
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── EXAMPLES.md                   # Usage examples
├── INSTALL.md                    # Installation guide
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
│
├── test_lume.sh                  # Test suite
└── demo.sh                       # Interactive demo
```

## Component Details

### 1. CLI Layer (`lume/cli.py`)

**Responsibilities:**
- Parse command-line arguments
- Handle user interaction
- Coordinate between engine and display
- Manage execution flow

**Key Functions:**
- `main()` - Entry point for the CLI

### 2. Engine Layer (`lume/core/engine.py`)

**Responsibilities:**
- Parse natural language instructions
- Match patterns against rules
- Extract targets (IP, domain, URL)
- Build executable commands

**Key Classes:**
- `LumeEngine` - Main engine class

**Key Methods:**
- `parse_instruction()` - Parse user input
- `_extract_target()` - Extract target from instruction
- `_build_command()` - Build command from template
- `execute_command()` - Execute the command

### 3. Display Layer (`lume/utils/display.py`)

**Responsibilities:**
- Format output with colors
- Display banners and messages
- Handle user prompts
- Show warnings and errors

**Key Classes:**
- `Display` - Display manager

**Key Methods:**
- `banner()` - Show Lume banner
- `show_command()` - Display generated command
- `confirm_execution()` - Ask for user confirmation
- `info()`, `warning()`, `error()`, `success()` - Message types

### 4. Rules Database (`lume/data/rules.json`)

**Structure:**
```json
{
  "rules": [
    {
      "tool": "nmap",
      "patterns": ["scan.*port", "port.*scan"],
      "command": "nmap -sV -T4 {target}",
      "description": "Scan target for open ports",
      "warning": "Port scanning may trigger IDS/IPS"
    }
  ]
}
```

**Fields:**
- `tool` - Pentesting tool name
- `patterns` - Regex patterns to match
- `command` - Command template with placeholders
- `description` - Human-readable description
- `warning` - Security warning message

## Data Flow

1. **User Input** → CLI receives instruction
2. **Parsing** → Engine analyzes instruction
3. **Pattern Matching** → Engine matches against rules
4. **Target Extraction** → Engine extracts IP/domain/URL
5. **Command Building** → Engine builds command from template
6. **Display** → Display shows command and warning
7. **Confirmation** → User confirms or cancels
8. **Execution** → Command runs if confirmed

## Extension Points

### Adding New Tools

1. Add patterns to `rules.json`
2. Define command template
3. Add special handling in `_build_command()` if needed

### Adding New Features

- **Command history**: Add logging in `execute_command()`
- **Output parsing**: Add parser in new module
- **Plugins**: Create plugin system in new directory
- **AI integration**: Add AI module for advanced parsing

## Design Principles

1. **Modularity** - Each component has a single responsibility
2. **Extensibility** - Easy to add new tools and features
3. **Safety** - Always confirm before execution
4. **Transparency** - Show actual commands being run
5. **Simplicity** - No external dependencies for MVP

## Testing Strategy

- **Unit tests** - Test individual components
- **Integration tests** - Test full workflow
- **Dry-run tests** - Test command generation safely
- **Manual tests** - Test on authorized targets

## Future Architecture

```
lume-security-toolkit/
├── lume/
│   ├── core/
│   │   ├── engine.py
│   │   ├── parser.py          # Advanced NLP parsing
│   │   └── executor.py        # Command execution
│   ├── plugins/               # Plugin system
│   │   ├── custom_tools/
│   │   └── workflows/
│   ├── ai/                    # AI integration
│   │   └── llm_parser.py
│   └── reporting/             # Report generation
│       └── generator.py
```

## Performance Considerations

- Rules loaded once at startup
- Regex patterns optimized for speed
- Minimal dependencies for fast installation
- Subprocess execution for command isolation

## Security Considerations

- No automatic execution without confirmation
- Clear warnings before dangerous operations
- Visible command display
- Audit trail capability (future)
- No credential storage
