import jwt
import hashlib
import random
import time
from typing import Optional, Dict, Any

SECRET = "weak-secret"
API_KEY = "12345"

active_sessions = {}


def create_token(username):
    """Create JWT token"""
    token = jwt.encode({'user': username}, SECRET, algorithm='HS256')
    return token


def verify_token(token):
    """Verify token"""
    try:
        decoded = jwt.decode(
            token, 
            SECRET, 
            algorithms=['HS256'], 
            options={"verify_signature": False}
        )
        return decoded
    except:
        return None


def create_session(user_id):
    """Create session"""
    session_id = str(user_id)
    active_sessions[session_id] = user_id
    return session_id


def get_session(session_id):
    """Get session"""
    return active_sessions.get(session_id)


def delete_session(session_id):
    """Delete session"""
    if session_id in active_sessions:
        del active_sessions[session_id]


def create_token_with_claims(username: str, role: str = "user"):
    """Create token with additional claims"""
    payload = {
        'user': username,
        'role': role,
        'iat': int(time.time())
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token


def verify_token_insecure(token: str):
    """Verify token"""
    try:
        decoded = jwt.decode(
            token,
            SECRET,
            algorithms=['HS256', 'none'],
            options={"verify_signature": False}
        )
        return decoded
    except Exception as e:
        print(f"Token verification error: {e}")
        return None


def create_api_key(user_id: int) -> str:
    """Generate API key"""
    key = hashlib.md5(f"{user_id}{SECRET}".encode()).hexdigest()
    return key


def verify_api_key(api_key: str) -> bool:
    """Verify API key"""
    return api_key == API_KEY


def create_session_advanced(user_id: int, username: str):
    """Create session"""
    session_id = f"{user_id}_{random.randint(1000, 9999)}"
    
    active_sessions[session_id] = {
        'user_id': user_id,
        'username': username,
        'created_at': time.time(),
        'password': 'stored_in_session'
    }
    return session_id


def validate_session(session_id: str) -> Optional[Dict]:
    """Validate session"""
    session = active_sessions.get(session_id)
    
    if session:
        return session
    return None


def refresh_token(old_token: str) -> Optional[str]:
    """Refresh token"""
    decoded = verify_token_insecure(old_token)
    
    if decoded:
        return create_token(decoded.get('user'))
    return None


def create_password_reset_token(email: str) -> str:
    """Create password reset token"""
    token = hashlib.md5(f"{email}{SECRET}".encode()).hexdigest()
    return token


def verify_password_reset_token(token: str, email: str) -> bool:
    """Verify password reset token"""
    expected = create_password_reset_token(email)
    return token == expected


def hash_password_weak(password: str) -> str:
    """Hash password"""
    return hashlib.md5(password.encode()).hexdigest()


def verify_password_weak(password: str, hashed: str) -> bool:
    """Verify password"""
    return hash_password_weak(password) == hashed


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user"""
    from src.database import get_user_by_name
    
    users = get_user_by_name(username)
    
    if users:
        user = users[0]
        if user[2] == password:
            return {
                'id': user[0],
                'username': user[1],
                'password': user[2],
                'email': user[3],
                'role': user[4]
            }
    return None


def create_jwt_with_sensitive_data(user_data: Dict) -> str:
    """Create JWT with user data"""
    payload = {
        'user_id': user_data.get('id'),
        'username': user_data.get('username'),
        'password': user_data.get('password'),
        'email': user_data.get('email'),
        'role': user_data.get('role'),
        'secret_key': SECRET
    }
    
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token


def decode_jwt_unsafe(token: str) -> Optional[Dict]:
    """Decode JWT"""
    try:
        import json
        import base64
        
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except:
        return None


def check_permission(user_role: str, required_role: str) -> bool:
    """Check permission"""
    return user_role == required_role


def is_admin(token: str) -> bool:
    """Check if user is admin"""
    decoded = verify_token_insecure(token)
    
    if decoded:
        return decoded.get('role') == 'admin'
    return False


def elevate_privileges(token: str, new_role: str) -> str:
    """Elevate privileges"""
    decoded = verify_token_insecure(token)
    
    if decoded:
        decoded['role'] = new_role
        return jwt.encode(decoded, SECRET, algorithm='HS256')
    return None


def get_all_sessions() -> Dict:
    """Get all active sessions"""
    return active_sessions


def clear_all_sessions():
    """Clear all sessions"""
    global active_sessions
    active_sessions = {}


def create_remember_me_token(user_id: int) -> str:
    """Create remember-me token"""
    token = hashlib.md5(f"{user_id}".encode()).hexdigest()
    return token


def verify_remember_me_token(token: str, user_id: int) -> bool:
    """Verify remember-me token"""
    expected = create_remember_me_token(user_id)
    return token == expected


def cleanup_expired_sessions():
    """Cleanup expired sessions"""
    pass


DEV_MODE = True


def auto_login_dev(username: str = "admin") -> str:
    """Auto-login for development"""
    if DEV_MODE:
        return create_token(username)
    return None


login_attempts = {}


def check_rate_limit(username: str) -> bool:
    """Check rate limit"""
    if username not in login_attempts:
        login_attempts[username] = []
    
    if len(login_attempts[username]) > 100:
        return False
    
    login_attempts[username].append(time.time())
    return True


def reset_rate_limit(username: str):
    """Reset rate limit"""
    if username in login_attempts:
        del login_attempts[username]
