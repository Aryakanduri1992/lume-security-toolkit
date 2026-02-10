# Changelog

All notable changes to Lume Security Toolkit will be documented in this file.

## [0.3.0] - 2026-02-10

### 🚀 Major Feature - ML-Enhanced Natural Language Understanding

#### Added
- **ML Natural Language Normalization** - Safe, offline ML capabilities
  - Uses spaCy (production-grade NLP library)
  - Understands varied phrasing and word order
  - Extracts intent from sentence structure
  - Normalizes to canonical instructions
  - **NEVER generates shell commands** (ML is preprocessor only)
  
- **--ml-normalize Flag** - Opt-in ML enhancement
  - Disabled by default (rule-based remains primary)
  - Configurable confidence threshold (--ml-confidence)
  - Graceful fallback to rule-based parsing
  - Full audit logging of ML decisions

- **12 Canonical Intents** - Deterministic intent mapping
  - Port scanning
  - Network discovery
  - Directory enumeration
  - Subdomain enumeration
  - Web vulnerability scanning
  - SQL injection testing
  - SSH/FTP brute forcing
  - EternalBlue checking
  - OS detection
  - Vulnerability scanning
  - Web technology identification

- **Intent Validation Layer** - Critical safety check
  - ML output validated by rule engine
  - Ensures normalized instructions are parseable
  - Prevents invalid command generation
  - Multiple fallback mechanisms

- **Enhanced Logging** - ML metadata in execution history
  - Logs original input
  - Logs normalized instruction
  - Logs ML confidence score
  - Full audit trail for compliance

#### Security Guarantees
- ✅ ML NEVER generates shell commands
- ✅ ML NEVER chooses tools or exploits
- ✅ ML NEVER executes anything
- ✅ Rule engine remains sole authority
- ✅ Fully offline operation (no API calls)
- ✅ Deterministic intent mapping
- ✅ Confidence thresholding with fallback
- ✅ Rule engine validation of all ML output

#### Technical Details
- New module: `lume/ml/normalizer.py` (400+ lines)
- spaCy integration with en_core_web_sm model (12MB)
- Verb + keyword matching for intent detection
- Entity recognition + regex for target extraction
- Confidence scoring (0.0-1.0 scale)
- Optional dependency (works without spaCy)

#### Installation
```bash
# ML-enhanced installation
sudo pip3 install -e ".[ml]" --break-system-packages
python -m spacy download en_core_web_sm

# Basic installation (no ML)
sudo pip3 install -e . --break-system-packages
```

#### Usage Examples
```bash
# Enable ML normalization
lume --ml-normalize "first give ip 192.168.1.1 then scan"

# Adjust confidence threshold
lume --ml-normalize --ml-confidence 0.80 "check example.com"

# Default (rule-based only)
lume "scan ports on 192.168.1.1"
```

#### Documentation
- ML_FEATURE.md - Complete ML feature documentation
- ML_INSTALLATION.md - Installation and troubleshooting guide
- Updated README with ML capabilities

#### Design Philosophy
> "This tool prioritizes TRUST over intelligence."

ML enhances language understanding but never controls execution.
The rule-based engine remains authoritative for security compliance.

---

## [0.2.0] - 2026-02-10

### 🎉 Major Features - Production-Ready Release

#### Added
- **Post-Execution Summaries** - Clear explanations after each command execution
  - Shows what action was performed
  - Explains the impact and results
  - Helps with learning and documentation

- **--explain Mode** - Educational feature for training
  - Shows what a command would do without executing it
  - Displays summary and impact
  - Perfect for learning and teaching

- **Execution Logging** - Audit trail for compliance
  - Automatic logging to `~/.lume/history.log`
  - Timestamps for all executions
  - Includes command, target, and summary
  - Essential for professional pentesting

- **Enhanced Rules Database** - All 12 rules now include:
  - `summary` - What the command does
  - `impact` - What you learn/achieve
  - Better documentation and transparency

#### Improved
- Engine now returns complete metadata (summary + impact)
- Display module enhanced with explanation and summary views
- CLI supports new --explain flag
- Better user feedback throughout execution

#### Technical
- Added datetime logging
- Created ~/.lume directory for logs
- Enhanced error handling for logging
- Maintained zero external dependencies

### Why This Matters

This release transforms Lume from a working tool to a **production-grade security utility**:

✅ **Compliance-Ready** - Audit trails for enterprise use
✅ **Educational** - Learn while you hack
✅ **Professional** - Industry-standard behavior
✅ **Transparent** - Clear explanations of all actions

---

## [0.1.0] - 2026-02-10

### Initial Release

#### Features
- Natural language to command conversion
- 7 supported tools (nmap, gobuster, nikto, sqlmap, hydra, metasploit, whatweb)
- 12 command mapping rules
- Pattern matching with regex
- Target extraction (IP/domain/URL)
- Dry-run mode
- User confirmation prompts
- Colored CLI output
- Safety warnings
- Comprehensive documentation

#### Supported Tools
- nmap - Port scanning and network discovery
- gobuster - Directory/subdomain enumeration
- nikto - Web vulnerability scanning
- sqlmap - SQL injection testing
- hydra - Password brute-forcing
- metasploit - Exploitation framework
- whatweb - Web technology identification

---

## Future Roadmap

### v0.3.0 (Planned)
- [ ] Report generation (PDF/HTML)
- [ ] Success/failure detection
- [ ] Next-step recommendations
- [ ] More tool integrations (wpscan, enum4linux)
- [ ] Custom wordlist support

### v1.0.0 (Vision)
- [ ] Optional AI/LLM integration
- [ ] Interactive mode
- [ ] Workflow automation
- [ ] Team collaboration features
- [ ] Plugin system
