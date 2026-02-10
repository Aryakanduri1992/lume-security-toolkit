# Changelog

All notable changes to Lume Security Toolkit will be documented in this file.

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
