# ML Feature Installation Guide

## Quick Start

### Option 1: Basic Installation (No ML)
```bash
cd ~/lume-security-toolkit
sudo pip3 install -e . --break-system-packages
```

Lume works perfectly without ML using rule-based parsing.

### Option 2: ML-Enhanced Installation
```bash
cd ~/lume-security-toolkit
sudo pip3 install -e ".[ml]" --break-system-packages
python -m spacy download en_core_web_sm
```

This adds ML normalization capabilities.

## Detailed Installation Steps

### Step 1: Update from GitHub
```bash
cd ~/lume-security-toolkit
git pull origin main
```

### Step 2: Install Lume with ML Support
```bash
sudo pip3 install -e ".[ml]" --break-system-packages --upgrade
```

This installs:
- Lume Security Toolkit v0.3.0
- spaCy library (NLP framework)

### Step 3: Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

This downloads the small English model (~12MB).

### Step 4: Verify Installation
```bash
lume --version
```

Expected output:
```
Lume Security Toolkit v0.3.0
```

### Step 5: Test ML Feature
```bash
lume --ml-normalize "first give ip 192.168.1.1 then scan"
```

Expected output:
```
🤖 ML normalization enabled
✓ ML normalized input (confidence: 0.85)
Original: first give ip 192.168.1.1 then scan
Normalized: scan ports on 192.168.1.1
...
```

## Troubleshooting

### Issue 1: spaCy Not Found
```
ModuleNotFoundError: No module named 'spacy'
```

**Solution:**
```bash
sudo pip3 install spacy --break-system-packages
```

### Issue 2: Model Not Found
```
Can't find model 'en_core_web_sm'
```

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### Issue 3: Permission Denied
```
Permission denied when downloading model
```

**Solution:**
```bash
sudo python -m spacy download en_core_web_sm
```

### Issue 4: ML Not Working
```
ML normalization requested but spaCy is not available
```

**Check installation:**
```bash
python3 -c "import spacy; print(spacy.__version__)"
python3 -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded')"
```

## Uninstalling ML Feature

To remove ML capabilities but keep Lume:

```bash
sudo pip3 uninstall spacy
```

Lume will automatically fall back to rule-based parsing.

## System Requirements

### Minimum Requirements
- Python 3.8+
- 100MB free disk space
- 512MB RAM

### Recommended Requirements
- Python 3.10+
- 200MB free disk space
- 1GB RAM

## Kali Linux Specific Notes

### Python Version
Kali Linux 2024+ comes with Python 3.11 by default.

Check your version:
```bash
python3 --version
```

### Virtual Environment (Optional)
If you prefer not to use `--break-system-packages`:

```bash
python3 -m venv ~/lume-venv
source ~/lume-venv/bin/activate
pip install -e ".[ml]"
python -m spacy download en_core_web_sm
```

Then use:
```bash
source ~/lume-venv/bin/activate
lume --ml-normalize "your command"
```

## Update Commands

### Update Lume from GitHub
```bash
cd ~/lume-security-toolkit
git pull origin main
sudo pip3 install -e ".[ml]" --break-system-packages --upgrade
```

### Update spaCy
```bash
sudo pip3 install --upgrade spacy --break-system-packages
```

### Update spaCy Model
```bash
python -m spacy download en_core_web_sm --upgrade
```

## Complete Reinstall

If you encounter issues:

```bash
# Remove old installation
cd ~/lume-security-toolkit
sudo pip3 uninstall lume-security-toolkit -y

# Clean install
git pull origin main
sudo pip3 install -e ".[ml]" --break-system-packages
python -m spacy download en_core_web_sm

# Verify
lume --version
lume --ml-normalize "scan 192.168.1.1"
```

## Disk Space

- **Lume**: ~1MB
- **spaCy library**: ~50MB
- **en_core_web_sm model**: ~12MB
- **Total**: ~63MB

## Performance

First run (model loading):
```bash
time lume --ml-normalize "scan 192.168.1.1"
# ~1-2 seconds
```

Subsequent runs (model cached):
```bash
time lume --ml-normalize "scan 192.168.1.1"
# ~0.1-0.2 seconds
```

## Offline Usage

Once installed, ML works completely offline:
- No internet required
- No API calls
- No data transmission
- Fully local processing

## Security Notes

1. **Installation uses `--break-system-packages`**
   - Required on Kali Linux 2024+
   - Safe for security tools
   - Isolated to Lume dependencies

2. **spaCy is trusted**
   - Production-grade NLP library
   - Used by major companies
   - Open source (MIT license)
   - No telemetry or tracking

3. **Model is static**
   - Pre-trained, not learning
   - Deterministic behavior
   - No data collection
   - Fully auditable

## Support

If you encounter issues:

1. Check this guide
2. Review ML_FEATURE.md
3. Check GitHub issues
4. Open a new issue with:
   - Python version
   - Kali version
   - Error message
   - Installation steps tried

---

**Version**: 0.3.0  
**Last Updated**: February 2026
