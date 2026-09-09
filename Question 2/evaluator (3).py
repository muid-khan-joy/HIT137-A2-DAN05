"""
evaluator.py - HIT137 Assignment 2, Question 2

Reads expressions from a text file, tokenizes and parses each one,
evaluates the result, and writes output.txt in the required
Input / Tree / Tokens / Result format.

No classes are used anywhere.
"""

import os
import sys


# ---------------------------------------------------------------------------
# Tokenizer + recursive-descent parser
# ---------------------------------------------------------------------------
#
# AST node shapes produced by this parser:
#
#   Number:           ("num", "3")        -- value is the raw lexeme (a
#                                             string); evaluate() converts
#                                             it to float when needed
#   Unary negation:   ("neg", operand)
#   Binary operation: ("bin", operator, left, right)


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

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():
            start = i

            while i < length and expression[i].isdigit():
                i += 1

            if i < length and expression[i] == ".":
                i += 1
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


def current_token(tokens: list[tuple[str, str]], position: int) -> tuple[str, str]:
    """Safely return the token at position."""
    if position < 0 or position >= len(tokens):
        return ("END", "")
    return tokens[position]


def parse_expression_tokens(tokens: list[tuple[str, str]]) -> tuple:
    """
    Parse a complete token list and return an AST.

    Precedence implemented, lowest to highest:
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


def parse_add_sub(tokens: list[tuple[str, str]], position: int) -> tuple[tuple, int]:
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


def parse_mul_div_mod(tokens: list[tuple[str, str]], position: int) -> tuple[tuple, int]:
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


def is_implicit_multiplication(tokens: list[tuple[str, str]], position: int) -> bool:
    """
    Return True when the boundary at `position` represents implicit
    multiplication.

    Accepted boundaries:
        NUM    followed by LPAREN
        RPAREN followed by NUM
        RPAREN followed by LPAREN

    This intentionally rejects NUM followed by NUM, since the assignment
    states that adjacent numbers such as "2 3" are not implicit
    multiplication.
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


def parse_unary(tokens: list[tuple[str, str]], position: int) -> tuple[tuple, int]:
    """
    Parse unary negation.

    Grammar:
        unary := '-' unary | power

    Repeated unary negation is valid: --5, ---5.
    Unary + is not supported and produces a syntax error.
    """
    token_type, token_value = current_token(tokens, position)

    if token_type == "OP" and token_value == "-":
        operand, position = parse_unary(tokens, position + 1)
        return ("neg", operand), position

    if token_type == "OP" and token_value == "+":
        raise ValueError("Unary + is not supported")

    return parse_power(tokens, position)


def parse_power(tokens: list[tuple[str, str]], position: int) -> tuple[tuple, int]:
    """
    Parse exponentiation.

    Grammar:
        power := primary ('^' unary)?

    Parsing the right operand through parse_unary makes exponentiation
    right associative while also allowing unary negation after ^:
        2 ^ 3 ^ 2  -> (^ 2 (^ 3 2))
        -2 ^ 2     -> (neg (^ 2 2))
        2 ^ -3     -> (^ 2 (neg 3))
    """
    left, position = parse_primary(tokens, position)
    token_type, token_value = current_token(tokens, position)

    if token_type == "OP" and token_value == "^":
        right, position = parse_unary(tokens, position + 1)
        left = ("bin", "^", left, right)

    return left, position


def parse_primary(tokens: list[tuple[str, str]], position: int) -> tuple[tuple, int]:
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
        f"Expected a number, unary '-', or '(', got {token_type}:{token_value}"
    )


def tree_to_string(node: tuple) -> str:
    """
    Convert the AST into the assignment's prefix tree format.

        ("num", "5")                              -> 5
        ("neg", ("num", "5"))                     -> (neg 5)
        ("bin", "+", ("num", "3"), ("num", "5"))  -> (+ 3 5)
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


def _self_test() -> None:
    """
    Self-tests for the tokenizer and parser (tokenization, precedence,
    associativity, unary negation, implicit multiplication, and syntax
    errors). Does not test evaluation.
    """
    valid_cases = {
        "3 + 5": "(+ 3 5)",
        "2 + 3 * 4": "(+ 2 (* 3 4))",
        "-(3 + 4)": "(neg (+ 3 4))",
        "--5": "(neg (neg 5))",
        "(10 - 2) * 3 + -4 / 2": "(+ (* (- 10 2) 3) (/ (neg 4) 2))",
        "2 ^ 3 ^ 2": "(^ 2 (^ 3 2))",
        "-2 ^ 2": "(neg (^ 2 2))",
        "2 ^ -3": "(^ 2 (neg 3))",
        "3 * -2": "(* 3 (neg 2))",
        "2(3 + 4)": "(* 2 (+ 3 4))",
        "(2 + 3)4": "(* (+ 2 3) 4)",
        "(2 + 3)(4 + 5)": "(* (+ 2 3) (+ 4 5))",
        "1 / 0": "(/ 1 0)",
    }

    for expression, expected_tree in valid_cases.items():
        ast = parse_expression_tokens(tokenize(expression))
        actual_tree = tree_to_string(ast)
        assert actual_tree == expected_tree, (
            f"{expression!r}: expected {expected_tree!r}, got {actual_tree!r}"
        )

    invalid_cases = ["3 @ 5", "+5", "2 3", "(3 + 4", "3 + 4)", "5.", ".5", "3 +", ""]

    for expression in invalid_cases:
        try:
            parse_expression_tokens(tokenize(expression))
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"{expression!r} should have produced a parser/tokenizer error"
            )


# ---------------------------------------------------------------------------
# Evaluation, formatting, and output.txt generation
# ---------------------------------------------------------------------------

def evaluate(node: tuple) -> float:
    """
    Walk a parsed tree and compute its numeric value (a float).

    Raises ZeroDivisionError for division/modulo by zero, OverflowError
    for results too large to represent, and ValueError for anything else
    that can't produce a valid real result (e.g. a fractional power of a
    negative number, which would otherwise silently become a complex
    number). evaluate_file() below turns any of these into the "ERROR"
    shown in the Result line -- this function's only job is to compute
    the value or raise.
    """
    kind = node[0]

    if kind == "num":
        return float(node[1])

    if kind == "neg":
        return -evaluate(node[1])

    if kind == "bin":
        op, left, right = node[1], node[2], node[3]
        lval = evaluate(left)
        rval = evaluate(right)

        if op == "+":
            return lval + rval
        if op == "-":
            return lval - rval
        if op == "*":
            return lval * rval
        if op == "/":
            if rval == 0:
                raise ZeroDivisionError("division by zero")
            return lval / rval
        if op == "%":
            if rval == 0:
                raise ZeroDivisionError("modulo by zero")
            return lval % rval
        if op == "^":
            result = lval ** rval
            if isinstance(result, complex):
                raise ValueError("result is not a real number")
            return result

    raise ValueError(f"Unknown tree node: {node}")


def format_number(value: float) -> str:
    """
    Apply the assignment's display rule to a result value: whole numbers
    show with no decimal point (8.0 -> "8"), anything else is rounded to
    4 decimal places (trailing zeros from that rounding are trimmed, so
    5.5 -> "5.5" rather than "5.5000").
    """
    cleaned = round(value, 9)  # round away float noise before checking is_integer

    if float(cleaned).is_integer():
        return str(int(round(cleaned)))

    rounded = round(cleaned, 4)
    return f"{rounded:.4f}".rstrip("0").rstrip(".")


def evaluate_file(input_path: str) -> list[dict]:
    """
    Read expressions from input_path (one per line), evaluate each one,
    write output.txt next to the input file, and return the same
    information as a list of dicts.

    Each dict has keys "input", "tree", "tokens", "result":
        - "tree" and "tokens" are always strings (either the formatted
          value, or "ERROR").
        - "result" is a float on success, or the string "ERROR".

    Three independent things can go wrong, and each is handled at the
    stage where it actually happens, which is why (for example) "1 / 0"
    still shows a correct Tree and Tokens line but an ERROR Result:
        1. tokenizing fails               -> tree, tokens, result all ERROR
        2. tokenizing OK, parsing fails    -> tokens OK, tree/result ERROR
        3. parsing OK, evaluation fails    -> tokens/tree OK, result ERROR
    """
    output_path = os.path.join(os.path.dirname(input_path) or ".", "output.txt")

    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    # blank lines in the input file aren't expressions to evaluate -- this
    # mainly avoids a spurious ERROR block for a trailing blank line at EOF
    expressions = [line for line in lines if line.strip() != ""]

    results = []
    blocks = []

    for expr_text in expressions:
        tokens = None
        tree_node = None

        tree_display = "ERROR"
        tokens_display = "ERROR"
        result_display = "ERROR"
        result_value = "ERROR"

        try:
            tokens = tokenize(expr_text)
            tokens_display = format_tokens(tokens)
        except ValueError:
            tokens = None

        if tokens is not None:
            try:
                tree_node = parse_expression_tokens(tokens)
                tree_display = tree_to_string(tree_node)
            except ValueError:
                tree_node = None

        if tree_node is not None:
            try:
                value = evaluate(tree_node)
                result_value = float(value)
                result_display = format_number(result_value)
            except (ZeroDivisionError, OverflowError, ValueError):
                result_value = "ERROR"
                result_display = "ERROR"

        results.append({
            "input": expr_text,
            "tree": tree_display,
            "tokens": tokens_display,
            "result": result_value,
        })

        blocks.append(
            f"Input: {expr_text}\n"
            f"Tree: {tree_display}\n"
            f"Tokens: {tokens_display}\n"
            f"Result: {result_display}"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks))
        if blocks:
            f.write("\n")

    return results


if __name__ == "__main__":
    _self_test()
    in_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    rows = evaluate_file(in_path)
    errors = sum(1 for r in rows if r["result"] == "ERROR")
    print(f"Parser self-tests passed. Evaluated {len(rows)} expression(s), "
          f"{errors} error(s). Wrote output.txt next to {in_path}.")
