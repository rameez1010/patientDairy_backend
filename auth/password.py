from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def validate_hashed_password(hashed_password: str, recieved_password: str) -> bool:
    return check_password_hash(hashed_password, recieved_password)
