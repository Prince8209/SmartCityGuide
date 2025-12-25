"""
Input Validators
Common validation functions
"""
import re

def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    # RFC 5322 compliant regex
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, ""

def validate_password(password):
    """
    Validate password strength
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
        
    return True, ""

def validate_username(username):
    """Validate username"""
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers and underscores"
        
    return True, ""

def validate_phone(phone):
    """Validate phone number"""
    if not phone:
        return False, "Phone number is required"
    
    # Basic international format validation
    # Allows: +1234567890, 123-456-7890, (123) 456-7890
    pattern = r"^(\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}$"
    if not re.match(pattern, phone) and not phone.isdigit():
        return False, "Invalid phone number format"
        
    return True, ""

def validate_name(name):
    """Validate full name"""
    if not name:
        return False, "Name is required"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    if not re.match(r"^[a-zA-Z\s.-]+$", name):
        return False, "Name contains invalid characters"
        
    return True, ""

def sanitize_string(s, max_length=None):
    """Sanitize string input"""
    if not s:
        return ""
    
    # Remove leading/trailing whitespace
    s = str(s).strip()
    
    # Truncate if too long
    if max_length and len(s) > max_length:
        s = s[:max_length]
        
    return s
