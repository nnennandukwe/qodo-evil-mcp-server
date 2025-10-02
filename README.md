# Qodo Evil MCP Server

⚠️ **WARNING: This is an intentionally insecure MCP server for educational purposes only!**

This MCP server is built with deliberate security vulnerabilities and poor coding practices to demonstrate the effectiveness of code review tools like Qodo.

## DO NOT USE IN PRODUCTION

This server contains:
- SQL injection vulnerabilities
- Path traversal vulnerabilities
- Hardcoded credentials
- Unsafe deserialization
- Poor error handling
- Missing input validation
- And many other security issues

## Purpose

This project is designed to showcase how automated code review tools can identify:
- Security vulnerabilities
- Code quality issues
- Anti-patterns
- Best practice violations

## Installation

```bash
uv sync
```

## Running the Server

```bash
uv run python src/server.py
```

## Running Tests

```bash
uv run pytest tests/test_server.py -v
```

## Vulnerability Documentation

See [VULNERABILITIES.md](VULNERABILITIES.md) for a complete catalog of all intentional security issues in this codebase.

## What's Included

### Intentional Vulnerabilities

1. **SQL Injection** - Multiple instances in database operations
2. **Command Injection** - Unsafe system command execution
3. **Path Traversal** - Unvalidated file operations
4. **Unsafe Deserialization** - Using pickle and eval on untrusted data
5. **Hardcoded Credentials** - Passwords and API keys in source code
6. **Missing Authentication** - No authorization checks on sensitive operations
7. **Information Disclosure** - Exposing sensitive data in responses and logs
8. **Weak Cryptography** - MD5 hashing and XOR encryption
9. **Insecure Randomness** - Using random instead of secrets
10. **Poor Error Handling** - Exposing stack traces and internal details
11. **Business Logic Flaws** - Missing validation in critical operations
12. **Resource Exhaustion** - No limits on resource-intensive operations
13. **Race Conditions** - Unsafe concurrent operations
14. **XXE Vulnerabilities** - Unsafe XML parsing
15. **Missing Rate Limiting** - No protection against abuse

### Code Quality Issues

- No type hints on many functions
- Global mutable state
- Poor exception handling
- No input validation
- Debug mode always enabled
- Inadequate sanitization
- Timing attack vulnerabilities

## Project Structure

```
qodo-evil-mcp-server/
├── src/
│   ├── server.py          # Main MCP server with vulnerable tools
│   ├── database.py        # SQL injection vulnerabilities
│   ├── file_operations.py # Path traversal vulnerabilities
│   ├── config.py          # Hardcoded credentials
│   └── utils.py           # Weak crypto and poor practices
├── tests/
│   └── test_server.py     # Tests demonstrating vulnerabilities
├── data/                  # Data directory for database
├── VULNERABILITIES.md     # Complete vulnerability catalog
└── README.md
```

## Usage Examples

⚠️ **DO NOT run these examples on production systems!**

### Example 1: SQL Injection
```python
# Bypass authentication
username = "admin' OR '1'='1"
```

### Example 2: Path Traversal
```python
# Read sensitive files
filename = "../../etc/passwd"
```

### Example 3: Command Injection
```python
# Execute arbitrary commands
cmd = "ls; cat /etc/passwd"
```

See `tests/test_server.py` for more examples.

## License

MIT License - For educational purposes only
