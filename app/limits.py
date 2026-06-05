from dataclasses import dataclass


@dataclass
class LIMITS:
    """Clas containing limits for the length of attributes of various models"""
    word_min_length: int = 1
    word_max_length: int = 1000
    script_family_name_min: int = 1
    script_family_name_max: int = 500
