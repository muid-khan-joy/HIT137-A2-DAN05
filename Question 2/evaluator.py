"""
HIT137 Assignment 2
Member 3 contribution: Question 2 tokenizer and recursive descent parser.

This file intentionally contains the tokenizer/parser portion only.
Member 4 can add evaluation, output.txt generation, result formatting,
and evaluate_file(input_path) around these functions.

No parser classes are used.
"""

from typing import Optional


# AST node shapes used by this parser:
#
# Number:
#   ("num", "3")
#
# Unary negation:
#   ("neg", operand)
#
# Binary operation:
#   ("bin", operator, left, right)
#
# Keeping numbers as their original lexemes preserves the exact numeric
# literal for token and tree generation. Member 4 can convert them to float
# during evaluation.


def tokenize(expression: str) -> list[tuple[str, str]]:
    """
    Convert one expression into tokens.

    Supported tokens:
        NUM     integer or decimal literal
        OP      + - * / % ^
        LPAREN  (
        RPAREN  )
        END     end of expression

    Number grammar:
        digits
        digits '.' digits

    Examples:
        "3 + 5"
        -> [("NUM", "3"), ("OP", "+"), ("NUM", "5"), ("END", "")]

        "-(3 + 4)"
        -> [("OP", "-"), ("LPAREN", "("), ("NUM", "3"),
            ("OP", "+"), ("NUM", "4"), ("RPAREN", ")"),
            ("END", "")]

    Raises:
        ValueError if an unsupported character or malformed number is found.
    """
    tokens: list[tuple[str, str]] = []
    i = 0
    length = len(expression)

    while i < length:
        ch = expression[i]

        # Whitespace is ignored during tokenization.
        if ch.isspace():
            i += 1
            continue

        # Number literal:
        # one or more digits, optionally followed by "." and one or more digits.
        if ch.isdigit():
            start = i

            while i < length and expression[i].isdigit():
                i += 1

            if i < length and expression[i] == ".":
                i += 1

                # A decimal point must be followed by at least one digit.
                if i >= length or not expression[i].isdigit():
                    raise ValueError("Malformed number literal")

                while i < length and expression[i].isdigit():
                    i += 1

            tokens.append(("NUM", expression[start:i]))
            continue

        if ch in "+-*/%^":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        raise ValueError(f"Unsupported character: {ch!r}")

    tokens.append(("END", ""))
    return tokens


def format_tokens(tokens: list[tuple[str, str]], include_end: bool = True) -> str:
    """
    Format a token list using the assignment output style.

    Example:
        [NUM:3] [OP:+] [NUM:5] [END]
    """
    parts: list[str] = []

    for token_type, value in tokens:
        if token_type == "END":
            if include_end:
                parts.append("[END]")
            continue

        parts.append(f"[{token_type}:{value}]")

    return " ".join(parts)


def current_token(
    tokens: list[tuple[str, str]], position: int
) -> tuple[str, str]:
    """Safely return the token at position."""
    if position < 0 or position >= len(tokens):
        return ("END", "")
    return tokens[position]


def parse_expression_tokens(
    tokens: list[tuple[str, str]]
) -> tuple:
    """
    Parse a complete token list and return an AST.

    The precedence implemented from lowest to highest is:

        1. + -
        2. * / % and implicit multiplication
        3. unary -
        4. ^

    Associativity:
        + -       left
        * / %     left
        unary -   prefix
        ^         right

    Raises:
        ValueError if the token sequence is syntactically invalid.
    """
    if not tokens or tokens[-1][0] != "END":
        raise ValueError("Token stream must end with END")

    node, position = parse_add_sub(tokens, 0)

    token_type, token_value = current_token(tokens, position)

    if token_type != "END":
        raise ValueError(
            f"Unexpected token after complete expression: "
            f"{token_type}:{token_value}"
        )

    return node


def parse_add_sub(
    tokens: list[tuple[str, str]], position: int
) -> tuple[tuple, int]:
    """
    Parse + and - at the lowest precedence level.

    Grammar:
        add_sub := mul_div_mod (('+' | '-') mul_div_mod)*
    """
    left, position = parse_mul_div_mod(tokens, position)

    while True:
        token_type, token_value = current_token(tokens, position)

        if token_type == "OP" and token_value in ("+", "-"):
            operator = token_value
            right, position = parse_mul_div_mod(tokens, position + 1)
            left = ("bin", operator, left, right)
        else:
            break

    return left, position


def parse_mul_div_mod(
    tokens: list[tuple[str, str]], position: int
) -> tuple[tuple, int]:
    """
    Parse *, /, %, and implicit multiplication.

    Explicit operators are left associative.

    Supported implicit multiplication forms include:
        2(3 + 4)
        (2 + 3)4
        (2 + 3)(4 + 5)

    Two adjacent number tokens are deliberately NOT treated as
    implicit multiplication:
        2 3   -> syntax error
    """
    left, position = parse_unary(tokens, position)

    while True:
        token_type, token_value = current_token(tokens, position)

        if token_type == "OP" and token_value in ("*", "/", "%"):
            operator = token_value
            right, position = parse_unary(tokens, position + 1)
            left = ("bin", operator, left, right)
            continue

        if is_implicit_multiplication(tokens, position):
            right, position = parse_unary(tokens, position)
            left = ("bin", "*", left, right)
            continue

        break

    return left, position


def is_implicit_multiplication(
    tokens: list[tuple[str, str]], position: int
) -> bool:
    """
    Return True when the boundary at `position` represents implicit
    multiplication.

    Accepted boundaries:
        NUM    followed by LPAREN
        RPAREN followed by NUM
        RPAREN followed by LPAREN

    This intentionally rejects:
        NUM followed by NUM

    That follows the assignment statement that adjacent numbers such as
    "2 3" are not implicit multiplication.
    """
    if position <= 0:
        return False

    previous_type, _ = current_token(tokens, position - 1)
    next_type, _ = current_token(tokens, position)

    if previous_type == "NUM" and next_type == "LPAREN":
        return True

    if previous_type == "RPAREN" and next_type in ("NUM", "LPAREN"):
        return True

    return False


def parse_unary(
    tokens: list[tuple[str, str]], position: int
) -> tuple[tuple, int]:
    """
    Parse unary negation.

    Grammar:
        unary := '-' unary | power

    Repeated unary negation is therefore valid:
        --5
        ---5

    Unary + is not supported and produces a syntax error.
    """
    token_type, token_value = current_token(tokens, position)

    if token_type == "OP" and token_value == "-":
        operand, position = parse_unary(tokens, position + 1)
        return ("neg", operand), position

    if token_type == "OP" and token_value == "+":
        raise ValueError("Unary + is not supported")

    return parse_power(tokens, position)


def parse_power(
    tokens: list[tuple[str, str]], position: int
) -> tuple[tuple, int]:
    """
    Parse exponentiation.

    Grammar:
        power := primary ('^' unary)?

    Parsing the right operand through `parse_unary` makes exponentiation
    right associative while also allowing unary negation after ^.

    Examples:
        2 ^ 3 ^ 2
        -> (^ 2 (^ 3 2))

        -2 ^ 2
        -> (neg (^ 2 2))

        2 ^ -3
        -> (^ 2 (neg 3))
    """
    left, position = parse_primary(tokens, position)

    token_type, token_value = current_token(tokens, position)

    if token_type == "OP" and token_value == "^":
        right, position = parse_unary(tokens, position + 1)
        left = ("bin", "^", left, right)

    return left, position


def parse_primary(
    tokens: list[tuple[str, str]], position: int
) -> tuple[tuple, int]:
    """
    Parse a number or parenthesised sub-expression.

    Grammar:
        primary := NUM | '(' add_sub ')'
    """
    token_type, token_value = current_token(tokens, position)

    if token_type == "NUM":
        return ("num", token_value), position + 1

    if token_type == "LPAREN":
        node, position = parse_add_sub(tokens, position + 1)

        close_type, _ = current_token(tokens, position)
        if close_type != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        return node, position + 1

    if token_type == "RPAREN":
        raise ValueError("Unexpected closing parenthesis")

    if token_type == "END":
        raise ValueError("Unexpected end of expression")

    raise ValueError(
        f"Expected a number, unary '-', or '(', got "
        f"{token_type}:{token_value}"
    )


def tree_to_string(node: tuple) -> str:
    """
    Convert the AST into the assignment's prefix tree format.

    Examples:
        ("num", "5")
        -> 5

        ("neg", ("num", "5"))
        -> (neg 5)

        ("bin", "+", ("num", "3"), ("num", "5"))
        -> (+ 3 5)
    """
    kind = node[0]

    if kind == "num":
        return node[1]

    if kind == "neg":
        return f"(neg {tree_to_string(node[1])})"

    if kind == "bin":
        operator = node[1]
        left = tree_to_string(node[2])
        right = tree_to_string(node[3])
        return f"({operator} {left} {right})"

    raise ValueError(f"Unknown AST node type: {kind!r}")


def parse_expression(expression: str) -> dict:
    """
    Convenience function for Member 4.

    It performs tokenization and parsing and returns:
        {
            "tokens_raw": [...],
            "tokens": "[NUM:3] [OP:+] [NUM:5] [END]",
            "ast": (...),
            "tree": "(+ 3 5)"
        }

    Errors are intentionally raised as ValueError so Member 4 can decide
    how to convert them into the required ERROR output.
    """
    tokens = tokenize(expression)
    ast = parse_expression_tokens(tokens)

    return {
        "tokens_raw": tokens,
        "tokens": format_tokens(tokens),
        "ast": ast,
        "tree": tree_to_string(ast),
    }


def try_parse_expression(expression: str) -> dict:
    """
    Optional integration helper.

    Unlike parse_expression(), this function converts tokenizer/parser
    failures into a simple ERROR structure. It does not evaluate results.
    """
    try:
        parsed = parse_expression(expression)
        return {
            "input": expression,
            "tree": parsed["tree"],
            "tokens": parsed["tokens"],
            "ast": parsed["ast"],
            "error": None,
        }
    except ValueError as exc:
        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": "ERROR",
            "ast": None,
            "error": str(exc),
        }


def _self_test() -> None:
    """
    Lightweight parser tests for Member 3.

    These do not evaluate arithmetic results. They verify tokenization,
    precedence, associativity, unary negation, implicit multiplication,
    and syntax errors.
    """
    valid_cases = {
        "3 + 5": "(+ 3 5)",
        "2 + 3 * 4": "(+ 2 (* 3 4))",
        "-(3 + 4)": "(neg (+ 3 4))",
        "--5": "(neg (neg 5))",
        "(10 - 2) * 3 + -4 / 2":
            "(+ (* (- 10 2) 3) (/ (neg 4) 2))",

        # Additional precedence and associativity checks
        "2 ^ 3 ^ 2": "(^ 2 (^ 3 2))",
        "-2 ^ 2": "(neg (^ 2 2))",
        "2 ^ -3": "(^ 2 (neg 3))",
        "3 * -2": "(* 3 (neg 2))",

        # Implicit multiplication checks
        "2(3 + 4)": "(* 2 (+ 3 4))",
        "(2 + 3)4": "(* (+ 2 3) 4)",
        "(2 + 3)(4 + 5)": "(* (+ 2 3) (+ 4 5))",

        # Parsing should succeed even though Member 4 will later produce
        # Result: ERROR for division by zero during evaluation.
        "1 / 0": "(/ 1 0)",
    }

    for expression, expected_tree in valid_cases.items():
        parsed = parse_expression(expression)
        actual_tree = parsed["tree"]
        assert actual_tree == expected_tree, (
            f"{expression!r}: expected {expected_tree!r}, "
            f"got {actual_tree!r}"
        )

    invalid_cases = [
        "3 @ 5",
        "+5",
        "2 3",
        "(3 + 4",
        "3 + 4)",
        "5.",
        ".5",
        "3 +",
        "",
    ]

    for expression in invalid_cases:
        try:
            parse_expression(expression)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"{expression!r} should have produced a parser/tokenizer error"
            )


if __name__ == "__main__":
    _self_test()
    print("Member 3 tokenizer/parser tests passed.")
