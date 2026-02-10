# 🔦 Lume Installation Guide for Kali Linux

## 🚀 Three Ways to Install

---

## ✨ **OPTION 1: One-Command Install (Easiest)**

Copy and paste this single command into your Kali Linux terminal:

```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/lume-security-toolkit/main/bootstrap.sh | bash
```

**What it does:**
- ✅ Checks prerequisites (Python, pip, git)
- ✅ Creates entire project structure
- ✅ Installs all Python files
- ✅ Sets up rules database
- ✅ Installs Lume command
- ✅ Verifies installation
- ✅ Checks pentesting tools

**Time:** ~2 minutes

---

## 📦 **OPTION 2: Clone from GitHub**

If you've pushed the project to GitHub:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/lume-security-toolkit.git

# Navigate to directory
cd lume-security-toolkit

# Install
sudo pip3 install -e .

# Verify
lume --version
```

**Time:** ~1 minute

---

## 💾 **OPTION 3: Manual File Transfer**

If you have the project on another machine:

### On Your Current Machine:

```bash
# Compress the project
tar -czf lume.tar.gz lume_security_toolkit/

# Transfer to Kali (replace with your Kali IP)
scp lume.tar.gz kali@192.168.1.100:~/
```

### On Your Kali Machine:

```bash
# Extract
tar -xzf lume.tar.gz

# Navigate
cd lume_security_toolkit

# Install
sudo pip3 install -e .

# Verify
lume --version
```

**Time:** ~3 minutes

---

## 🔧 Prerequisites

Before installing, ensure you have:

```bash
# Check Python (need 3.8+)
python3 --version

# Check pip
pip3 --version

# Check git (for Option 1 & 2)
git --version
```

If missing, install:

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

---

## 🛠️ Install Pentesting Tools

Lume requires these tools to be installed:

```bash
sudo apt update
sudo apt install nmap gobuster nikto sqlmap hydra metasploit-framework whatweb -y
```

**Check if installed:**
```bash
which nmap gobuster nikto sqlmap hydra msfconsole whatweb
```

---

## ✅ Verify Installation

After installation, run these commands:

```bash
# 1. Check version
lume --version

# 2. List supported tools
lume --list-tools

# 3. Show help
lume --help

# 4. Test with dry-run (safe)
lume --dry-run "scan ports on 192.168.1.1"
```

**Expected Output:**
```
╦  ╦ ╦╔╦╗╔═╗
║  ║ ║║║║║╣ 
╩═╝╚═╝╩ ╩╚═╝
Security Toolkit v0.1.0
Think in English. Hack in Kali.

Lume Security Toolkit v0.1.0
```

---

## 🧪 Test Installation

### Quick Test:
```bash
lume --dry-run "scan ports on scanme.nmap.org"
```

### Real Test (Authorized Target):
```bash
lume "scan ports on scanme.nmap.org"
# Type 'y' when prompted
```

---

## 🎯 Quick Start Examples

Once installed, try these commands:

```bash
# Port scanning
lume "scan ports on 192.168.1.1"

# Directory enumeration
lume "find admin page on example.com"

# Web vulnerability scan
lume "scan web vulnerabilities on target.com"

# SQL injection test
lume "test sql injection on http://target.com/page?id=1"

# Subdomain discovery
lume "find subdomains of example.com"

# Network discovery
lume "find live hosts on 192.168.1.0"

# Always use dry-run first!
lume --dry-run "your command here"
```

---

## 🔍 Troubleshooting

### Issue: Command not found

```bash
# Add to PATH
export PATH=$PATH:~/.local/bin

# Make permanent
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Or reinstall with sudo
sudo pip3 install -e .
```

### Issue: Permission denied

```bash
# Run with sudo for certain commands
sudo lume "scan ports on 192.168.1.1"
```

### Issue: Module not found

```bash
# Reinstall
cd lume_security_toolkit
sudo pip3 uninstall lume-security-toolkit -y
sudo pip3 install -e .
```

### Issue: Tools not found

```bash
# Install pentesting tools
sudo apt update
sudo apt install nmap gobuster nikto sqlmap hydra metasploit-framework whatweb -y
```

---

## 📍 Installation Locations

After installation, files are located at:

- **Project:** `~/lume-security-toolkit/` (if using bootstrap)
- **Command:** `/usr/local/bin/lume` or `~/.local/bin/lume`
- **Python Package:** Check with `pip3 show lume-security-toolkit`

---

## 🗑️ Uninstall

To remove Lume:

```bash
# Uninstall package
sudo pip3 uninstall lume-security-toolkit -y

# Remove project directory (if using bootstrap)
rm -rf ~/lume-security-toolkit
```

---

## 📚 Next Steps

After installation:

1. **Read the docs:**
   ```bash
   cat ~/lume-security-toolkit/README.md
   ```

2. **Practice with dry-run:**
   ```bash
   lume --dry-run "scan ports on 127.0.0.1"
   ```

3. **Test on authorized targets:**
   ```bash
   lume "scan ports on scanme.nmap.org"
   ```

4. **Learn the patterns:**
   ```bash
   lume --list-tools
   ```

---

## ⚠️ Important Reminders

- ✅ **Only use on authorized systems**
- ✅ **Always use --dry-run first**
- ✅ **Read warnings before confirming**
- ✅ **Get written permission**
- ❌ **Never use without authorization**
- ❌ **Illegal without permission**

---

## 🎓 Support

- **Documentation:** Check README.md in project directory
- **Issues:** Report on GitHub
- **Help:** `lume --help`

---

## 🎉 You're Ready!

Once installed, you can start using Lume:

```bash
lume "scan ports on scanme.nmap.org"
```

**Think in English. Hack in Kali.** 🔦

**Remember: Hack ethically. Get permission. Stay legal.** 🔒
