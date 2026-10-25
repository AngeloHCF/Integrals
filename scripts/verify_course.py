"""Exact checks of the new source answers, definite integrals, and geometry setups.

Needs SymPy and antlr4-python3-runtime==4.11.1, as does verify_math.py.
The worksheet itself has no installation requirements.
"""
import os
import re
import sys
if os.environ.get('MATH_VERIFY_DEPS'):
    sys.path.insert(0, os.environ['MATH_VERIFY_DEPS'])
import sympy as s
from sympy.parsing.latex import parse_latex
from course_content import PROBLEMS, TOPICS
from verify_math import derivative, normalize, X

Y = s.Symbol('y', real=True)

def brace_fractions(latex):
    # KaTeX accepts TeX's one-token arguments; SymPy needs explicit braces.
    def argument(text, start):
        while text[start].isspace():
            start += 1
        if text[start] == '{':
            depth, end = 1, start + 1
            while depth:
                depth += (text[end] == '{') - (text[end] == '}')
                end += 1
            return text[start:end], end
        match = re.match(r'\\[A-Za-z]+|.', text[start:])
        return '{' + match[0] + '}', start + len(match[0])
    for match in reversed(list(re.finditer(r'\\frac', latex))):
        top, end = argument(latex, match.end())
        bottom, end = argument(latex, end)
        latex = latex[:match.start()] + r'\frac' + top + bottom + latex[end:]
    return latex

def parse(latex):
    latex = brace_fractions(latex)
    latex = latex.replace(r'\,', ' ').replace(r'\!', '').replace(r'\left', '').replace(r'\right', '')
    latex = latex.replace(r'\lvert', '|').replace(r'\rvert', '|')
    latex = re.sub(r'\\sqrt\s*([A-Za-z0-9])', lambda m: r'\sqrt{' + m[1] + '}', latex)
    latex = re.sub(r'(\\(?:sin|cos|tan|sec|csc|cot)(?:\^\{?\d+\}?)?)\s*x(?![A-Za-z])', r'\1(x)', latex)
    latex = re.sub(r'([xy])(?=\()', lambda m: m[1] + r'\cdot ', latex)
    latex = re.sub(r'\\pi(?=\s*\()', lambda _: r'\pi\cdot ', latex)
    result = parse_latex(latex, strict=True)
    return result.subs({s.Symbol('x'):X, s.Symbol('y'):Y, s.Symbol('e'):s.E, s.Symbol('pi'):s.pi})

def integrate_piece(piece, variable):
    f, a, b = (parse(piece[key]) for key in ('integrand','lower','upper'))
    return s.integrate(f, (variable, a, b))

def verify():
    assert len(PROBLEMS) == 100
    assert len({p['id'] for p in PROBLEMS}) == 100
    assert [sum(p['difficulty'] == d for p in PROBLEMS) for d in ['Medium','Hard','Tricky']] == [70,20,10]
    for title, _ in TOPICS:
        assert sum(p['topic'] == title for p in PROBLEMS) == 10
    definite_count = derivative_count = positive_samples = 0
    for p in PROBLEMS:
        c = p['check']
        assert len(p['steps']) >= 3 and all(step['text'] for step in p['steps'])
        try:
            if c['kind'] == 'antiderivative':
                F = parse(p['answer'].removesuffix(' + C'))
                f = parse(c['integrand'])
                assert normalize(derivative(F)-f) == 0, 'Derivative does not match integrand'
                derivative_count += 1
            elif c['kind'] == 'divergence':
                for piece in c['pieces']:
                    f,a,b = (parse(piece[key]) for key in ('integrand','lower','upper'))
                    primitive = s.integrate(f, X)
                    # Use real logarithms on negative intervals, then take each
                    # one-sided endpoint independently (never a principal value).
                    primitive = primitive.replace(lambda t:t.func == s.log, lambda t:s.log(s.Abs(t.args[0])))
                    actual = s.limit(primitive,X,b,dir='-') - s.limit(primitive,X,a,dir='+')
                    assert actual == s.sympify(piece['expected']), (actual, piece['expected'])
                    definite_count += 1
            else:
                variable = Y if c.get('variable') == 'y' else X
                actual = sum(integrate_piece(piece, variable) for piece in c['pieces'])
                expected = s.sympify(c['expected']) if 'expected' in c else parse(p['answer'])
                if expected in (s.oo, -s.oo):
                    assert actual == expected, (actual, expected)
                else:
                    assert normalize(actual-expected) == 0, (actual, expected, s.simplify(actual-expected))
                definite_count += len(c['pieces'])
                if p['topic'] in [title for title,_ in TOPICS[7:]]:
                    # Verify that every declared area / cross section is nonnegative.
                    for piece in c['pieces']:
                        f,a,b = (parse(piece[k]) for k in ('integrand','lower','upper'))
                        for fraction in [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]:
                            value = f.subs(variable,a+(b-a)*fraction).evalf()
                            assert value.is_real and value >= 0, (piece,value)
                            positive_samples += 1
        except Exception as error:
            raise AssertionError(f"{p['id']} ({p['topic']}): {error}") from error
        if int(p['id'][3:]) % 10 == 0:
            print(f"Checked {p['id']}: {p['topic']}", flush=True)
    print(f'PASS: 100 problems across 10 topics; {derivative_count} exact derivatives; {definite_count} exact definite/improper integral pieces; {positive_samples} nonnegative geometry samples.')

if __name__ == '__main__':
    verify()
