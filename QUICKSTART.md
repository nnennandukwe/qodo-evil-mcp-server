# Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Initialize the database:**
   ```bash
   uv run python -c "from src.database import init_database; init_database()"
   ```

3. **Run the server:**
   ```bash
   uv run python src/server.py
   ```

## Testing Vulnerabilities

### Run All Tests
```bash
uv run pytest tests/test_server.py -v
```

### Run Specific Test Categories
```bash
# SQL Injection tests
uv run pytest tests/test_server.py::TestSQLInjection -v

# Path Traversal tests
uv run pytest tests/test_server.py::TestPathTraversal -v

# Weak Cryptography tests
uv run pytest tests/test_server.py::TestWeakCryptography -v
```

## Using the MCP Server

The server exposes multiple tools through the FastMCP interface. Here are some examples:

### 1. SQL Injection Example

```python
# Normal usage
get_user_data(user_id="1")

# SQL Injection attack
get_user_data(user_id="1 OR 1=1")
get_user_data(user_id="1; DROP TABLE users; --")
```

### 2. Path Traversal Example

```python
# Normal usage
read_file(filename="data.txt")

# Path Traversal attack
read_file(filename="../../etc/passwd")
read_file(filename="../../../home/user/.ssh/id_rsa")
```

### 3. Command Injection Example

```python
# Normal usage
run_system_command(cmd="ls")

# Command Injection attack
run_system_command(cmd="ls; cat /etc/passwd")
run_system_command(cmd="ls && whoami && id")
```

### 4. Authentication Bypass

```python
# SQL Injection in login
login(username="admin' OR '1'='1", password="anything")

# This bypasses authentication and returns admin access
```

### 5. Privilege Escalation

```python
# Any user can make themselves admin
set_user_role(user_id="123", role="admin")

# No authorization check!
```

### 6. Information Disclosure

```python
# Get all system information including credentials
get_system_info()

# Returns:
# - Environment variables
# - Admin credentials
# - API keys
# - Secret keys
```

### 7. Unsafe Deserialization

```python
# Execute arbitrary code via eval
parse_json_unsafe(json_string="__import__('os').system('whoami')")

# Or via pickle
store_user_data(data="malicious_pickle_payload")
```

## Code Review Exercise

Use this codebase to practice identifying vulnerabilities:

1. **Manual Review:**
   - Read through each file in `src/`
   - Try to identify all security issues
   - Compare with `VULNERABILITIES.md`

2. **Automated Tools:**
   - Run Qodo code review
   - Run Bandit: `uv run bandit -r src/`
   - Run pylint: `uv run pylint src/`
   - Compare findings

3. **Exploitation Practice:**
   - Try to exploit each vulnerability
   - Document your findings
   - Propose fixes

## Common Vulnerability Patterns

### Pattern 1: String Formatting in SQL
```python
# VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"

# SECURE
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### Pattern 2: Direct File Access
```python
# VULNERABLE
with open(filename, 'r') as f:
    return f.read()

# SECURE
import os
safe_path = os.path.abspath(os.path.join(base_dir, filename))
if not safe_path.startswith(base_dir):
    raise ValueError("Invalid path")
with open(safe_path, 'r') as f:
    return f.read()
```

### Pattern 3: Command Execution
```python
# VULNERABLE
os.system(command)

# SECURE
import subprocess
subprocess.run([command, arg1, arg2], shell=False, check=True)
```

### Pattern 4: Password Hashing
```python
# VULNERABLE
hashlib.md5(password.encode()).hexdigest()

# SECURE
import bcrypt
bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Pattern 5: Deserialization
```python
# VULNERABLE
pickle.loads(data)
eval(data)

# SECURE
import json
json.loads(data)
```

## Learning Objectives

After working with this codebase, you should be able to:

1. ✅ Identify SQL injection vulnerabilities
2. ✅ Recognize path traversal issues
3. ✅ Spot command injection risks
4. ✅ Understand unsafe deserialization
5. ✅ Identify hardcoded credentials
6. ✅ Recognize missing authentication
7. ✅ Spot information disclosure
8. ✅ Identify weak cryptography
9. ✅ Understand timing attacks
10. ✅ Recognize business logic flaws

## Next Steps

1. Review the code in `src/`
2. Read `VULNERABILITIES.md` for detailed explanations
3. Run the tests to see exploits in action
4. Try to fix one vulnerability at a time
5. Use automated tools to verify your fixes

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Bandit Security Linter](https://bandit.readthedocs.io/)

## Warning

⚠️ **Remember: This code is intentionally insecure!**

- Never use this code in production
- Never deploy this server publicly
- Only use in isolated test environments
- Always practice responsible disclosure
