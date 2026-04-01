# ABOUTME: Cryptographically secure secret generation.
# ABOUTME: Generates random strings with configurable character sets and length.

import secrets
import string


AMBIGUOUS_CHARS = set("IOl01")


def generate_secret(
    length: int = 24,
    avoid_ambiguous: bool = True,
    lowercase: bool = True,
    uppercase: bool = True,
    numbers: bool = True,
    special: bool = True,
) -> str:
    """Generate a cryptographically secure random string."""
    if length < 1:
        raise ValueError("Length must be at least 1")

    alphabet = ""
    if lowercase:
        alphabet += string.ascii_lowercase
    if uppercase:
        alphabet += string.ascii_uppercase
    if numbers:
        alphabet += string.digits
    if special:
        alphabet += "!@#$%^&*"

    if not alphabet:
        raise ValueError("At least one character set must be enabled")

    if avoid_ambiguous:
        alphabet = "".join(c for c in alphabet if c not in AMBIGUOUS_CHARS)

    return "".join(secrets.choice(alphabet) for _ in range(length))
