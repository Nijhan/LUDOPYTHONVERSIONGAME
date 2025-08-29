RESERVED_USERNAMES = ["admin", "test", "player", "none"]

def sanitize_username(raw):
    """
    Make a username neat:
    - remove spaces at start/end
    - lowercase it
    - replace inner spaces with underscores
    """
    return raw.strip().lower().replace(" ", "_")


def validate_username(name):
    """
    Check if a username is valid.
    Returns (True, None) if valid, or (False, reason) if invalid.
    """
    # Check length
    if len(name) < 3 or len(name) > 20:
        return False, "Username must be between 3 and 20 characters."

    # Check allowed characters: letters, numbers, _, -
    for ch in name:
        if not (ch.isalnum() or ch in "_-"):
            return False, "Only letters, numbers, _ and - are allowed."

    # Reserved words
    if name in RESERVED_USERNAMES:
        return False, f"'{name}' is not allowed."

    return True, None


def prompt_username(prompt, existing_usernames):
    """
    Ask the user for a username until it's valid and not taken.
    """
    while True:
        raw = input(prompt + ": ")
        username = sanitize_username(raw)
        ok, reason = validate_username(username)

        if not ok:
            print("⚠️ " + reason)
            continue

        if username in existing_usernames:
            print("⚠️ Username already taken in this game.")
            continue

        return username


def prompt_int(prompt, min_v, max_v):
    """
    Ask for a number until it's valid and in range.
    """
    while True:
        raw = input(f"{prompt} ({min_v}-{max_v}): ")
        if not raw.isdigit():
            print("⚠️ Please enter a number.")
            continue

        value = int(raw)
        if value < min_v or value > max_v:
            print(f"⚠️ Number must be between {min_v} and {max_v}.")
            continue

        return value


def prompt_choice(prompt, choices):
    """
    Ask the user to pick one of the given choices.
    """
    choices_str = ", ".join(choices)
    while True:
        value = input(f"{prompt} ({choices_str}): ").strip().lower()
        for choice in choices:
            if value == choice.lower():
                return choice
        print(f"⚠️ Invalid choice. Pick from: {choices_str}")


def prompt_yes_no(prompt):
    """
    Ask the user for a yes/no response.
    """
    while True:
        value = input(f"{prompt} (y/n): ").strip().lower()
        if value in ['y', 'yes']:
            return True
        elif value in ['n', 'no']:
            return False
        print("⚠️ Please enter 'y' for yes or 'n' for no.")
