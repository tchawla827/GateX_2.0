import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqJwiFhXToEropkCl1rt0
uGv7szeNL/EdypI3qXcP5HKA5oXd4znpRWTJcN4VAuSMFMqLjZarKLa85SDZgZbC
RiB6UxDH9Zals5zkO7Ky0zacxBPuLpoOevtrhpKfFyyNfilWyjcpGtZYKknw44lR
DNOzqlGageGutsk26XdVUmSbzben2c7GX8OlXHxRIbvqyZ72lK2dam652w5N7T79
Hcko/EAeUADnbWNjFhUBKIFY87OH9Ourb1JgBeS3mE/JC42r3WHdyY65tOKHLXls
q4VEJyuJUDJEadh2z9IKL9g+lJv2YxZpepxjvi516kwBobrkPtdwUwCnR+SXRGth
4QIDAQAB
-----END PUBLIC KEY-----"""

def verify_file_integrity(file_path: str, signature_path: str = None) -> bool:
    """Verify that the file at ``file_path`` matches the embedded signature."""
    if signature_path is None:
        signature_path = f"{file_path}.sig"

    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
        digest = hashlib.sha256(file_data).digest()
        with open(signature_path, "rb") as f:
            signature = f.read()
        public_key = serialization.load_pem_public_key(PUBLIC_KEY)
        public_key.verify(
            signature,
            digest,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except (FileNotFoundError, InvalidSignature, ValueError):
        return False

