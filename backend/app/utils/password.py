import bcrypt
import hashlib

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt directly.
    For passwords longer than 72 bytes, use SHA-256 pre-hashing.
    """
    # Convert to bytes
    password_bytes = password.encode('utf-8')
    
    # If password is too long for bcrypt, pre-hash with SHA-256
    if len(password_bytes) > 72:
        # Pre-hash long passwords with SHA-256
        password_bytes = hashlib.sha256(password_bytes).digest()
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    Handles both normal and pre-hashed passwords.
    """
    # Convert to bytes
    password_bytes = password.encode('utf-8')
    
    # If password is too long for bcrypt, pre-hash with SHA-256
    if len(password_bytes) > 72:
        password_bytes = hashlib.sha256(password_bytes).digest()
    
    # Verify password
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
