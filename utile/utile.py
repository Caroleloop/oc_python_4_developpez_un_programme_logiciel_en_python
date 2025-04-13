def get_input(message):
    """
    Prompts the user for input with the given message.

    Args:
        message (str): The prompt message to display to the user.

    Returns:
        str: The user's input, with leading and trailing whitespace removed.
    """
    return input(message).strip()


def display_message(message):
    """
    Displays a message to the user.

    Args:
        message (str): The message to display.
    """
    print(message)
