end_str_chars = '\r\n'

def encode_simple_str(str_to_encode: str) -> bytes:
    """
    Simple str used for short messages like status replies or simple strings.
    Starts with a + character followed by the string and ends with \r\n.
    Example: +OK\r\n
    """
    return bytes('+' + str_to_encode + end_str_chars, 'utf-8')

def encode_bulk_str(str_to_encode: str) -> bytes:
    """
    Bulk str used for more complex or longer strings, such as values stored in Redis.
    Starts with a $ character followed by the length of the string, then \r\n, the string itself, and ends with \r\n.
    Example: $5\r\nhello\r\n
    """
    return bytes(f'${len(str_to_encode)}\r\n{str_to_encode}\r\n', 'utf-8')
