# Security Vulnerabilities Catalog

This document catalogs all intentional security vulnerabilities in the Evil MCP Server.

## 🔴 Critical Vulnerabilities

### 1. SQL Injection (Multiple Locations)

**Location:** `src/database.py`, `src/server.py`

**Examples:**
```python
# database.py - Line ~25
query = f"SELECT * FROM users WHERE username = '{username}'"

# server.py - get_user_data tool
query = f"SELECT * FROM users WHERE id = {user_id}"
```

**Exploitation:**
```python
# Bypass authentication
username = "admin' OR '1'='1"

# Drop tables
user_id = "1; DROP TABLE users; --"
```

**Impact:** Complete database compromise, data theft, data destruction

---

### 2. Command Injection

**Location:** `src/server.py`, `src/utils.py`

**Examples:**
```python
# server.py - run_system_command tool
result = os.system(cmd)

# utils.py - execute_command
result = subprocess.run(command, shell=True, capture_output=True, text=True)
```

**Exploitation:**
```python
# Execute arbitrary commands
cmd = "ls; cat /etc/passwd; rm -rf /"
```

**Impact:** Complete system compromise, arbitrary code execution

---

### 3. Path Traversal

**Location:** `src/file_operations.py`, `src/server.py`

**Examples:**
```python
# file_operations.py - read_file
file_path = os.path.join(self.data_dir, filename)
with open(file_path, 'r') as f:
    return f.read()

# server.py - read_file tool
with open(filename, 'r') as f:
    content = f.read()
```

**Exploitation:**
```python
# Read sensitive files
filename = "../../etc/passwd"
filename = "../../../home/user/.ssh/id_rsa"
```

**Impact:** Unauthorized file access, credential theft, system information disclosure

---

### 4. Unsafe Deserialization

**Location:** `src/database.py`, `src/utils.py`, `src/file_operations.py`

**Examples:**
```python
# database.py - load_object
return pickle.loads(result[0][0])

# utils.py - deserialize_data
return eval(data)

# file_operations.py - load_config
return pickle.load(f)
```

**Exploitation:**
```python
# Arbitrary code execution via pickle
import pickle
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))

# Or via eval
data = "__import__('os').system('malicious_command')"
```

**Impact:** Arbitrary code execution, complete system compromise

---

### 5. Hardcoded Credentials

**Location:** `src/config.py`, `src/server.py`

**Examples:**
```python
# config.py
DATABASE_PASSWORD = "admin123"
API_KEY = "sk_live_1234567890abcdef"
SECRET_KEY = "super_secret_key_do_not_share"

# server.py
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"
```

**Impact:** Unauthorized access, credential compromise

---

### 6. Arbitrary Code Execution

**Location:** `src/file_operations.py`

**Examples:**
```python
# file_operations.py - execute_file
with open(file_path, 'r') as f:
    code = f.read()
    eval(code)  # NEVER DO THIS
```

**Impact:** Complete system compromise

---

## 🟠 High Severity Vulnerabilities

### 7. Missing Authentication/Authorization

**Location:** `src/server.py` (all tools)

**Examples:**
```python
@mcp.tool()
def delete_all_users():
    # NO AUTHORIZATION CHECK
    db.execute_query("DELETE FROM users")
    return {"message": "All users deleted"}

@mcp.tool()
def drop_table(table_name: str):
    # EXTREMELY DANGEROUS - no validation or authorization
    query = f"DROP TABLE {table_name}"
```

**Impact:** Unauthorized data access and modification

---

### 8. Information Disclosure

**Location:** `src/server.py`, `src/utils.py`

**Examples:**
```python
# server.py - get_system_info
return {
    "env": dict(os.environ),  # Exposing all environment variables!
    "admin_user": ADMIN_USERNAME,
    "admin_pass": ADMIN_PASSWORD,
    "secret_key": SECRET_KEY,
    "api_key": API_KEY
}

# server.py - login
return {
    "user": user,  # Includes password hash
    "secret_key": SECRET_KEY  # Exposing secret key!
}

# utils.py - log_error
print(f"User data: {user_data}")  # May contain passwords, tokens, etc.
```

**Impact:** Credential theft, system information disclosure

---

### 9. Weak Cryptography

**Location:** `src/utils.py`, `src/config.py`

**Examples:**
```python
# utils.py - hash_password
return hashlib.md5(password.encode()).hexdigest()

# utils.py - encrypt_data (XOR encryption)
encrypted.append(char ^ key[i % len(key)])

# config.py
ENCRYPTION_KEY = b"1234567890123456"  # Predictable key
```

**Impact:** Password cracking, data decryption

---

### 10. Insecure Randomness

**Location:** `src/utils.py`, `src/server.py`

**Examples:**
```python
# utils.py - generate_token
random_part = random.randint(1000, 9999)

# server.py - generate_password_reset_token
token = f"{email}_{random.randint(1000, 9999)}"
```

**Impact:** Token prediction, session hijacking

---

## 🟡 Medium Severity Vulnerabilities

### 11. Timing Attack Vulnerability

**Location:** `src/utils.py`

**Examples:**
```python
# utils.py - verify_password
return hash_password(password) == hashed
```

**Impact:** Password enumeration

---

### 12. Race Conditions

**Location:** `src/server.py`

**Examples:**
```python
# server.py - increment_counter
result = db.execute_query(query)
current_value = result[0][0]
new_value = current_value + 1
# Race condition window here
update_query = f"UPDATE counters SET value = {new_value}"
```

**Impact:** Data inconsistency, business logic bypass

---

### 13. Inadequate Input Validation

**Location:** `src/utils.py`, `src/server.py`

**Examples:**
```python
# utils.py - sanitize_input (blacklist approach)
dangerous = ['<script>', 'DROP TABLE', 'DELETE FROM']
for term in dangerous:
    user_input = user_input.replace(term, '')

# utils.py - validate_email
return '@' in email

# server.py - Most tools have no type hints or validation
def get_user_data(user_id):  # No validation
```

**Impact:** XSS, injection attacks, data corruption

---

### 14. Poor Error Handling

**Location:** `src/server.py`, `src/database.py`

**Examples:**
```python
# server.py - divide_numbers
except Exception as e:
    return {"error": traceback.format_exc()}

# database.py - init_database
except:
    pass  # Silently ignore errors
```

**Impact:** Information disclosure, debugging difficulties

---

### 15. Business Logic Flaws

**Location:** `src/server.py`

**Examples:**
```python
# server.py - transfer_funds
# NO VALIDATION - can transfer negative amounts
# NO AUTHORIZATION - anyone can transfer from any account
# NO BALANCE CHECK

# server.py - set_user_role
# NO AUTHORIZATION - any user can make themselves admin
```

**Impact:** Financial fraud, privilege escalation

---

### 16. Resource Exhaustion

**Location:** `src/server.py`

**Examples:**
```python
# server.py - generate_report
report = "x" * size  # Can cause memory exhaustion

# server.py - recursive_operation
# STACK OVERFLOW - no recursion limit
```

**Impact:** Denial of service

---

### 17. Missing Rate Limiting

**Location:** `src/server.py`, `src/utils.py`

**Examples:**
```python
# server.py - send_email
# NO RATE LIMITING - can be abused for spam

# utils.py - rate_limit_check
return True  # Always returns True
```

**Impact:** Spam, brute force attacks, resource abuse

---

### 18. XXE (XML External Entity) Vulnerability

**Location:** `src/utils.py`

**Examples:**
```python
# utils.py - parse_xml
root = ET.fromstring(xml_string)  # No protection against external entities
```

**Impact:** File disclosure, SSRF, denial of service

---

## 🟢 Low Severity / Code Quality Issues

### 19. Global State Without Synchronization

**Location:** `src/server.py`, `src/database.py`, `src/file_operations.py`

**Examples:**
```python
# server.py
current_user = None
session_tokens = {}

# database.py
db = DatabaseManager()

# file_operations.py
file_manager = FileManager()
```

**Impact:** Thread safety issues, state corruption

---

### 20. Poor Code Practices

**Examples:**
- No type hints on many functions
- Relying on `__del__` for cleanup
- Using `os.system` instead of subprocess
- Silently catching all exceptions
- No logging framework
- No configuration management
- Debug mode always enabled
- Predictable file naming

---

## Exploitation Scenarios

### Scenario 1: Complete System Compromise

1. Use SQL injection to extract admin credentials
2. Use path traversal to read SSH keys
3. Use command injection to establish reverse shell
4. Escalate privileges using exposed credentials

### Scenario 2: Data Exfiltration

1. Use SQL injection to dump entire database
2. Use path traversal to read sensitive files
3. Use information disclosure endpoints to get credentials
4. Use weak encryption to decrypt sensitive data

### Scenario 3: Privilege Escalation

1. Create account with SQL injection
2. Use `set_user_role` to make yourself admin
3. Use admin privileges to access all data
4. Use command injection for system access

### Scenario 4: Denial of Service

1. Use resource exhaustion endpoints
2. Trigger recursive operations
3. Abuse missing rate limiting
4. Cause database corruption with SQL injection

---

## Remediation Guidelines

For each vulnerability type, here's how to fix it:

### SQL Injection
- Use parameterized queries
- Use ORM frameworks
- Validate and sanitize all inputs

### Command Injection
- Never use `shell=True`
- Use subprocess with argument lists
- Validate all inputs against whitelist

### Path Traversal
- Validate file paths
- Use `os.path.abspath()` and check prefix
- Implement access controls

### Unsafe Deserialization
- Never use `pickle` with untrusted data
- Never use `eval()` on user input
- Use JSON or other safe formats

### Hardcoded Credentials
- Use environment variables
- Use secret management systems
- Never commit credentials to code

### Missing Authentication
- Implement proper authentication
- Use JWT or session tokens
- Implement role-based access control

### Weak Cryptography
- Use bcrypt/argon2 for passwords
- Use secrets module for randomness
- Use proper encryption libraries (cryptography)

### Information Disclosure
- Implement proper error handling
- Don't expose stack traces
- Don't log sensitive data
- Use generic error messages

---

## Testing the Vulnerabilities

See `tests/test_server.py` for examples of how to test and demonstrate each vulnerability.

Run tests with:
```bash
uv run pytest tests/test_server.py -v
```

---

## Disclaimer

⚠️ **This code is intentionally insecure and should NEVER be used in production!**

This project is for educational purposes only to demonstrate:
- Common security vulnerabilities
- How code review tools detect issues
- Best practices by showing what NOT to do
