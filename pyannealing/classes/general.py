from enum import Enum

class Engine(Enum):
    PYTHON = 'Python'
    RUST = 'Rust'

    @classmethod
    def from_string(cls, input_string: str):
        """
        Basic conversion method for mapping strings to values
        """
        string_map: dict = {
            'python': cls.PYTHON,
            'rust': cls.RUST,
        }
        if (pattern_match := string_map.get(input_string.lower().strip())):
            return pattern_match
        else:
            raise ValueError(f'No Pattern with the value: {input_string}')