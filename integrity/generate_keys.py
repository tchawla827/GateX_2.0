"""
Run once to create a 2048-bit RSA key pair:

    python integrity/generate_keys.py

It writes:
  • private_key.pem   – keep **only** on the machine that signs code
  • public_key.pem    – commit this to the repo so everyone can verify
"""
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pathlib import Path

PRIV_PATH = Path(__file__).with_name("private_key.pem")
PUB_PATH  = Path(__file__).with_name("public_key.pem")

def main():
    if PRIV_PATH.exists() or PUB_PATH.exists():
        raise RuntimeError("Key pair already exists; delete first if you really "
                           "want to regenerate.")

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    PRIV_PATH.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

    PUB_PATH.write_bytes(
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )

    print(f"✅  Created {PRIV_PATH} and {PUB_PATH}")

if __name__ == "__main__":
    main()
