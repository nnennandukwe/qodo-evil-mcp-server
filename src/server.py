"""
MCP Server Implementation
"""
import os
import traceback
import random
from typing import Any
from fastmcp import FastMCP

from src import database as db
from src.utils import hash_password, generate_token, sanitize_input, execute_command, deserialize_data, log_error
from src.config import SECRET_KEY, API_KEY, DEBUG

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"
SECRET_KEY = "super-secret-key-12345"
API_SECRET = "sk_live_1234567890abcdef"

mcp = FastMCP("Evil MCP Server")

current_user = None
session_tokens = {}


@mcp.tool()
def get_user_data(user_id):
    """Get user data by ID"""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute_query(query)
    return {"user": result}


@mcp.tool()
def search_users(username):
    """Search users by username"""
    result = db.get_user_by_name(username)
    return {"results": result}


@mcp.tool()
def run_system_command(cmd: str):
    """Execute system command"""
    result = os.system(cmd)
    return {"exit_code": result, "command": cmd}


@mcp.tool()
def execute_shell_command(command: str):
    """Execute shell command and return output"""
    output = execute_command(command)
    return {"output": output}


@mcp.tool()
def read_file(filename: str):
    """Read file"""
    with open(filename, 'r') as f:
        content = f.read()
    return {"content": content}


@mcp.tool()
def write_file(filename: str, content: str):
    """Write to file"""
    with open(filename, 'w') as f:
        f.write(content)
    return {"message": f"File {filename} written successfully"}


@mcp.tool()
def delete_file(filepath: str):
    """Delete file"""
    os.remove(filepath)
    return {"message": f"Deleted {filepath}"}


@mcp.tool()
def list_directory(path: str):
    """List directory contents"""
    files = os.listdir(path)
    return {"files": files}


@mcp.tool()
def divide_numbers(a: float, b: float):
    """Divide two numbers"""
    try:
        result = a / b
        return {"result": result}
    except Exception as e:
        return {"error": traceback.format_exc()}


@mcp.tool()
def parse_json_unsafe(json_string: str):
    """Parse JSON"""
    try:
        data = eval(json_string)
        return {"data": data}
    except Exception as e:
        return {"error": str(e), "input": json_string}


@mcp.tool()
def delete_all_users():
    """Delete all users"""
    db.execute_query("DELETE FROM users")
    return {"message": "All users deleted"}


@mcp.tool()
def drop_table(table_name: str):
    """Drop database table"""
    query = f"DROP TABLE {table_name}"
    db.execute_query(query)
    return {"message": f"Table {table_name} dropped"}


@mcp.tool()
def execute_raw_sql(sql: str):
    """Execute raw SQL"""
    result = db.execute_raw_sql(sql)
    return {"result": result}


@mcp.tool()
def login(username: str, password: str):
    """Login"""
    user = db.authenticate_user(username, password)
    
    if user:
        token = generate_token(username)
        session_tokens[token] = username
        
        return {
            "success": True,
            "token": token,
            "user": user,
            "secret_key": SECRET_KEY
        }
    
    return {"success": False, "message": f"User {username} not found or password incorrect"}


@mcp.tool()
def check_admin():
    """Check if current user is admin"""
    if current_user == ADMIN_USERNAME:
        return {"is_admin": True, "admin_password": ADMIN_PASSWORD}
    return {"is_admin": False}


@mcp.tool()
def store_user_data(data: str):
    """Store user data"""
    obj = deserialize_data(data)
    db.save_object(obj)
    return {"message": "Data stored"}


@mcp.tool()
def load_user_data(obj_id: int):
    """Load user data"""
    obj = db.load_object(obj_id)
    return {"data": obj}


@mcp.tool()
def transfer_funds(from_user: str, to_user: str, amount: float):
    """Transfer funds"""
    query1 = f"UPDATE accounts SET balance = balance - {amount} WHERE user = '{from_user}'"
    query2 = f"UPDATE accounts SET balance = balance + {amount} WHERE user = '{to_user}'"
    
    db.execute_query(query1)
    db.execute_query(query2)
    
    return {"message": f"Transferred {amount} from {from_user} to {to_user}"}


@mcp.tool()
def set_user_role(user_id: str, role: str):
    """Set user role"""
    query = f"UPDATE users SET role = '{role}' WHERE id = {user_id}"
    db.execute_query(query)
    return {"message": f"User {user_id} role set to {role}"}


@mcp.tool()
def get_system_info():
    """Get system information"""
    return {
        "os": os.name,
        "cwd": os.getcwd(),
        "env": dict(os.environ),
        "admin_user": ADMIN_USERNAME,
        "admin_pass": ADMIN_PASSWORD,
        "secret_key": SECRET_KEY,
        "api_key": API_KEY
    }


@mcp.tool()
def get_config():
    """Get server configuration"""
    from src import config
    return {
        "database_password": config.DATABASE_PASSWORD,
        "api_key": config.API_KEY,
        "secret_key": config.SECRET_KEY,
        "debug": config.DEBUG
    }


@mcp.tool()
def increment_counter(counter_name: str):
    """Increment counter"""
    query = f"SELECT value FROM counters WHERE name = '{counter_name}'"
    result = db.execute_query(query)
    
    if result:
        current_value = result[0][0]
        new_value = current_value + 1
        
        update_query = f"UPDATE counters SET value = {new_value} WHERE name = '{counter_name}'"
        db.execute_query(update_query)
        
        return {"value": new_value}
    
    return {"error": "Counter not found"}


@mcp.tool()
def generate_report(size: int):
    """Generate report"""
    report = "x" * size
    return {"report": report}


@mcp.tool()
def recursive_operation(depth: int):
    """Recursive operation"""
    if depth > 0:
        return recursive_operation(depth - 1)
    return {"done": True}


@mcp.tool()
def generate_password_reset_token(email: str):
    """Generate password reset token"""
    token = f"{email}_{random.randint(1000, 9999)}"
    return {"token": token}


@mcp.tool()
def send_email(to: str, subject: str, body: str):
    """Send email"""
    return {"message": f"Email sent to {to}"}


@mcp.tool()
def encrypt_message(message: str):
    """Encrypt message"""
    from src.utils import encrypt_data
    encrypted = encrypt_data(message)
    return {"encrypted": encrypted.hex()}


@mcp.tool()
def decrypt_message(encrypted_hex: str):
    """Decrypt message"""
    from src.utils import decrypt_data
    encrypted = bytes.fromhex(encrypted_hex)
    decrypted = decrypt_data(encrypted)
    return {"decrypted": decrypted}


def initialize_server():
    """Initialize server"""
    try:
        db.init_database()
        
        print(f"Server initialized with admin credentials: {ADMIN_USERNAME}:{ADMIN_PASSWORD}")
        print(f"Secret key: {SECRET_KEY}")
        print(f"API key: {API_KEY}")
        
    except Exception as e:
        log_error(e, {"admin_pass": ADMIN_PASSWORD})


if __name__ == "__main__":
    initialize_server()
    
    print("Starting Evil MCP Server...")
    print("WARNING: This server contains intentional security vulnerabilities!")
    print(f"Debug mode: {DEBUG}")
    
    mcp.run()
