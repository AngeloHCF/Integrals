"""Verify the actual LaTeX source with symbolic differentiation.

Developer check only (the worksheet itself needs no Python or installation):
  python -m pip install sympy antlr4-python3-runtime==4.11.1
  python scripts/verify_math.py

An optional MATH_VERIFY_DEPS directory may hold the antlr runtime instead.
"""
from pathlib import Path
import os
import re
import sys

if os.environ.get("MATH_VERIFY_DEPS"):
    sys.path.insert(0, os.environ["MATH_VERIFY_DEPS"])

import sympy as s
from sympy.parsing.latex import parse_latex

ROOT = Path(__file__).resolve().parents[1]
X = s.Symbol("x", real=True)


def braced(text, start):
    assert text[start] == "{"
    depth = 1
    cursor = start + 1
    while depth:
        if text[cursor] == "{":
            depth += 1
        elif text[cursor] == "}":
            depth -= 1
        cursor += 1
    return text[start + 1:cursor - 1], cursor


def source_questions():
    source = (ROOT / "main.tex").read_text(encoding="utf-8")
    questions = []
    for match in re.finditer(r"\\question\{ans\d+\}", source):
        cursor = match.start() + len(r"\question")
        fields = []
        for _ in range(3):
            value, cursor = braced(source, cursor)
            fields.append(value)
        questions.append(fields)
    assert [q[0] for q in questions] == [f"ans{n}" for n in range(1, 101)]
    return questions


def expression(latex, integrand=False):
    if integrand:
        latex = latex.replace(r"\int", "").replace("{dx}", "{1}").replace("dx", "")
    latex = latex.replace(r"\,", " ")
    for command in [r"\!", r"\left", r"\right"]:
        latex = latex.replace(command, "")
    # Make implicit function arguments and multiplication unambiguous to the
    # LaTeX parser: sin x e^... means sin(x)*e^..., and x(...) is a product.
    latex = re.sub(r"(\\(?:sin|cos|tan|sec|csc|cot)(?:\^\{?\d+\}?)?)\s*x(?![A-Za-z])", r"\1(x)", latex)
    latex = re.sub(r"x(?=\()", r"x\\cdot ", latex)
    latex = latex.replace(r"\lvert", "|").replace(r"\rvert", "|")
    result = parse_latex(latex, strict=True)
    result = result.subs({s.Symbol("x"): X, s.Symbol("e"): s.E})
    return result


def derivative(answer):
    # On every open real interval where f != 0, d(log|f|)/dx = f'/f.
    # Removing Abs only inside log implements that local derivative without
    # introducing symbolic sign/Dirac expressions. Domain samples below also
    # check both positive and negative components whenever they exist.
    local_answer = answer.replace(
        lambda term: term.func == s.log and term.has(s.Abs),
        lambda term: s.log(term.args[0].replace(s.Abs, lambda arg: arg)),
    )
    return s.diff(local_answer, X)


def normalize(value):
    value = s.simplify(s.trigsimp(value))
    if value != 0:
        value = s.simplify(s.expand(s.expand_trig(value)))
    return value


def verify():
    failures = []
    samples = [s.Rational(n, 10) for n in [-121, -73, -51, -37, -21, -13, -7, 3, 7, 13, 21, 37, 51, 73, 121]]
    sample_count = 0
    for identity, question, answer in source_questions():
        f = expression(question, integrand=True)
        F = expression(answer)
        dF = derivative(F)
        residual = normalize(dF - f)
        if residual != 0:
            failures.append((identity, str(residual)))
            continue
        checked = 0
        for point in samples:
            f_value = f.subs(X, point).evalf(35)
            F_value = F.subs(X, point).evalf(35)
            if f_value.is_real is not True or F_value.is_real is not True:
                continue
            if f_value.is_finite is not True or F_value.is_finite is not True:
                continue
            error = (dF.subs(X, point) - f_value).evalf(25)
            relative_error = abs(complex(error)) / (1 + abs(complex(f_value)))
            assert relative_error < 1e-20, (identity, point, error)
            checked += 1
        assert checked >= 2, (identity, "insufficient real-domain samples")
        sample_count += checked
    if failures:
        for identity, failure in failures:
            print(f"FAIL {identity}: {failure}")
        raise SystemExit(1)
    print(f"PASS: all 100 source antiderivatives differentiated exactly; {sample_count} real-domain samples checked.")


if __name__ == "__main__":
    verify()
