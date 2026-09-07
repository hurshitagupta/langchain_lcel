MAX_INPUT_WORDS = 100


def validate_input(data: dict) -> dict:
    if "q" not in data:
        raise ValueError("Missing required field: q")

    if not isinstance(data["q"], str):
        raise ValueError("q must be a string")

    if not data["q"].strip():
        raise ValueError("q cannot be empty")

    return data


def check_token_budget(data: dict) -> dict:
    word_count = len(data["q"].split())

    if word_count > MAX_INPUT_WORDS:
        raise ValueError("Token budget exceeded")

    return data


def validate_output(output: str) -> str:
    if not isinstance(output, str) or not output.strip():
        raise ValueError("Invalid model output")

    return output