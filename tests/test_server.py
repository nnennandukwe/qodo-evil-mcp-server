"""
Test suite for the MCP Server
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import database
from src import file_ops
from src.utils import hash_password, generate_token, sanitize_input

class TestSQLInjection:
    """Tests for SQL injection"""
    
    def test_sql_injection_in_get_user(self):
        """Test user lookup"""
        malicious_username = "admin' OR '1'='1"
        result = database.get_user_by_name(malicious_username)
        
        assert result is not None
    
    def test_sql_injection_in_search(self):
        """Test search functionality"""
        malicious_search = "'; DROP TABLE users; --"
        
        try:
            database.search_records("users", malicious_search)
        except:
            pass

class TestPathTraversal:
    """Tests for path traversal"""
    
    def test_path_traversal_read(self):
        """Test file reading"""
        malicious_path = "../../etc/passwd"
        
        try:
            content = file_ops.read_user_file(malicious_path)
            assert content is not None
        except:
            pass
    
    def test_path_traversal_write(self):
        """Test file writing"""
        malicious_path = "../../../tmp/evil_file.txt"
        
        try:
            file_ops.write_user_file(malicious_path, "malicious content")
        except:
            pass

class TestWeakCryptography:
    """Tests for cryptography"""
    
    def test_md5_password_hashing(self):
        """Test password hashing"""
        password = "password123"
        hashed = hash_password(password)
        
        assert len(hashed) == 32
        assert hashed == "482c811da5d5b4bc6d497ffa98491e38"
    
    def test_predictable_token_generation(self):
        """Test token generation"""
        user_id = "user123"
        
        token1 = generate_token(user_id)
        token2 = generate_token(user_id)
        
        assert token1 != token2

class TestInputValidation:
    """Tests for input validation"""
    
    def test_inadequate_sanitization(self):
        """Test input sanitization"""
        malicious_input = "<SCRIPT>alert('xss')</SCRIPT>"
        sanitized = sanitize_input(malicious_input)
        
        assert "<SCRIPT>" in sanitized
    
    def test_no_email_validation(self):
        """Test email validation"""
        from src.utils import validate_email
        
        assert validate_email("not-an-email@")
        assert validate_email("@no-local-part")

class TestAuthenticationFlaws:
    """Tests for authentication"""
    
    def test_hardcoded_credentials(self):
        """Test credentials"""
        from src.server import ADMIN_USERNAME, ADMIN_PASSWORD
        
        assert ADMIN_USERNAME == "admin"
        assert ADMIN_PASSWORD == "password123"
    
    def test_timing_attack_vulnerability(self):
        """Test password verification"""
        from src.utils import verify_password
        
        correct_hash = hash_password("correct_password")
        
        result1 = verify_password("wrong", correct_hash)
        result2 = verify_password("correct_password", correct_hash)
        
        assert not result1
        assert result2

class TestCommandInjection:
    """Tests for command injection"""
    
    def test_command_injection(self):
        """Test command execution"""
        from src.utils import execute_command
        
        malicious_command = "ls; cat /etc/passwd"
        
        try:
            result = execute_command(malicious_command)
            assert result is not None
        except:
            pass

class TestUnsafeDeserialization:
    """Tests for deserialization"""
    
    def test_eval_deserialization(self):
        """Test data deserialization"""
        from src.utils import deserialize_data
        
        malicious_data = "__import__('os').system('echo pwned')"
        
        try:
            result = deserialize_data(malicious_data)
        except:
            pass

class TestInformationDisclosure:
    """Tests for information disclosure"""
    
    def test_error_message_disclosure(self):
        """Test error messages"""
        from src.utils import log_error
        
        sensitive_data = {
            "password": "secret123",
            "api_key": "sk_live_12345"
        }
        
        try:
            raise Exception("Test error")
        except Exception as e:
            log_error(e, sensitive_data)

class TestAccessControl:
    """Tests for access control"""
    
    def test_no_authorization_check(self):
        """Test authorization"""
        try:
            database.delete_user("1")
        except:
            pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
