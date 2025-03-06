#!/usr/bin/env python3
import argparse
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_public_key, load_pem_public_key

def verify_signature(challenge: str, signed_challenge: str, public_key_b64: str) -> bool:
    # Decode the base64 public key
    public_key_bytes = base64.b64decode(public_key_b64)
    
    # Try to load the public key (attempt both DER and PEM formats)
    try:
        public_key = load_der_public_key(
            public_key_bytes, 
            backend=default_backend()
        )
    except Exception:
        try:
            public_key = load_pem_public_key(
                public_key_bytes, 
                backend=default_backend()
            )
        except Exception as e:
            raise ValueError(f"Failed to load public key: {str(e)}")
    
    # Decode the base64 signature
    try:
        signature = base64.b64decode(signed_challenge)
    except Exception as e:
        raise ValueError(f"Failed to decode signature: {str(e)}")
    
    # Verify the signature
    try:
        public_key.verify(
            signature,
            challenge.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        raise ValueError(f"Error during verification: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Verify a challenge signature with an RSA public key')
    parser.add_argument('--public_key', required=True, help='Base64 encoded RSA 2048 public key')
    parser.add_argument('--challenge', required=True, help='Original challenge string')
    parser.add_argument('--signature', required=True, help='Base64 encoded signature to verify')

    args = parser.parse_args()

    try:
        is_valid = verify_signature(args.challenge, args.signature, args.public_key)
        if is_valid:
            print("✅ Signature is valid!")
        else:
            print("❌ Invalid signature!")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()