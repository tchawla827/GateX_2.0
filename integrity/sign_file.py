"""
Usage:
    python integrity/sign_file.py path/to/file.py
Writes <file>.sig alongside <file>.  Exits non-zero on error.
"""
import hashlib
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Path to your private key (must be kept secret)
PRIV_PATH = Path(__file__).with_name("private_key.pem")


def _normalized_bytes(path: Path) -> bytes:
    """
    Read the file and collapse CRLF sequences (\r\n) into LF (\n),
    so signatures created on Windows verify correctly on Linux/macOS.
    """
    return path.read_bytes().replace(b"\r\n", b"\n")


def load_private_key():
    """
    Load the RSA private key, or error if it doesn't exist.
    """
    if not PRIV_PATH.exists():
        raise FileNotFoundError(
            f"🔒 Private key not found at {PRIV_PATH}. "
            "Run generate_keys.py on the signing machine first."
        )
    return serialization.load_pem_private_key(PRIV_PATH.read_bytes(), password=None)


def sign_file(file_path: Path):
    """
    Compute a SHA-256 over the normalized bytes of `file_path`,
    sign it with the private key, and write out <file>.sig.
    """
    # Normalize line endings before hashing
    digest = hashlib.sha256(_normalized_bytes(file_path)).digest()

    private_key = load_private_key()
    signature = private_key.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    sig_path = file_path.with_suffix(file_path.suffix + ".sig")
    sig_path.write_bytes(signature)
    print(f"✅  Signature written to {sig_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python integrity/sign_file.py <file>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"❌  File not found: {target}")
        sys.exit(1)

    sign_file(target)


if __name__ == "__main__":
    main()
