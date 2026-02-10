# 📜 Command History Feature

## 🎉 New Feature: View Your Command History

Lume now tracks all your commands and lets you view them easily!

---

## 🚀 **How to Use**

### **Method 1: Using --history Flag**
```bash
lume --history
```

### **Method 2: Natural Language** (NEW!)
```bash
lume "show history"
lume "view history"
lume "display history"
lume "see history"
```

All of these work the same way!

---

## 📊 **What You'll See**

```
📜 Command Execution History
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entry #1:
[2026-02-10 18:42:15] Command: nmap -sV -T4 192.168.70.1
                      Target: 192.168.70.1
                      Summary: Performed a service and version scan on the target

Entry #2:
[2026-02-10 18:45:30] Command: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt -t 50
                      Target: http://example.com
                      Summary: Performed directory and file enumeration on web server

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total commands executed: 2
```

---

## 🎨 **Features**

✅ **Color-coded display**
- 🔵 Timestamps in cyan
- 🟢 Commands in green
- 🟡 Targets in yellow
- 🟣 Summaries in magenta

✅ **Automatic tracking**
- Every successful command is logged
- Includes timestamp, command, target, and summary
- No manual work required

✅ **Natural language support**
- Just say "show history" in plain English
- Works like any other Lume command

✅ **Professional format**
- Numbered entries
- Clear separation
- Total count at the end

---

## 📍 **Where is History Stored?**

Your command history is stored at:
```
~/.lume/history.log
```

You can also view it directly:
```bash
cat ~/.lume/history.log
```

---

## 🔧 **Advanced Usage**

### **View Last 10 Commands**
```bash
tail -n 40 ~/.lume/history.log
```

### **Search History**
```bash
grep "nmap" ~/.lume/history.log
grep "2026-02-10" ~/.lume/history.log
```

### **Clear History**
```bash
rm ~/.lume/history.log
```

### **Export History**
```bash
cp ~/.lume/history.log ~/lume-history-backup.log
```

---

## 💡 **Use Cases**

### **1. Audit Trail**
Keep track of all pentesting activities for reports

### **2. Learning**
Review what commands you've run and learn from them

### **3. Compliance**
Maintain records for security audits

### **4. Debugging**
Check what commands were executed and when

### **5. Documentation**
Generate reports from your testing history

---

## 🎯 **Examples**

### **Example 1: Check Your History**
```bash
$ lume "show history"

📜 Command Execution History
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entry #1:
[2026-02-10 18:42:15] Command: nmap -sV -T4 192.168.70.1
                      Target: 192.168.70.1
                      Summary: Performed a service and version scan

Total commands executed: 1
```

### **Example 2: After Running Multiple Commands**
```bash
$ lume "scan ports on 192.168.1.1"
[executes...]

$ lume "find admin page on example.com"
[executes...]

$ lume --history

📜 Command Execution History
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entry #1:
[2026-02-10 18:42:15] Command: nmap -sV -T4 192.168.1.1
                      Target: 192.168.1.1
                      Summary: Performed a service and version scan

Entry #2:
[2026-02-10 18:45:30] Command: gobuster dir -u example.com -w ...
                      Target: example.com
                      Summary: Performed directory enumeration

Total commands executed: 2
```

---

## 🔒 **Privacy & Security**

- History is stored locally on your machine
- Only successful commands are logged
- No sensitive data is transmitted
- You can delete history anytime
- File permissions: Only you can read it

---

## 📝 **Summary**

**View your history with:**
```bash
lume --history
```

**Or just say:**
```bash
lume "show history"
```

**That's it!** Simple, natural, and powerful. 🔦

---

**Think in English. Hack in Kali.** 🔦
