/* A small, non-evaluating expression parser. User input is never executed as code. */
(function (global) {
  'use strict';
  const functions = new Set(['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'ln', 'log', 'exp', 'arcsin', 'arccos', 'arctan', 'sqrt', 'abs']);
  const symbols = new Set(['pi', 'theta', 'alpha', 'beta', 'gamma', 'delta', 'infty']);

  function plainToLatex(input) {
    if (input.length > 4000) throw new Error('Expression too long');
    input = input.replace(/\|([^|]+)\|/g, 'abs($1)');
    const tokens = [];
    const pattern = /\s+|(?:\d+(?:\.\d*)?|\.\d+)|[A-Za-z]+|[+\-*/^_=<>()[\]{},!']/gy;
    let position = 0;
    while (position < input.length) {
      pattern.lastIndex = position;
      const match = pattern.exec(input);
      if (!match) throw new Error('Use LaTeX for this notation');
      position = pattern.lastIndex;
      const token = match[0];
      if (/^\s+$/.test(token)) continue;
      if (/^[A-Za-z]{2,}$/.test(token) && !functions.has(token) && !symbols.has(token)) {
        // Adjacent short variables (dx, xy) are products; prose remains plain text.
        if (token.length > 2) throw new Error('Text');
        tokens.push(...token);
      } else tokens.push(token);
    }
    let index = 0;
    let depth = 0;
    const peek = () => tokens[index];
    const take = () => tokens[index++];
    const startsAtom = token => token && (/^[A-Za-z0-9.]/.test(token) || '([{'.includes(token));
    function atom() {
      if (++depth > 80) throw new Error('Expression too deeply nested');
      const token = take();
      let output;
      if (!token) throw new Error('Incomplete expression');
      if ('([{'.includes(token)) {
        const close = { '(': ')', '[': ']', '{': '}' }[token];
        const inside = relation();
        if (take() !== close) throw new Error('Unclosed group');
        output = { tex: `\\left(${inside}\\right)`, inner: inside };
      } else if (functions.has(token)) {
        const argument = peek() && '([{'.includes(peek()) ? atom() : unary();
        if (token === 'sqrt') output = { tex: `\\sqrt{${argument.inner ?? argument.tex}}` };
        else if (token === 'abs') output = { tex: `\\left|${argument.inner ?? argument.tex}\\right|` };
        else output = { tex: `\\${token} ${argument.tex}` };
      } else if (symbols.has(token)) output = { tex: `\\${token}` };
      else if (/^(?:[A-Za-z]|\d+(?:\.\d*)?|\.\d+)$/.test(token)) output = { tex: token };
      else throw new Error('Expected expression');
      depth--;
      return output;
    }
    function power() {
      let base = atom();
      while (peek() === '!' || peek() === "'" || peek() === '_' || peek() === '^') {
        const operator = take();
        if (operator === '!' || operator === "'") base = { tex: base.tex + operator };
        else {
          const exponent = unary();
          base = { tex: `${base.tex}${operator}{${exponent.inner ?? exponent.tex}}` };
        }
      }
      return base;
    }
    function unary() {
      if (peek() === '+' || peek() === '-') {
        const sign = take();
        return { tex: sign + unary().tex };
      }
      return power();
    }
    function product() {
      let left = unary();
      while (peek() === '*' || peek() === '/' || startsAtom(peek())) {
        const operator = peek() === '*' || peek() === '/' ? take() : '';
        const right = unary();
        if (operator === '/') left = { tex: `\\frac{${left.inner ?? left.tex}}{${right.inner ?? right.tex}}` };
        else left = { tex: left.tex + (operator ? ' \\cdot ' : ' ') + right.tex };
      }
      return left;
    }
    function sum() {
      let output = product().tex;
      while (peek() === '+' || peek() === '-') output += ` ${take()} ${product().tex}`;
      return output;
    }
    function relation() {
      let output = sum();
      while (['=', '<', '>', ','].includes(peek())) output += ` ${take()} ${sum()}`;
      return output;
    }
    const result = relation();
    if (index !== tokens.length) throw new Error('Unexpected token');
    return result;
  }

  function toLatex(input) {
    return input.includes('\\') ? input : plainToLatex(input);
  }
  function renderFormula(source, target, display = false, normalize = false) {
    try {
      const latex = normalize ? toLatex(source) : source;
      global.katex.render(latex, target, {
        displayMode: display, throwOnError: true, trust: false, strict: 'ignore',
        output: 'htmlAndMathml', maxExpand: 500, maxSize: 12
      });
      target.classList.remove('math-fallback');
      return true;
    } catch (_) {
      target.textContent = source;
      target.classList.add('math-fallback');
      return false;
    }
  }

  function appendInline(text, target) {
    // Only matched dollar delimiters are interpreted; unfinished input stays visible.
    const pattern = /\$\$([\s\S]+?)\$\$|(?<!\\)\$([^\n$]+?)(?<!\\)\$/g;
    let cursor = 0;
    for (const match of text.matchAll(pattern)) {
      target.append(document.createTextNode(text.slice(cursor, match.index)));
      const node = document.createElement(match[1] ? 'div' : 'span');
      if (match[1]) node.className = 'math-block';
      renderFormula(match[1] || match[2], node, Boolean(match[1]), true);
      target.append(node);
      cursor = match.index + match[0].length;
    }
    target.append(document.createTextNode(text.slice(cursor)));
  }

  function renderNotes(text, target) {
    target.replaceChildren();
    if (!text.trim()) {
      const hint = document.createElement('p');
      hint.className = 'preview-placeholder';
      hint.textContent = 'Your math preview appears here.';
      target.append(hint);
      return;
    }
    for (const line of text.split('\n')) {
      const node = document.createElement('div');
      node.className = 'preview-line';
      if (line.includes('$')) appendInline(line, node);
      else {
        // Plain prose remains prose. Explicit math symbols opt a line into math parsing.
        const looksLikeMath = /[\\^/=+*_<>{}]|\d|[()[\]]/.test(line) || /^[a-zA-Z]$/.test(line.trim());
        if (looksLikeMath) {
          try {
            const latex = toLatex(line.trim());
            node.classList.add('math-block');
            renderFormula(latex, node, true);
          } catch (_) { node.textContent = line; }
        } else node.textContent = line;
      }
      target.append(node);
    }
  }
  global.WorksheetMath = { plainToLatex, toLatex, renderFormula, renderNotes, appendInline };
})(typeof window === 'undefined' ? globalThis : window);
