#!/usr/bin/env python3
import argparse
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_private_key, load_pem_private_key

def sign_challenge(challenge: str, private_key_b64: str) -> str:
    private_key_bytes = base64.b64decode(private_key_b64)

    try:
        private_key = load_der_private_key(
            private_key_bytes, 
            password=None, 
            backend=default_backend()
        )
    except Exception:
        try:
            private_key = load_pem_private_key(
                private_key_bytes, 
                password=None, 
                backend=default_backend()
            )
        except Exception as e:
            raise ValueError(f"Failed to load private key: {str(e)}")

    signature = private_key.sign(
        challenge.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    signed_challenge = base64.b64encode(signature).decode('utf-8')

    return signed_challenge

def main():
    parser = argparse.ArgumentParser(description='Sign a challenge string with an RSA private key')
    parser.add_argument('--private_key', required=True, help='Base64 encoded RSA 2048 private key')
    parser.add_argument('--challenge', required=True, help='Challenge string to sign')

    args = parser.parse_args()

    try:
        signed_challenge = sign_challenge(args.challenge, args.private_key)
        print(signed_challenge)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()