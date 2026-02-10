# 🚀 Quick Start Guide

Get up and running with Lume in 5 minutes!

## Step 1: Install

```bash
git clone https://github.com/yourusername/lume-security-toolkit.git
cd lume-security-toolkit
sudo pip3 install -e .
```

## Step 2: Verify Installation

```bash
lume --version
```

You should see:
```
Lume Security Toolkit v0.1.0
```

## Step 3: Try Your First Command (Safe)

```bash
lume --dry-run "scan ports on scanme.nmap.org"
```

This shows what command would run without actually executing it.

## Step 4: Run a Real Command

```bash
lume "scan ports on scanme.nmap.org"
```

When prompted, type `y` to confirm execution.

## Common Commands

### Reconnaissance
```bash
lume "find live hosts on 192.168.1.0"
lume "identify web technologies on example.com"
```

### Scanning
```bash
lume "scan ports on 192.168.1.100"
lume "check vulnerabilities on target.com"
```

### Enumeration
```bash
lume "find admin page on example.com"
lume "enumerate subdomains of target.com"
```

### Testing
```bash
lume "scan web vulnerabilities on https://testsite.com"
lume "test sql injection on http://target.com/page?id=1"
```

## Tips

1. **Always use --dry-run first** to see what will execute
2. **Only test authorized systems** - get permission first
3. **Read the warnings** before confirming execution
4. **Use specific targets** - include IPs, domains, or URLs

## Next Steps

- Read [EXAMPLES.md](EXAMPLES.md) for more usage examples
- Check [README.md](README.md) for full documentation
- Run `./demo.sh` for an interactive demonstration

## Need Help?

```bash
lume --help
lume --list-tools
```

Happy (ethical) hacking! 🔒
