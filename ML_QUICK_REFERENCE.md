# ML Feature Quick Reference

## Installation

```bash
# Install with ML support
sudo pip3 install -e ".[ml]" --break-system-packages
python -m spacy download en_core_web_sm
```

## Basic Usage

```bash
# Enable ML normalization
lume --ml-normalize "your flexible instruction"

# Adjust confidence threshold (default: 0.75)
lume --ml-normalize --ml-confidence 0.80 "instruction"

# Without ML (rule-based only)
lume "your instruction"
```

## Examples

| Input | ML Normalizes To | Tool Used |
|-------|------------------|-----------|
| "first give ip 192.168.1.1 then scan" | "scan ports on 192.168.1.1" | nmap |
| "check example.com for admin pages" | "find directories on example.com" | gobuster |
| "enumerate subdomains of target.com" | "find subdomains of target.com" | gobuster |
| "test sqli on http://site.com?id=1" | "test sql injection on http://site.com?id=1" | sqlmap |
| "crack ssh password on 192.168.1.10" | "brute force ssh on 192.168.1.10" | hydra |

## Supported Intents

1. **port_scan** - Port and service scanning
2. **network_discovery** - Find live hosts
3. **directory_enum** - Web directory enumeration
4. **subdomain_enum** - DNS subdomain enumeration
5. **web_vuln_scan** - Web vulnerability scanning
6. **sql_injection** - SQL injection testing
7. **ssh_brute** - SSH brute force
8. **ftp_brute** - FTP brute force
9. **eternalblue** - EternalBlue vulnerability check
10. **os_detection** - Operating system detection
11. **vuln_scan** - General vulnerability scanning
12. **web_tech_id** - Web technology identification

## Confidence Thresholds

- **0.75** (default) - Balanced (recommended)
- **0.80** - More conservative (fewer false positives)
- **0.60** - More permissive (more ML usage)

## Fallback Scenarios

ML falls back to rule-based parsing when:
- spaCy not installed
- No target found in input
- No intent matched
- Confidence below threshold
- Rule engine cannot parse normalized output

## Security Guarantees

✅ ML NEVER generates shell commands
✅ ML NEVER chooses tools
✅ ML NEVER executes anything
✅ Rule engine validates all ML output
✅ Fully offline operation
✅ Deterministic intent mapping

## Troubleshooting

**spaCy not found:**
```bash
sudo pip3 install spacy --break-system-packages
python -m spacy download en_core_web_sm
```

**Model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Check if ML is working:**
```bash
python3 -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('ML ready')"
```

## Performance

- Model size: 12MB
- Load time: ~1 second (first run)
- Inference: <100ms per query
- Memory: ~50MB additional RAM

## Documentation

- [ML_FEATURE.md](ML_FEATURE.md) - Complete feature documentation
- [ML_INSTALLATION.md](ML_INSTALLATION.md) - Installation guide
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [README.md](README.md) - Main documentation

## Version

Current: **0.3.0**
Codename: **Maverick**
