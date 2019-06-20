import bcrypt


def encrypt(value) -> bytes:
    encoded = str(value).encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded, salt)


def equals_to_encrypted(value, encrypted_value):
    value = str(value).encode()
    return bcrypt.checkpw(value, encrypted_value)