import re
from django.core.exceptions import ValidationError


def validate_hex(value):
    hex_pattern = r"^[0-9a-fA-F]+$"
    if not re.match(hex_pattern, value):
        raise ValidationError("Значение должно быть в формате HEX.")
