from dataclasses import dataclass


@dataclass
class UserProfile:
    lang: str = "zh-tw"
    length: int = 200
