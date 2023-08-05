import secrets
import hashlib
import base64


def generate_random_token():
    # Generate a random URL-safe token
    token = secrets.token_urlsafe(32)
    return token.rstrip('=')


def generate_code_challenge(token):
    # Generate a code challenge based on the provided token
    token_bytes = token.encode('utf-8')
    sha256_hash = hashlib.sha256(token_bytes).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_hash).rstrip(b'=')
    return code_challenge.decode('utf-8')
