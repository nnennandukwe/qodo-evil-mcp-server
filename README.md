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
│   ├── server.py
│   ├── database.py
│   ├── file_operations.py
│   ├── config.py
│   └── utils.py
├── tests/
│   └── test_server.py
├── data/
├── VULNERABILITIES.md
└── README.md
```

## License

MIT License - For educational purposes only
