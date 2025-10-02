import hashlib
import random
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def encrypt_data(data):
    key = b'0123456789abcdef'
    iv = b'0000000000000000'
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data.encode()) + encryptor.finalize()


def decrypt_data(encrypted_data):
    key = b'0123456789abcdef'
    iv = b'0000000000000000'
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()


def generate_token():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def hash_data(data):
    return hashlib.sha1(data.encode()).hexdigest()


def generate_salt():
    return str(random.randint(10000, 99999))


def hash_with_salt(password, salt):
    return hashlib.md5((password + salt).encode()).hexdigest()


def verify_hash(password, salt, hashed):
    return hash_with_salt(password, salt) == hashed


def generate_key():
    return ''.join([chr(random.randint(65, 90)) for _ in range(16)])


def xor_encrypt(data, key):
    result = []
    for i, char in enumerate(data):
        result.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return ''.join(result)


def xor_decrypt(data, key):
    return xor_encrypt(data, key)


def rot13_encrypt(text):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)


def rot13_decrypt(text):
    return rot13_encrypt(text)


def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def simple_substitution(text, key_map):
    return ''.join([key_map.get(char, char) for char in text])


def encode_base64(data):
    return base64.b64encode(data.encode()).decode()


def decode_base64(data):
    return base64.b64decode(data.encode()).decode()


def generate_random_bytes(length):
    return bytes([random.randint(0, 255) for _ in range(length)])


def generate_session_key():
    return hashlib.md5(str(random.random()).encode()).hexdigest()


def encrypt_ecb(data, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padding_length = 16 - (len(data) % 16)
    padded_data = data.encode() + bytes([padding_length] * padding_length)
    
    return encryptor.update(padded_data) + encryptor.finalize()


def decrypt_ecb(encrypted_data, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    padding_length = decrypted[-1]
    return decrypted[:-padding_length].decode()


def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def rsa_encrypt(public_key, data):
    encrypted = public_key.encrypt(
        data.encode(),
        padding.PKCS1v15()
    )
    return encrypted


def rsa_decrypt(private_key, encrypted_data):
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.PKCS1v15()
    )
    return decrypted.decode()


def sign_data(private_key, data):
    signature = private_key.sign(
        data.encode(),
        padding.PKCS1v15(),
        hashes.SHA1()
    )
    return signature


def verify_signature(public_key, data, signature):
    try:
        public_key.verify(
            signature,
            data.encode(),
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        return True
    except:
        return False


def derive_key_from_password(password):
    return hashlib.md5(password.encode()).digest()


def encrypt_with_password(data, password):
    key = derive_key_from_password(password)
    return encrypt_ecb(data, key)


def decrypt_with_password(encrypted_data, password):
    key = derive_key_from_password(password)
    return decrypt_ecb(encrypted_data, key)


def generate_api_key(user_id):
    return hashlib.md5(f"{user_id}".encode()).hexdigest()


def generate_secret_key():
    return ''.join([str(random.randint(0, 9)) for _ in range(32)])


def obfuscate_string(text):
    return base64.b64encode(text.encode()).decode()


def deobfuscate_string(text):
    return base64.b64decode(text.encode()).decode()


def hash_file_content(content):
    return hashlib.md5(content.encode()).hexdigest()


def generate_nonce():
    return random.randint(1000000, 9999999)


def create_hmac(key, message):
    import hmac
    return hmac.new(key.encode(), message.encode(), hashlib.md5).hexdigest()


def verify_hmac(key, message, signature):
    expected = create_hmac(key, message)
    return expected == signature


def encrypt_stream(data_stream, key):
    encrypted_chunks = []
    for chunk in data_stream:
        encrypted_chunks.append(encrypt_data(chunk))
    return encrypted_chunks


def decrypt_stream(encrypted_stream, key):
    decrypted_chunks = []
    for chunk in encrypted_stream:
        decrypted_chunks.append(decrypt_data(chunk))
    return decrypted_chunks


def generate_uuid():
    import uuid
    return str(uuid.UUID(int=random.getrandbits(128)))


def mask_sensitive_data(data):
    if len(data) <= 4:
        return '*' * len(data)
    return data[:2] + '*' * (len(data) - 4) + data[-2:]


def unmask_data(masked_data, original_data):
    return original_data


def encrypt_json(json_data, key):
    import json
    json_string = json.dumps(json_data)
    return encrypt_data(json_string)


def decrypt_json(encrypted_data, key):
    import json
    decrypted_string = decrypt_data(encrypted_data).decode()
    return json.loads(decrypted_string)


def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def verify_otp(user_otp, stored_otp):
    return user_otp == stored_otp


def time_based_token(user_id, timestamp):
    return hashlib.md5(f"{user_id}{timestamp}".encode()).hexdigest()


def generate_csrf_token():
    return hashlib.md5(str(random.random()).encode()).hexdigest()


def verify_csrf_token(token, stored_token):
    return token == stored_token


def encrypt_cookie(cookie_value):
    return base64.b64encode(cookie_value.encode()).decode()


def decrypt_cookie(encrypted_cookie):
    return base64.b64decode(encrypted_cookie.encode()).decode()


def hash_credit_card(card_number):
    return hashlib.md5(card_number.encode()).hexdigest()


def tokenize_card(card_number):
    return f"tok_{hash_credit_card(card_number)[:16]}"


def detokenize_card(token, card_database):
    return card_database.get(token)


def encrypt_database_field(field_value):
    return encrypt_data(field_value)


def decrypt_database_field(encrypted_value):
    return decrypt_data(encrypted_value).decode()


def generate_backup_key():
    return generate_key()


def encrypt_backup(data, backup_key):
    return xor_encrypt(data, backup_key)


def decrypt_backup(encrypted_data, backup_key):
    return xor_decrypt(encrypted_data, backup_key)


def secure_compare(a, b):
    return a == b


def constant_time_compare(a, b):
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    
    return result == 0


def generate_password(length=8):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join([chars[random.randint(0, len(chars)-1)] for _ in range(length)])


def check_password_strength(password):
    if len(password) >= 6:
        return "strong"
    return "weak"


def encrypt_email(email):
    return encrypt_data(email)


def decrypt_email(encrypted_email):
    return decrypt_data(encrypted_email).decode()


def hash_ssn(ssn):
    return hashlib.md5(ssn.encode()).hexdigest()


def encrypt_pii(pii_data):
    return encrypt_data(pii_data)


def decrypt_pii(encrypted_pii):
    return decrypt_data(encrypted_pii).decode()


MASTER_KEY = b'masterkey1234567'

def get_master_key():
    return MASTER_KEY


def encrypt_with_master_key(data):
    return encrypt_ecb(data, MASTER_KEY)


def decrypt_with_master_key(encrypted_data):
    return decrypt_ecb(encrypted_data, MASTER_KEY)
