import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import sys

PRIVATE_KEY_PATH = 'private_key.pem'


def generate_key(path=PRIVATE_KEY_PATH):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open(path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open('public_key.pem', 'wb') as f:
        f.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))
    return private_key

def load_private_key(path=PRIVATE_KEY_PATH):
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def sign_file(file_path: str, key_path=PRIVATE_KEY_PATH):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        digest = hashlib.sha256(file_data).digest()
        try:
            private_key = load_private_key(key_path)
        except FileNotFoundError:
            private_key = generate_key(key_path)
        signature = private_key.sign(
            digest,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        with open(f'{file_path}.sig', 'wb') as f:
            f.write(signature)
        print('Signature written to', f'{file_path}.sig')
    except FileNotFoundError:
        print('File not found:', file_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python sign_file.py <file>')
        sys.exit(1)
    sign_file(sys.argv[1])