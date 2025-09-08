# a function that check if the input is not an escape sequence or a null input
def is_valid_input(user_input: str) -> bool:
    # Check for empty input
    if not user_input.strip():
        return False

    escape_sequences = ["\x1b", "\x00", "\r", "\t", "\x03"]
    for seq in escape_sequences:
        if seq in user_input:
            return False
        
    return True