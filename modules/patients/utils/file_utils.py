import hashlib


def calculate_file_hash(file_content: bytes) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_content)
    return sha256_hash.hexdigest()


def is_duplicate_file_hash(file_hash: str, existing_hashes: list[str]) -> bool:
    return file_hash in existing_hashes
