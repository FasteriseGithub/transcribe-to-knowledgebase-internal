import re

def detect_string(input_string):
    # Regex patterns
    yes_pattern = r"^\s*yes\s*$"     # Matches 'YES' in various cases, ignoring leading/trailing spaces
    no_pattern = r"^\s*no\s*$"       # Matches 'NO' in various cases, ignoring leading/trailing spaces
    partial_pattern = r"^\s*partial\s*$" # Matches 'PARTIAL' in various cases, ignoring leading/trailing spaces

    # Check for matches
    if re.match(yes_pattern, input_string, re.IGNORECASE):
        return 'YES'
    elif re.match(no_pattern, input_string, re.IGNORECASE):
        return 'NO'
    elif re.match(partial_pattern, input_string, re.IGNORECASE):
        return 'PARTIAL'
    else:
        return 'UNKNOWN'
