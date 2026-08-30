"""
HIT137 Assignment 2 - Question 1
Member 1's working file: ENCRYPTION LOGIC (Sections 1 + 2)

MERGE NOTE
----------
When merging into cipher.py:
  * KEEP everything from "SECTION 1" down to the end of transform_text()
  * DELETE the test harness at the bottom of this file
    (it is clearly marked between the two "DELETE" banners)
"""

# =====================================================================
# SECTION 1 - CHARACTER GROUPS                          [KEEP ON MERGE]
# (Requirement: "first half (a-n)", "second half (o-z)", "A-M", "N-Z", digits)
# =====================================================================

LOWER_FIRST_HALF = "abcdefghijklmn"      # a - n  (14 letters)
LOWER_SECOND_HALF = "opqrstuvwxyz"       # o - z  (12 letters)
UPPER_FIRST_HALF = "ABCDEFGHIJKLM"       # A - M  (13 letters)
UPPER_SECOND_HALF = "NOPQRSTUVWXYZ"      # N - Z  (13 letters)
DIGITS = "0123456789"                    # 0 - 9  (10 digits)


# =====================================================================
# SECTION 2 - CHARACTER TRANSFORMATION                  [KEEP ON MERGE]
# (Requirement: the four letter rules, the digit rule, and
#  "other characters remain unchanged")
# =====================================================================

def shift_in_group(character, group, offset):
    position = group.index(character)
    new_position = (position + offset) % len(group)
    return group[new_position]


def transform_character(character, shift1, shift2, decrypting=False):
    """Apply the assignment's transformation rules to a single character.

    decrypting=False -> encryption offsets
    decrypting=True  -> the same offsets negated (the exact inverse)
    """
    direction = -1 if decrypting else 1

    # Rule 1: lowercase, first half (a-n)  -> forward by shift1 * shift2
    if character in LOWER_FIRST_HALF:
        return shift_in_group(character, LOWER_FIRST_HALF,
                              direction * (shift1 * shift2))

    # Rule 2: lowercase, second half (o-z) -> backward by shift1 + shift2
    if character in LOWER_SECOND_HALF:
        return shift_in_group(character, LOWER_SECOND_HALF,
                              direction * -(shift1 + shift2))

    # Rule 3: uppercase, first half (A-M)  -> backward by shift1
    if character in UPPER_FIRST_HALF:
        return shift_in_group(character, UPPER_FIRST_HALF,
                              direction * -shift1)

    # Rule 4: uppercase, second half (N-Z) -> forward by shift2 squared
    if character in UPPER_SECOND_HALF:
        return shift_in_group(character, UPPER_SECOND_HALF,
                              direction * (shift2 ** 2))

    # Rule 5: digits (0-9) -> forward by shift1 - shift2
    if character in DIGITS:
        return shift_in_group(character, DIGITS,
                              direction * (shift1 - shift2))

    # Rule 6: everything else (spaces, tabs, newlines, punctuation, symbols)
    return character


def transform_text(text, shift1, shift2, decrypting=False):
    """Apply transform_character to every character of a string."""
    return "".join(
        transform_character(ch, shift1, shift2, decrypting) for ch in text
    )



#   DELETE EVERYTHING BELOW THIS LINE WHEN MERGING 


if __name__ == "__main__":
    sample = "Lorem Ipsum 1966, Zoo! Nam-Xyz."
    print("Original :", sample)
    for s1, s2 in [(3, 4), (0, 0), (7, 2), (1, 25)]:
        enc = transform_text(sample, s1, s2)
        dec = transform_text(enc, s1, s2, decrypting=True)
        status = "OK" if dec == sample else "FAIL"
        print(f"s1={s1:<2} s2={s2:<2} -> {enc!r:40} roundtrip={status}")


