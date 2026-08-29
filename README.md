# HIT137 Assignment 2 | DAN05

<div align="center">

# HIT137-A2-DAN05

### Group Assignment 2

**HIT137 | Software Now**

![Python](https://img.shields.io/badge/Python-Programming-blue?logo=python\&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Collaboration-black?logo=github)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)
![Assignment](https://img.shields.io/badge/Assessment-Group%20Assignment%202-purple)

</div>

---

## About This Repository

This repository contains the work completed by **Group DAN05** for **HIT137 Group Assignment 2**.

The assessment consists of two Python programming tasks:

1. A file encryption, decryption, and verification program.
2. A mathematical expression evaluator using recursive descent parsing.

The assignment also requires the group to work collaboratively through a **public GitHub repository**, with individual contributions recorded through GitHub.

---

## Group Members

<table>
<tr>
<td align="center" width="25%">

### 👤

**Muid Khan Joy**

Student ID
`S373799`

</td>

<td align="center" width="25%">

### 👤

**Abishek Rajeshkumar**

Student ID
`S367359`

</td>

<td align="center" width="25%">

### 👤

**Saurav Suniara**

Student ID
`S408811`

</td>

<td align="center" width="25%">

### 👤

**Trong Hieu Pham**

Student ID
`S406541`

</td>
</tr>
</table>

---

# Assignment Overview

## Question 1: Cipher Program

The first task requires the development of:

```text
cipher.py
```

The program reads text from:

```text
raw_text.txt
```

and encrypts it using two non-negative integer values:

```text
shift1
shift2
```

Different transformation rules are applied depending on whether a character is:

* A lowercase letter
* An uppercase letter
* A digit
* Another character such as punctuation, spaces, tabs, or newlines

The encrypted content is written to:

```text
encrypted_text.txt
```

The program then decrypts the encrypted content and writes it to:

```text
decrypted_text.txt
```

Finally, the original and decrypted files are compared to confirm that the decryption was successful.

### Required Functions

```python
encrypt_file(
    shift1: int,
    shift2: int,
    input_path: str,
    output_path: str
) -> None
```

```python
decrypt_file(
    shift1: int,
    shift2: int,
    input_path: str,
    output_path: str
) -> None
```

```python
verify_files(
    original_path: str,
    decrypted_path: str
) -> bool
```

### Encryption Rules

| Character Type   | Range | Operation                           |
| ---------------- | ----- | ----------------------------------- |
| Lowercase        | `a-n` | Shift forward by `shift1 * shift2`  |
| Lowercase        | `o-z` | Shift backward by `shift1 + shift2` |
| Uppercase        | `A-M` | Shift backward by `shift1`          |
| Uppercase        | `N-Z` | Shift forward by `shift2²`          |
| Digits           | `0-9` | Shift forward by `shift1 - shift2`  |
| Other characters | Any   | Remain unchanged                    |

### Expected Program Flow

```text
User enters shift1 and shift2
            │
            ▼
      Read raw_text.txt
            │
            ▼
        Encrypt text
            │
            ▼
   encrypted_text.txt
            │
            ▼
        Decrypt text
            │
            ▼
   decrypted_text.txt
            │
            ▼
Compare with raw_text.txt
            │
            ▼
   Verification result
```

---

# Question 2: Mathematical Expression Evaluator

The second task requires the development of:

```text
evaluator.py
```

The program reads mathematical expressions from an input file, with one expression on each line.

The expressions must be processed using a **recursive descent parser implemented with plain functions**.

Classes are not required for this task.

## Supported Features

The evaluator must support:

### Binary Operators

```text
+
-
*
/
%
```

### Exponentiation

```text
^
```

### Parentheses

```text
(...)
```

Nested parentheses must also be supported.

### Unary Negation

Examples:

```text
-5
--5
-(3 + 4)
3 * -2
```

Unary `+` is not supported and should result in an error.

### Implicit Multiplication

Implicit multiplication must also be handled where valid according to the assignment grammar.

Two adjacent numbers such as:

```text
2 3
```

are not considered valid implicit multiplication.

---

## Operator Precedence

Operators must follow the precedence specified in the assessment.

| Priority   | Operators                           | Associativity |
| ---------- | ----------------------------------- | ------------- |
| 1, Lowest  | `+ -`                               | Left          |
| 2          | `* / %` and implicit multiplication | Left          |
| 3          | Unary `-`                           | Prefix        |
| 4, Highest | `^`                                 | Right         |

Example:

```text
3 + 5 * 2
```

is interpreted as:

```text
3 + (5 * 2)
```

---

# Expression Output

Each expression must produce four output fields:

```text
Input:
Tree:
Tokens:
Result:
```

For example:

```text
Input: 3 + 5
Tree: (+ 3 5)
Tokens: [NUM:3] [OP:+] [NUM:5] [END]
Result: 8
```

Each expression block is separated by a blank line.

---

## Parse Tree

Binary operations follow this structure:

```text
(operator left right)
```

Example:

```text
3 + 5
```

produces:

```text
(+ 3 5)
```

A more complex expression:

```text
3 + 5 * 2
```

produces a structure similar to:

```text
(+ 3 (* 5 2))
```

Unary negation is represented using:

```text
(neg operand)
```

Example:

```text
-5
```

becomes:

```text
(neg 5)
```

---

# Token Format

Tokens use the following format:

```text
[TYPE:value]
```

Supported token types are:

| Token    | Meaning               |
| -------- | --------------------- |
| `NUM`    | Numeric literal       |
| `OP`     | Mathematical operator |
| `LPAREN` | `(`                   |
| `RPAREN` | `)`                   |
| `END`    | End of expression     |

Example:

```text
3 + 5
```

Tokens:

```text
[NUM:3] [OP:+] [NUM:5] [END]
```

Unary minus remains a separate operator token.

For example:

```text
-5
```

should be tokenised as:

```text
[OP:-] [NUM:5] [END]
```

---

# Result Formatting

If the calculated result is a whole number:

```text
8.0
```

it should be displayed as:

```text
8
```

If the value is not a whole number, it should be rounded to a maximum of four decimal places according to the assignment requirements.

Invalid expressions should produce:

```text
ERROR
```

where required.

---

# Required Interface

The evaluator must provide:

```python
def evaluate_file(input_path: str) -> list[dict]:
```

The function must:

1. Read expressions from the specified input file.
2. Process each expression.
3. Generate `output.txt`.
4. Save `output.txt` in the same directory as the input file.
5. Return a list of dictionaries containing the results.

Example structure:

```python
[
    {
        "input": "3 + 5",
        "tree": "(+ 3 5)",
        "tokens": "[NUM:3] [OP:+] [NUM:5]",
        "result": 8.0
    },
    {
        "input": "3 @ 5",
        "tree": "ERROR",
        "tokens": "ERROR",
        "result": "ERROR"
    }
]
```

---

# Suggested Project Structure

```text
HIT137-A2-DAN05/
│
├── README.md
├── github_link.txt
│
├── cipher.py
├── raw_text.txt
├── encrypted_text.txt
├── decrypted_text.txt
│
├── evaluator.py
├── input.txt
├── output.txt
│
├── sample_input.txt
└── sample_output.txt
```

The exact repository structure may be adjusted as the group develops the assignment.

---

# Team Workflow

All members should work through this repository so that individual contributions are clearly recorded.

Recommended workflow:

```text
Create / choose task
        │
        ▼
Create working branch
        │
        ▼
Implement solution
        │
        ▼
Test locally
        │
        ▼
Commit changes
        │
        ▼
Push to GitHub
        │
        ▼
Create / review Pull Request
        │
        ▼
Merge approved work
```

### Recommended Commit Style

Examples:

```bash
git commit -m "feat: implement cipher encryption"
```

```bash
git commit -m "feat: add cipher decryption"
```

```bash
git commit -m "feat: implement expression tokenizer"
```

```bash
git commit -m "feat: add recursive descent parser"
```

```bash
git commit -m "test: add cipher verification tests"
```

```bash
git commit -m "fix: handle invalid mathematical expressions"
```

---

# Task Allocation

| Member              | Assigned Area   | Status |
| ------------------- | --------------- | ------ |
| Muid Khan Joy       | To be confirmed | ⏳      |
| Abishek Rajeshkumar | To be confirmed | ⏳      |
| Saurav Suniara      | To be confirmed | ⏳      |
| Trong Hieu Pham     | To be confirmed | ⏳      |

This table can be updated once all members select their assigned task.

---

# Running the Programs

## Cipher

```bash
python cipher.py
```

The program should ask for:

```text
shift1
shift2
```

and then perform encryption, decryption, and verification.

## Evaluator

The required entry point is:

```python
evaluate_file(input_path)
```

Example usage:

```python
from evaluator import evaluate_file

results = evaluate_file("input.txt")
print(results)
```

---

# Collaboration Requirements

The assignment requires:

* A public GitHub repository
* All group members added to the repository
* Contributions recorded through GitHub
* A `github_link.txt` file containing the repository URL
* Programming files and generated outputs included in the final submission

---

# Final Submission Checklist

Before submission, the group should verify:

* [ ] `cipher.py` completed
* [ ] Encryption rules implemented correctly
* [ ] `encrypted_text.txt` generated
* [ ] `decrypted_text.txt` generated
* [ ] File verification working
* [ ] `evaluator.py` completed
* [ ] Tokenizer implemented
* [ ] Recursive descent parser implemented
* [ ] Operator precedence handled correctly
* [ ] Unary negation handled correctly
* [ ] Exponentiation handled correctly
* [ ] Parentheses handled correctly
* [ ] Implicit multiplication handled correctly
* [ ] Invalid expressions handled
* [ ] Parse trees formatted correctly
* [ ] Tokens formatted correctly
* [ ] Results formatted correctly
* [ ] `output.txt` generated correctly
* [ ] Sample input and output checked
* [ ] All members have GitHub contributions
* [ ] Repository is public
* [ ] `github_link.txt` included
* [ ] Final files reviewed before submission

---

<div align="center">

### HIT137 | Assignment 2

**Group DAN05**

Muid Khan Joy • Abishek Rajeshkumar • Saurav Suniara • Trong Hieu Pham

</div>
