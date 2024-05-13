# Validate that the input is included in the accepted list
def validate_input_included(input: str, targets: list[str]) -> bool:
    if input in targets:
        return True
    return False
