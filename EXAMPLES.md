# 📚 Lume Security Toolkit - Usage Examples

## Real-World Pentesting Scenarios

### 1. Reconnaissance Phase

**Discover live hosts on a network**
```bash
$ lume "find live hosts on 192.168.1.0"

[Tool] nmap
[Description] Discover live hosts on network
[Command] nmap -sn 192.168.1.0/24

Execute this command? [y/N]: y
```

**Identify web technologies**
```bash
$ lume "identify web technologies on example.com"

[Tool] whatweb
[Description] Identify web technologies and CMS
[Command] whatweb example.com
```

### 2. Scanning Phase

**Quick port scan**
```bash
$ lume "quick scan ports on 192.168.1.100"

[Tool] nmap
[Description] Scan target for open ports and services
[Command] nmap -F -T4 192.168.1.100
```

**Comprehensive vulnerability scan**
```bash
$ lume "check vulnerabilities on 10.0.0.5"

[Tool] nmap
[Description] Scan for known vulnerabilities using NSE scripts
[Command] nmap --script vuln 10.0.0.5
```

### 3. Enumeration Phase

**Directory enumeration**
```bash
$ lume "find hidden directories on https://target.com"

[Tool] gobuster
[Description] Enumerate directories and files on web server
[Command] gobuster dir -u https://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50
```

**Subdomain discovery**
```bash
$ lume "enumerate subdomains of example.com"

[Tool] gobuster
[Description] Enumerate subdomains
[Command] gobuster dns -d example.com -w /usr/share/wordlists/dnsmap.txt -t 50
```

### 4. Vulnerability Assessment

**Web server vulnerability scan**
```bash
$ lume "scan web vulnerabilities on https://testsite.com"

[Tool] nikto
[Description] Scan web server for vulnerabilities
[Command] nikto -h https://testsite.com
```

**SQL injection testing**
```bash
$ lume "test sql injection on http://target.com/page?id=1"

[Tool] sqlmap
[Description] Test for SQL injection vulnerabilities
[Command] sqlmap -u http://target.com/page?id=1 --batch --banner
```

### 5. Exploitation Phase

**Check for EternalBlue**
```bash
$ lume "check ms17-010 on 192.168.1.50"

[Tool] metasploit
[Description] Check for EternalBlue vulnerability (MS17-010)
[Command] msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS 192.168.1.50; check; exit'
```

## Dry-Run Examples

Test commands without executing them:

```bash
$ lume --dry-run "brute force ssh on 192.168.1.10"

[Tool] hydra
[Description] Brute force authentication
[Command] hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/rockyou.txt 192.168.1.10 ssh

Dry-run mode: Command not executed
```

## Output Examples

### Successful Command
```bash
$ lume "scan ports on scanme.nmap.org"

╦  ╦ ╦╔╦╗╔═╗
║  ║ ║║║║║╣ 
╩═╝╚═╝╩ ╩╚═╝
Security Toolkit v0.1.0
Think in English. Hack in Kali.

[Tool] nmap
[Description] Scan target for open ports and services

[Command]
  nmap -sV -T4 scanme.nmap.org

⚠️  Port scanning may trigger IDS/IPS systems. Ensure you have authorization.

Execute this command? [y/N]: y
ℹ️  Executing command...

Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.065s latency).
...
```

### Command Not Understood
```bash
$ lume "do something random"

╦  ╦ ╦╔╦╗╔═╗
║  ║ ║║║║║╣ 
╩═╝╚═╝╩ ╩╚═╝
Security Toolkit v0.1.0
Think in English. Hack in Kali.

❌ Could not understand the instruction. Try being more specific.
ℹ️  Example: lume "scan ports on 192.168.1.1"
```

## Tips & Tricks

1. **Be specific with targets**: Include IP addresses, domains, or URLs in your instruction
2. **Use keywords**: Words like "scan", "find", "enumerate", "brute force" help Lume understand intent
3. **Test safely**: Always use `--dry-run` first to see what command will be executed
4. **Check tools**: Use `lume --list-tools` to see all supported tools
5. **Read warnings**: Pay attention to the warnings before confirming execution
