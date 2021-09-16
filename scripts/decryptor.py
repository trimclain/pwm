#!/usr/bin/env python3

import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def decrypt(token: bytes, passphrase: str) -> str:
    """
    Read an encrypted data from a file and decrypt it

    Args:
        token: encrypted data
        passphrase: used to create the Fernet key

    Returns:
        data: decrypted data

    Raises:
        None
    """
    passphrase_bytes = passphrase.encode()   # convert string to bytes

    # salt = os.urandom(16)
    # TODO: Gotta figure out how to properly store this so I can decrypt
    salt = b'\xe0\xfd\xe6\xbc\xd2\x1e\xed\x1a\xab\x10!\xf1~\xc3$\xd9'
    kdf = PBKDF2HMAC(   # Password Based Key Derivation Function 2 HMAC
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(passphrase_bytes))

    f = Fernet(key)

    try:
        data = f.decrypt(token)
        return data.decode()
    except InvalidToken:
        return 'Wrong passphrase! Try again'
