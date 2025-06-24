"""
Runtime verification helper.

Example from app.py:
    from integrity.integrity_check import verify_file_integrity
    if not verify_file_integrity(__file__):
        sys.exit("Integrity check failed. File may be tampered.")
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Path to the repo-committed public key (same folder as this file)
PUB_PATH = Path(__file__).with_name("public_key.pem")


def _normalized_bytes(path: Path) -> bytes:
    """
    Read the file and collapse CRLF sequences (\\r\\n) into LF (\\n),
    so signatures created on Windows verify correctly on Linux/macOS.
    """
    return path.read_bytes().replace(b"\r\n", b"\n")


def verify_file_integrity(
    file_path: str | Path,
    *,
    signature_path: str | Path | None = None,
    public_key_path: str | Path = PUB_PATH,
) -> bool:
    """
    Returns True if `file_path` matches the detached signature at `signature_path`
    using the RSA public key in `public_key_path`.
    """
    file_path       = Path(file_path)
    signature_path  = Path(signature_path or f"{file_path}.sig")
    public_key_path = Path(public_key_path)

    try:
        # Load the public key
        public_key = serialization.load_pem_public_key(public_key_path.read_bytes())

        # Compute SHA-256 over the normalized bytes
        digest = hashlib.sha256(_normalized_bytes(file_path)).digest()

        # Read the signature
        signature = signature_path.read_bytes()

        # Verify the signature
        public_key.verify(
            signature,
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True

    except (FileNotFoundError, InvalidSignature, ValueError):
        return False
