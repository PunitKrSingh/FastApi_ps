from passlib.context import CryptContext
from passlib.exc import PasslibSecurityError


pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash(password: str):
    try:
        hashed_password = pwd_context.hash(password)
        return hashed_password
    except PasslibSecurityError as e:        
        print(f"Error occurred during password hashing: {e}")
        return None
    
def verify(password,hashed_password):
    return pwd_context.verify(password,hashed_password)