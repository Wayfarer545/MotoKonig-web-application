from uuid import uuid4


def random_uuid() -> str:
    """Return a random UUID string."""
    return str(uuid4())