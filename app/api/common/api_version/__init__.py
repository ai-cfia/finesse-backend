from dataclasses import dataclass


@dataclass
class ApiVersion:
    full: str
    release_date: str
    deprecated: bool
    supported_until: str | None = None
