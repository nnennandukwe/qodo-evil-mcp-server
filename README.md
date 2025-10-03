# Qodo Evil MCP Server

This project is an MCP server used for demonstration and testing purposes.

## Important Notice

- This repository is not intended for production use.
- It may contain intentionally insecure or low-quality code as part of its educational intent.

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

## Documentation

For additional project notes and context, consult the repository files.

## Project Structure

```
qodo-evil-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main MCP server implementation
│   ├── database.py        # Database operations
│   ├── file_ops.py        # File operation utilities
│   ├── auth.py            # Authentication logic
│   ├── crypto.py          # Cryptographic utilities
│   ├── config.py          # Configuration management
│   └── utils.py           # General utilities
├── tests/
│   ├── __init__.py
│   └── test_server.py     # Server tests
├── data/
│   └── users.db           # User database
├── LICENSE                # MIT License
├── pyproject.toml         # Project configuration
├── uv.lock                # UV lock file
└── README.md              # This file
```

## License

MIT License - For educational purposes only
