# ML Natural Language Normalization Feature

## Overview

Version 0.3.0 introduces **SAFE, OFFLINE machine learning** capabilities to enhance natural language understanding while maintaining all security guarantees.

## What ML Does

The ML normalization layer uses **spaCy** (a production-grade NLP library) to:

✅ **Understand varied phrasing**
- "scan ports on 192.168.1.1"
- "first give ip 192.168.1.1 then scan"
- "check 192.168.1.1 for open ports"

All normalize to: `"scan ports on 192.168.1.1"`

✅ **Extract intent from sentence structure**
- Identifies verbs (scan, find, test, etc.)
- Identifies keywords (port, directory, sql, etc.)
- Maps to canonical instructions

✅ **Extract targets reliably**
- IP addresses (192.168.1.1, 10.0.0.0/24)
- Domains (example.com)
- URLs (http://target.com/page?id=1)

## What ML Does NOT Do

❌ **NEVER generates shell commands**
❌ **NEVER chooses tools or exploits**
❌ **NEVER executes anything**
❌ **NEVER makes security decisions**

The rule-based engine remains the **SOLE AUTHORITY** for command generation.

## Architecture

```
User Input
    ↓
[OPTIONAL] ML Normalizer (spaCy)
    ↓
Canonical English Instruction
    ↓
Rule-Based Engine (AUTHORITATIVE)
    ↓
Command + Explanation
    ↓
User Confirmation
    ↓
Execution
```

## Security Guarantees

1. **Offline Operation** - No API calls, no data leaves your system
2. **Deterministic Intent Mapping** - No free-form generation
3. **Rule Engine Validation** - ML output must be parseable by rules
4. **Confidence Thresholding** - Falls back to rules on low confidence
5. **Full Audit Logging** - All ML decisions are logged
6. **Graceful Degradation** - Works without spaCy installed

## Installation

### Basic Installation (No ML)
```bash
sudo pip3 install -e . --break-system-packages
```

### ML-Enhanced Installation
```bash
# Install Lume with ML support
sudo pip3 install -e ".[ml]" --break-system-packages

# Download spaCy English model (12MB)
python -m spacy download en_core_web_sm
```

## Usage

### Enable ML Normalization
```bash
lume --ml-normalize "first give ip 192.168.1.1 then scan"
```

Output:
```
🤖 ML normalization enabled
✓ ML normalized input (confidence: 0.85)
Original: first give ip 192.168.1.1 then scan
Normalized: scan ports on 192.168.1.1

[Tool] nmap
[Description] Scan target for open ports and services
...
```

### Adjust Confidence Threshold
```bash
lume --ml-normalize --ml-confidence 0.80 "check example.com for admin pages"
```

Default threshold: **0.75** (75% confidence)

### ML is Disabled by Default
```bash
# This uses rule-based parsing only
lume "scan ports on 192.168.1.1"
```

## How It Works

### 1. Intent Detection (Deterministic)

ML uses predefined intent maps:

```python
'port_scan': {
    'verbs': ['scan', 'check', 'probe', 'test', 'find'],
    'keywords': ['port', 'service', 'open'],
    'canonical': 'scan ports on {target}'
}
```

Scoring:
- 50% weight for verb matches
- 50% weight for keyword matches
- Minimum threshold: 0.75 (configurable)

### 2. Target Extraction

Uses spaCy entity recognition + regex fallback:
1. Try spaCy named entities (IP, URL, ORG)
2. Fall back to regex patterns (same as rule engine)

### 3. Validation (Critical Safety Check)

Before using ML output:
```python
# Can the rule engine parse this?
if not rule_engine.parse_instruction(normalized):
    # Fallback to original input
    use_original_input()
```

### 4. Fallback Scenarios

ML falls back to rule-based parsing when:
- spaCy not installed
- No target found
- No intent matched
- Confidence below threshold
- Rule engine cannot parse normalized output

## Supported Intents

| Intent | Example Input | Canonical Output |
|--------|---------------|------------------|
| Port Scan | "check ports on 192.168.1.1" | "scan ports on 192.168.1.1" |
| Network Discovery | "find live hosts on 10.0.0.0/24" | "scan network for hosts on 10.0.0.0/24" |
| Directory Enum | "search for admin pages on example.com" | "find directories on example.com" |
| Subdomain Enum | "enumerate subdomains of example.com" | "find subdomains of example.com" |
| Web Vuln Scan | "check website security on target.com" | "scan web vulnerabilities on target.com" |
| SQL Injection | "test for sqli on http://site.com?id=1" | "test sql injection on http://site.com?id=1" |
| SSH Brute Force | "crack ssh password on 192.168.1.10" | "brute force ssh on 192.168.1.10" |
| FTP Brute Force | "brute ftp on 192.168.1.20" | "brute force ftp on 192.168.1.20" |
| EternalBlue | "check for ms17-010 on 192.168.1.30" | "check eternalblue on 192.168.1.30" |
| OS Detection | "identify operating system on target" | "detect os on target" |
| Vuln Scan | "find vulnerabilities on 192.168.1.1" | "scan vulnerabilities on 192.168.1.1" |
| Web Tech ID | "fingerprint web stack on example.com" | "identify web technologies on example.com" |

## Audit Logging

When ML is used, execution history includes:

```
[2026-02-10 18:42] Command: nmap -sV -T4 192.168.1.1
            Target: 192.168.1.1
            Summary: Performed a service and version scan on the target
            ML Normalized: Yes (confidence: 0.85)
            Original Input: first give ip 192.168.1.1 then scan
```

## Examples

### Example 1: Flexible Phrasing
```bash
# Without ML (fails - doesn't match patterns)
lume "first give ip 192.168.1.1 then scan"
# Error: Could not understand the instruction

# With ML (succeeds)
lume --ml-normalize "first give ip 192.168.1.1 then scan"
# Normalized to: "scan ports on 192.168.1.1"
# Executes: nmap -sV -T4 192.168.1.1
```

### Example 2: Synonym Handling
```bash
# Without ML (might not match)
lume "enumerate admin pages on example.com"

# With ML (normalizes to canonical form)
lume --ml-normalize "enumerate admin pages on example.com"
# Normalized to: "find directories on example.com"
# Executes: gobuster dir -u example.com ...
```

### Example 3: Low Confidence Fallback
```bash
lume --ml-normalize "do something with 192.168.1.1"
# ML fallback: No matching intent detected
# Using rule-based parsing...
```

## Performance

- **Model Size**: 12MB (en_core_web_sm)
- **Load Time**: ~1 second (first run)
- **Inference Time**: <100ms per query
- **Memory**: ~50MB additional RAM

## Troubleshooting

### spaCy Not Found
```
ML normalization requested but spaCy is not available
Install with: python -m spacy download en_core_web_sm
Falling back to rule-based parsing...
```

**Solution:**
```bash
pip3 install spacy
python -m spacy download en_core_web_sm
```

### Low Confidence
```
ML fallback: Low confidence (0.65 < 0.75)
Using rule-based parsing...
```

**Solution:** Lower threshold or use more specific phrasing
```bash
lume --ml-normalize --ml-confidence 0.60 "your instruction"
```

### Rule Engine Cannot Parse
```
ML fallback: Rule engine cannot parse normalized instruction (safety check failed)
```

This is a **safety feature** - ML produced output that doesn't match any rules.

## Design Philosophy

> **"This tool prioritizes TRUST over intelligence."**

ML enhances language understanding but **never controls execution**.

The rule-based engine remains authoritative because:
- ✅ Deterministic behavior
- ✅ Explainable decisions
- ✅ Auditable actions
- ✅ Security compliance
- ✅ No surprises

ML is a **linguistic assistant**, not a decision-maker.

## Technical Details

### spaCy Pipeline
```
Tokenization → POS Tagging → Dependency Parsing → NER
```

We use:
- **POS Tagging**: Extract verbs and nouns
- **Lemmatization**: Normalize word forms
- **NER**: Extract IP/domain entities

We do NOT use:
- Word vectors (not needed)
- Dependency parsing (not needed)
- Custom training (not needed)

### Confidence Calculation
```python
confidence = (verb_score * 0.5) + (keyword_score * 0.5)

verb_score = min(matches / total_verbs, 1.0)
keyword_score = min(matches / total_keywords, 1.0)
```

Simple, explainable, deterministic.

## Future Enhancements

Potential improvements (maintaining security guarantees):

1. **Custom Intent Training** - Add user-defined intents
2. **Multi-language Support** - Spanish, French, etc.
3. **Typo Correction** - Handle common misspellings
4. **Context Memory** - Remember previous targets

All enhancements will maintain:
- Offline operation
- Deterministic behavior
- Rule engine authority
- Full auditability

## Compliance

This ML implementation is suitable for:
- ✅ Enterprise pentesting
- ✅ Red team operations
- ✅ Security audits
- ✅ Training environments
- ✅ Compliance requirements

Because:
- All actions are logged
- All decisions are explainable
- No data leaves the system
- Rule engine remains authoritative
- User confirmation required

## Questions?

**Q: Is this AI-powered hacking?**
A: No. ML only normalizes language. The rule engine generates all commands.

**Q: Can ML execute commands?**
A: No. ML only produces English instructions. The rule engine validates them.

**Q: Does this send data to the cloud?**
A: No. Everything runs offline on your Kali machine.

**Q: Is ML required?**
A: No. Lume works perfectly without ML. It's an optional enhancement.

**Q: Can I trust ML output?**
A: Yes. ML output is validated by the rule engine before use.

---

**Version**: 0.3.0  
**Author**: Arya Kanduri  
**License**: MIT  
**Codename**: Maverick
