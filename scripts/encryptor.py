#!/usr/bin/env python3

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt(data: str, passphrase: str) -> bytes:
    """
    Encrypt a string and return it

    Args:
        data: to be encrypted
        passphrase: used to create the Fernet key

    Returns:
        token: a Fernet token with encrypted data

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

    token = f.encrypt(data.encode())
    return token
