from dotenv import load_dotenv


def load_env(path: str = ".env") -> None:
    """Load environment variables from a .env file if present."""
    load_dotenv(path)
