# HIT137 Assignment 2 - Group DAN05

This repository contains the files for HIT137 Group Assignment 2.

The assignment has two programming questions:

1. Question 1: file encryption, decryption, and verification
2. Question 2: mathematical expression evaluator using tokenization and recursive descent parsing

## Group Members

| Member | Student ID | Main Contribution |
|---|---|---|
| Muid Khan Joy | S373799 | Question 2: tokenizer and recursive descent parser |
| Abishek Rajeshkumar | S367359 | Question 2: evaluation, error handling, result formatting, and output generation |
| Saurav Suniara | S408811 | Question 1: decryption, verification, file handling, and program flow |
| Trong Hieu Pham | S406541 | Question 1: encryption and character shifting logic |

The GitHub commit history records the contributions made by each group member.

## Folder Structure

```text
.
├── Question 1
│   ├── README_Q1.md
│   ├── cipher.py
│   └── raw_text.txt
├── Question 2
│   ├── evaluator.py
│   ├── sample_input.txt
│   └── sample_output.txt
├── README.md
└── githublink.txt
```

Generated files are created when the programs are run.

Question 1 generates:

```text
Question 1/encrypted_text.txt
Question 1/decrypted_text.txt
```

Question 2 generates:

```text
Question 2/program_output.txt
```

## Requirements

- Python 3
- No external Python packages are required

## Running the Programs from the Repository Root

Because each program uses files stored inside its own folder, run the program from that folder while starting the command from the repository root.

### Question 1

macOS / Linux:

```bash
(cd "Question 1" && python3 cipher.py)
```

If `python` is the Python 3 command on your system:

```bash
(cd "Question 1" && python cipher.py)
```

Windows PowerShell:

```powershell
cd "Question 1"; python cipher.py; cd ..
```

The program asks for two non-negative whole numbers:

```text
Enter shift1:
Enter shift2:
```

It reads `raw_text.txt`, creates `encrypted_text.txt` and `decrypted_text.txt`, and verifies that the decrypted file matches the original file.

More information about Question 1 is available in:

```text
Question 1/README_Q1.md
```

### Question 2

macOS / Linux:

```bash
(cd "Question 2" && python3 evaluator.py)
```

If `python` is the Python 3 command on your system:

```bash
(cd "Question 2" && python evaluator.py)
```

Windows PowerShell:

```powershell
cd "Question 2"; python evaluator.py; cd ..
```

The program asks for an input text file:

```text
Enter input file name [sample_input.txt]:
```

Press Enter to use the default file:

```text
sample_input.txt
```

To use another input file, enter its filename with the `.txt` extension. The file should be placed inside the `Question 2` folder before running the program.

The result is written to:

```text
Question 2/program_output.txt
```

The provided `sample_output.txt` can be used to compare the expected output format.

## Question 1 Summary

`cipher.py` performs the following steps:

1. Reads `raw_text.txt`.
2. Encrypts the text using the two shift values entered by the user.
3. Writes the encrypted text to `encrypted_text.txt`.
4. Decrypts the encrypted text.
5. Writes the decrypted text to `decrypted_text.txt`.
6. Compares the decrypted file with the original file.

## Question 2 Summary

`evaluator.py` reads one mathematical expression per line and supports:

- `+` and `-`
- `*`, `/`, and `%`
- exponentiation using `^`
- parentheses
- unary negation
- implicit multiplication
- operator precedence
- error handling

For each expression, the output contains:

```text
Input:
Tree:
Tokens:
Result:
```

Example:

```text
Input: 3 + 5
Tree: (+ 3 5)
Tokens: [NUM:3] [OP:+] [NUM:5] [END]
Result: 8
```

## Submission Files

The repository includes:

- source code for both questions
- supplied input files
- sample input and expected output for Question 2
- `githublink.txt` containing the public GitHub repository link
- README files with basic instructions

The generated output files can be recreated by running the programs.
