import re


def sanitize(input, pattern):
    """Mitigates log injection risks."""
    return re.sub(pattern, "", input)
