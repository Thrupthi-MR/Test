# verifier.py

from bluetooth_rules import BLUETOOTH_RULES


def verify_bluetooth_connection(pairing_code):

    rules = BLUETOOTH_RULES

    if pairing_code == "":
        return rules["empty_code_message"]

    if not pairing_code.isdigit():
        return rules["invalid_code_message"]

    if len(pairing_code) != rules["exact_length"]:
        return rules["length_error_message"]

    if pairing_code == rules["valid_code"]:
        return rules["connection_success_message"]

    return rules["incorrect_code_message"]
