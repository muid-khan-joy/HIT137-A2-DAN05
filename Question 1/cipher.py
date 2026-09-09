
# HIT137 Assignment 2 - Question 1
# Encrypt a text file, decrypt it again, then check the two files match.
# Member 1 --> THP
# Member 2 --> SS
 
 
# ===== Section 1: the character groups (Member 1) =====
 
lower_first = "abcdefghijklmn"     # a to n
lower_second = "opqrstuvwxyz"      # o to z
upper_first = "ABCDEFGHIJKLM"      # A to M
upper_second = "NOPQRSTUVWXYZ"     # N to Z
digits = "0123456789"              # 0 to 9
 # other characters remain unchanged
 
# ===== Section 2: change one character (Member 1) =====
 
def shift_in_group(character, group, offset):
    # Find where the character sits in its group.
    position = group.index(character)
    # Move it, and wrap around to the start if it goes past the end.
    new_position = (position + offset) % len(group)
    return group[new_position]
 
 
def encrypt_character(character, shift1, shift2):
    if character in lower_first:
        # a to n: move forward by shift1 * shift2
        return shift_in_group(character, lower_first, shift1 * shift2)
 
    if character in lower_second:
        # o to z: move backward by shift1 + shift2
        return shift_in_group(character, lower_second, -(shift1 + shift2))
 
    if character in upper_first:
        # A to M: move backward by shift1
        return shift_in_group(character, upper_first, -shift1)
 
    if character in upper_second:
        # N to Z: move forward by shift2 * shift2
        return shift_in_group(character, upper_second, shift2 * shift2)
 
    if character in digits:
        # 0 to 9: move forward by shift1 - shift2
        return shift_in_group(character, digits, shift1 - shift2)
 
    # Anything else (spaces, commas, new lines) stays the same.
    return character
 
 
def decrypt_character(character, shift1, shift2):
    # Decrypting is the same thing, but moving the opposite way.
    if character in lower_first:
        return shift_in_group(character, lower_first, -(shift1 * shift2))
 
    if character in lower_second:
        return shift_in_group(character, lower_second, shift1 + shift2)
 
    if character in upper_first:
        return shift_in_group(character, upper_first, shift1)
 
    if character in upper_second:
        return shift_in_group(character, upper_second, -(shift2 * shift2))
 
    if character in digits:
        return shift_in_group(character, digits, -(shift1 - shift2))
 
    return character
 
 
def encrypt_text(text, shift1, shift2):
    # Go through the text one character at a time and build the answer.
    result = ""
    for character in text:
        result = result + encrypt_character(character, shift1, shift2)
    return result
 
 
def decrypt_text(text, shift1, shift2):
    result = ""
    for character in text:
        result = result + decrypt_character(character, shift1, shift2)
    return result
 
 
# ===== Section 3: reading and writing files (Member 2) =====
 
def read_text_file(path):
    
    my_file = open(path, "r", encoding="utf-8", newline="")
    text = my_file.read()
    my_file.close()
    return text
 
 
def write_text_file(path, text):
    my_file = open(path, "w", encoding="utf-8", newline="")
    my_file.write(text)
    my_file.close()
 
 
# ===== Section 4: the three functions the assignment asks for (Member 2) =====
 
def encrypt_file(shift1: int, shift2: int,
                 input_path: str, output_path: str) -> None:
    original = read_text_file(input_path)
    encrypted = encrypt_text(original, shift1, shift2)
    write_text_file(output_path, encrypted)
    print("Encrypted", input_path, "->", output_path)
 
 
def decrypt_file(shift1: int, shift2: int,
                 input_path: str, output_path: str) -> None:
    encrypted = read_text_file(input_path)
    decrypted = decrypt_text(encrypted, shift1, shift2)
    write_text_file(output_path, decrypted)
    print("Decrypted", input_path, "->", output_path)
 
 
def verify_files(original_path: str, decrypted_path: str) -> bool:
    original = read_text_file(original_path)
    decrypted = read_text_file(decrypted_path)
 
    if original == decrypted:
        print("Verification: SUCCESS - the two files are the same.")
        return True
    else:
        print("Verification: FAILED - the two files are different.")
        return False
 
 
# ===== Section 5: asking the user and running everything (Member 2) =====
 
def user_input(question):
    # Keep asking until the user types a number that is 0 or bigger.
    while True:
        answer = input(question)
        if answer.strip().isdigit():
            return int(answer)
        print("  Please type a whole number that is 0 or bigger.")
 
 
def main():
    print("====HIT137 Assignment 2 - Question 1====")
    print()
 
    # Step 1: request user input for the two shift values
    shift1 = user_input("Enter shift1: ")
    shift2 = user_input("Enter shift2: ")
    print()
 
    # Step 2: encrypt
    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
 
    # Step 3: decrypt
    decrypt_file(shift1, shift2, "encrypted_text.txt", "decrypted_text.txt")
 
    # Step 4: check the decrypted file matches the original
    verify_files("raw_text.txt", "decrypted_text.txt")
 
 
main()
