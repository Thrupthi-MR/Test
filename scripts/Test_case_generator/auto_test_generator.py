# auto_test_generator.py

from bluetooth_rules import BLUETOOTH_RULES


def generate_test_cases():

    rules = BLUETOOTH_RULES

    tc_id = 1

    test_cases = []

    def add_case(scenario, test_input, expected):

        nonlocal tc_id

        test_cases.append({
            "TC_ID": f"TC{tc_id:03}",
            "Scenario": scenario,
            "Input": test_input,
            "Expected": expected
        })

        tc_id += 1

    # Positive Test Case

    add_case(
        "Verify Bluetooth connection with correct pairing code",
        rules["valid_code"],
        rules["connection_success_message"]
    )

    # Empty Input

    if rules["mandatory"]:
        add_case(
            "Verify Bluetooth connection with empty pairing code",
            "",
            rules["empty_code_message"]
        )

    # Digits Only Rules

    if rules["digits_only"]:

        add_case(
            "Verify Bluetooth connection with alphabetic characters",
            "abcd",
            rules["invalid_code_message"]
        )

        add_case(
            "Verify Bluetooth connection with special characters",
            "@#$%",
            rules["invalid_code_message"]
        )

        add_case(
            "Verify Bluetooth connection with mixed characters",
            "12a4",
            rules["invalid_code_message"]
        )

    # Length Rules

    if rules["exact_length"]:

        add_case(
            "Verify Bluetooth connection with less than required digits",
            "123",
            rules["length_error_message"]
        )

        add_case(
            "Verify Bluetooth connection with more than required digits",
            "12345",
            rules["length_error_message"]
        )

    # Wrong Numeric Code

    add_case(
        "Verify Bluetooth connection with incorrect pairing code",
        "9999",
        rules["incorrect_code_message"]
    )

    return test_cases


if __name__ == "__main__":

    test_cases = generate_test_cases()

    for tc in test_cases:
        print(tc)
