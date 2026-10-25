/* Developer integration checks. Run with jsdom available on NODE_PATH. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL, fileURLToPath } = require('node:url');
const { JSDOM, VirtualConsole } = require('jsdom');
const root = path.resolve(__dirname, '..');
const page = path.join(root, 'Open worksheet.html');
const katex = require('../worksheet/vendor/katex.min.js');
const values = new Map([
  ['unrelated.saved.data', 'keep me'],
  ['integrals.worksheet.ans7.notes', 'Existing note: $x^2$'],
  ['integrals.worksheet.ans7.completed', 'true'],
  ['integrals.worksheet.future.setting', '{"preserve":true}']
]);
const loaded = new Set();
const errors = [];
let blocked = false;
async function openWorksheet() {
  const console = new VirtualConsole();
  console.on('jsdomError', error => { if (error.type !== 'css-parsing') errors.push(error.message); });
  const dom = new JSDOM(fs.readFileSync(page, 'utf8'), {
    url: pathToFileURL(page).href,
    resources: 'usable', runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: console,
    beforeParse(window) {
      Object.defineProperty(window, 'localStorage', { value: {
        getItem(key) { if (blocked) throw new Error('Storage unavailable'); return values.get(key) ?? null; },
        setItem(key, value) { if (blocked) throw new Error('Storage full'); values.set(key, String(value)); },
        removeItem(key) { values.delete(key); },
        clear() { throw new Error('Storage must never be cleared'); }
      }});
    }
  });
  await new Promise(resolve => dom.window.addEventListener('load', resolve));
  for (const node of dom.window.document.querySelectorAll('script[src], link[rel="stylesheet"]')) {
    const url = node.src || node.href;
    assert.ok(url.startsWith('file:'), `Unexpected network request: ${url}`);
    const filename = fileURLToPath(url);
    assert.ok(fs.existsSync(filename), `Missing asset: ${filename}`);
    loaded.add(path.relative(root, filename).replaceAll('\\', '/'));
    if (node.tagName === 'LINK') assert.ok(node.sheet?.cssRules.length, 'Stylesheet must load and parse');
  }
  return dom;
}
async function verify() {
  let dom = await openWorksheet();
  let w = dom.window, d = w.document;
  const q = selector => d.querySelector(selector);
  assert.equal(q('#worksheet-set').value, 'course', 'New course set is the default');
  assert.equal(q('#notes-ans7').value, '', 'Old notes must not appear on new questions');
  assert.equal(q('#progress').value, 0, 'Old completion must not apply to new questions');
  assert.equal(values.size, 4, 'Initial loading does not rewrite saved data');
  q('#worksheet-set').value = 'original';
  q('#worksheet-set').dispatchEvent(new w.Event('change'));
  assert.equal(d.querySelectorAll('.question').length, 100);
  assert.equal(d.querySelectorAll('textarea').length, 100);
  assert.equal(d.querySelectorAll('.solution[hidden]').length, 100);
  assert.equal(d.querySelectorAll('.problem-math .katex').length, 100);
  assert.ok(q('#complete-ans7').checked);
  assert.equal(q('#notes-ans7').value, 'Existing note: $x^2$');
  assert.equal(q('#completion-count').textContent, '1 of 100 complete');
  assert.equal(values.size, 5, 'Switching sets only adds the selection preference');
  for (const name of ['styles.css', 'app.js', 'problems.js', 'math-preview.js', 'vendor/katex.min.css', 'vendor/katex.min.js']) {
    assert.ok(loaded.has('worksheet/' + name), `Asset did not load: ${name}`);
  }
  const css = fs.readFileSync(path.join(root, 'worksheet/vendor/katex.min.css'), 'utf8');
  const fonts = [...css.matchAll(/url\(([^)]+)\)/g)];
  for (const match of fonts) assert.ok(fs.existsSync(path.join(root, 'worksheet/vendor', match[1].replace(/["']/g, ''))));
  for (const notes of d.querySelectorAll('textarea')) {
    assert.equal(notes.getAttribute('spellcheck'), 'false');
    assert.equal(notes.getAttribute('autocorrect'), 'off');
    assert.equal(notes.getAttribute('autocapitalize'), 'off');
  }
  let formulas = 0;
  for (const problem of w.INTEGRALS) {
    for (const source of [problem.question, problem.answer, ...problem.steps.map(s => s.math).filter(Boolean)]) {
      katex.renderToString(source, { throwOnError: true, trust: false });
      formulas++;
    }
    const button = q(`#${problem.id} .solution-toggle`);
    button.click();
    assert.equal(button.getAttribute('aria-expanded'), 'true');
    assert.ok(!q(`#solution-${problem.id}`).hidden);
    assert.ok(q(`#solution-${problem.id} ol`).children.length >= 3);
    button.click();
    assert.ok(q(`#solution-${problem.id}`).hidden);
  }
  assert.equal(d.querySelectorAll('.math-fallback').length, 0, [...d.querySelectorAll('.math-fallback')].map(node => `${node.closest('article')?.id}: ${node.textContent}`).join('\n'));
  const preview = q('#preview-ans1');
  assert.equal(w.WorksheetMath.plainToLatex('sin(x)^2'), '\\sin \\left(x\\right)^{2}');
  assert.equal(w.WorksheetMath.plainToLatex('x^(n+1)'), 'x^{n + 1}');
  assert.equal(w.WorksheetMath.plainToLatex('(n+1)/(n+2)'), '\\frac{n + 1}{n + 2}');
  for (const [source, tag, expected] of [
    ['a^x', 'msup', 1], ['a/b', 'mfrac', 1], ['(n+1)/(n+2)', 'mfrac', 1],
    ['x^(n+1)', 'msup', 1], ['a/(b/c)', 'mfrac', 2], ['(a/b)^2', 'mfrac', 1],
    ['\\frac{x^2}{2}', 'mfrac', 1], ['Let $u=x^2+3$, then $(n+1)/(n+2)$.', 'mfrac', 1]
  ]) {
    w.WorksheetMath.renderNotes(source, preview);
    assert.equal(preview.querySelectorAll(tag).length, expected, source);
  }
  assert.ok(preview.textContent.startsWith('Let '));
  w.WorksheetMath.renderNotes('<img src=x onerror=alert(1)>', preview);
  assert.equal(preview.querySelectorAll('img,script').length, 0);
  w.WorksheetMath.renderNotes('x^(', preview);
  assert.equal(preview.textContent, 'x^(');
  const note = 'Saved immediately: $x^(n+1)$\n(n+1)/(n+2)\n\\frac{1}{2}';
  q('#notes-ans1').value = note;
  q('#notes-ans1').dispatchEvent(new w.Event('input', { bubbles: true }));
  assert.equal(values.get('integrals.worksheet.ans1.notes'), note, 'Notes save before debounce');
  q('#complete-ans1').click();
  assert.equal(values.get('integrals.worksheet.ans1.completed'), 'true');
  dom.window.close();
  dom = await openWorksheet(); w = dom.window; d = w.document;
  assert.equal(q('#notes-ans1').value, note);
  assert.ok(q('#complete-ans1').checked);
  assert.ok(q('#preview-ans1 mfrac'));
  assert.equal(d.querySelectorAll('.solution[hidden]').length, 100);
  q('#reset').click();
  assert.equal(q('#progress').value, 0);
  assert.equal(q('#notes-ans1').value, note);
  assert.equal(values.get('integrals.worksheet.ans1.notes'), note);
  q('#undo-reset').click();
  assert.equal(q('#progress').value, 2);
  q('#reset').click();
  dom.window.close();
  dom = await openWorksheet(); w = dom.window; d = w.document;
  assert.equal(q('#progress').value, 0);
  assert.equal(q('#notes-ans1').value, note);
  assert.equal(q('#notes-ans7').value, 'Existing note: $x^2$');
  assert.equal(values.get('unrelated.saved.data'), 'keep me');
  assert.equal(values.get('integrals.worksheet.future.setting'), '{"preserve":true}');
  blocked = true;
  q('#notes-ans1').value = 'Temporarily unsaved';
  q('#notes-ans1').dispatchEvent(new w.Event('input'));
  assert.ok(q('#storage-status').textContent.includes('Saving is unavailable'));
  assert.equal(values.get('integrals.worksheet.ans1.notes'), note);
  blocked = false;
  q('#complete-ans2').click();
  assert.equal(values.get('integrals.worksheet.ans1.notes'), 'Temporarily unsaved');
  const originalState = new Map([...values].filter(([key]) => key.startsWith('integrals.worksheet.')));
  q('#worksheet-set').value = 'course';
  q('#worksheet-set').dispatchEvent(new w.Event('change'));
  assert.equal(d.querySelectorAll('.topic-heading').length, 10);
  assert.equal(q('#topic-jump').options.length, 10);
  assert.equal(d.querySelectorAll('.difficulty-medium').length, 70);
  assert.equal(d.querySelectorAll('.difficulty-hard').length, 20);
  assert.equal(d.querySelectorAll('.difficulty-tricky').length, 10);
  assert.equal(q('#progress').value, 0);
  assert.equal(q('#notes-ans1').value, '');
  for (const problem of w.INTEGRALS) {
    assert.ok(problem.prompt && problem.topic && problem.difficulty);
    for (const source of [problem.question, problem.answer, ...problem.steps.map(s => s.math).filter(Boolean)]) {
      katex.renderToString(source, {throwOnError:true, trust:false});
      formulas++;
    }
    q(`#${problem.id} .solution-toggle`).click();
    assert.ok(q(`#solution-${problem.id} ol`).children.length >= 3);
  }
  assert.equal(d.querySelectorAll('.math-fallback').length, 0, [...d.querySelectorAll('.math-fallback')].map(n => `${n.closest('article')?.id}: ${n.textContent}`).join('\n'));
  q('#topic-jump').value = 'topic-ans81';
  q('#topic-jump').dispatchEvent(new w.Event('change'));
  assert.equal(d.activeElement.id, 'topic-ans81');
  q('#notes-ans1').value = 'New course note $a/b$';
  q('#notes-ans1').dispatchEvent(new w.Event('input'));
  q('#complete-ans1').click();
  assert.equal(values.get('integrals.course-v1.ans1.notes'), 'New course note $a/b$');
  assert.equal(values.get('integrals.course-v1.ans1.completed'), 'true');
  dom.window.close();
  dom = await openWorksheet(); w = dom.window; d = w.document;
  assert.equal(q('#worksheet-set').value, 'course');
  assert.equal(q('#notes-ans1').value, 'New course note $a/b$');
  assert.ok(q('#complete-ans1').checked);
  assert.equal(d.querySelectorAll('.solution[hidden]').length, 100);
  q('#reset').click();
  assert.equal(q('#progress').value, 0);
  assert.equal(q('#notes-ans1').value, 'New course note $a/b$');
  q('#undo-reset').click();
  assert.equal(q('#progress').value, 1);
  for (const [key,value] of originalState) assert.equal(values.get(key), value, 'Course actions must preserve all original saved data');
  q('#worksheet-set').value = 'original';
  q('#worksheet-set').dispatchEvent(new w.Event('change'));
  assert.equal(q('#notes-ans1').value, 'Temporarily unsaved');
  assert.equal(q('#notes-ans7').value, 'Existing note: $x^2$');
  assert.ok(q('#complete-ans2').checked);
  q('#worksheet-set').value = 'course';
  q('#worksheet-set').dispatchEvent(new w.Event('change'));
  assert.equal(q('#notes-ans1').value, 'New course note $a/b$');
  dom.window.close();
  assert.deepEqual(errors, []);
  console.log(`PASS: 100 course + 100 original questions and worked solutions, ${formulas} display formulas, ${fonts.length} local font references; previews, topic jumps, set switching, immediate save, reload, reset, undo, original data preservation, and storage recovery.`);
}
verify().catch(error => { console.error(error); process.exitCode = 1; });
