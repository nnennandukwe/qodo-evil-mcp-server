# Qodo Evil MCP Server

Warning: This repository contains intentionally insecure and low-quality code created for educational and testing purposes. Do not deploy or use this project in production environments.

## Purpose

This project exists to support demonstrations of automated code review and security tooling.

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
├── README.md
└── LICENSE
```

## Notes

- This codebase intentionally contains flawed patterns for demonstration only.
- Keep this repository private and isolated from production systems.

## License

MIT License - For educational purposes only.
