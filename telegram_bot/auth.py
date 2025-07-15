from config import CHATBOT_KEY

# conjunto en memoria de usuarios autenticados
_authenticated_users = set()

def is_authenticated(user_id: int) -> bool:
    return user_id in _authenticated_users

def authenticate(user_id: int, password: str) -> bool:
    if password == CHATBOT_KEY:
        _authenticated_users.add(user_id)
        return True
    return False