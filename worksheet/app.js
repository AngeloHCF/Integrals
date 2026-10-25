(function () {
  'use strict';
  const sets = window.WORKSHEETS;
  let problems = [];
  const math = window.WorksheetMath;
  const list = document.getElementById('questions');
  const status = document.getElementById('storage-status');
  let prefix = '';
  const cards = new Map();
  const pendingWrites = new Map();
  let previousCompletion = null;

  function storageFailure() {
    status.textContent = 'Saving is unavailable. Keep this tab open and copy your notes before closing it. Your existing saved data has not been cleared.';
    status.classList.add('warning');
  }
  function read(id, field) {
    try { return localStorage.getItem(prefix + id + '.' + field); }
    catch (_) { storageFailure(); return null; }
  }
  function save(id, field, value) {
    const key = prefix + id + '.' + field;
    pendingWrites.set(key, value);
    try {
      // Retry any earlier failed writes; never replace or clear unrelated data.
      for (const [pendingKey, pendingValue] of pendingWrites) {
        localStorage.setItem(pendingKey, pendingValue);
        pendingWrites.delete(pendingKey);
      }
      status.textContent = 'Saved on this device. Reset clears checkmarks only.';
      status.classList.remove('warning');
    } catch (_) { storageFailure(); }
  }
  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function updateProgress() {
    let count = 0;
    for (const { checkbox, card } of cards.values()) {
      if (checkbox.checked) count++;
      card.classList.toggle('is-complete', checkbox.checked);
    }
    document.getElementById('completion-count').textContent = `${count} of ${problems.length} complete`;
    const percent = Math.round(count / problems.length * 100);
    document.getElementById('completion-percent').textContent = `${percent}%`;
    const progress = document.getElementById('progress');
    progress.max = problems.length;
    progress.value = count;
    progress.textContent = `${percent}%`;
  }
  function populateSolution(problem, solution) {
    if (solution.childElementCount) return;
    solution.append(element('h3', '', problem.method));
    const steps = element('ol');
    for (const step of problem.steps) {
      const item = element('li');
      const explanation = element('p');
      math.appendInline(step.text, explanation);
      item.append(explanation);
      if (step.math) {
        const equation = element('div', 'math-block');
        math.renderFormula(step.math, equation, true);
        item.append(equation);
      }
      steps.append(item);
    }
    const answer = element('div', 'answer');
    answer.append(element('span', 'answer-label', 'Final answer'));
    const equation = element('div', 'math-block');
    math.renderFormula(problem.answer, equation, true);
    answer.append(equation);
    solution.append(steps, answer);
  }

  if (!sets?.course?.problems?.length || !math || !window.katex) {
    const error = document.getElementById('load-error');
    error.hidden = false;
    error.textContent = 'The worksheet could not load. Keep the worksheet folder beside Open worksheet.html, then reopen the page.';
    return;
  }
  function renderSet(setId) {
  const set = sets[setId] || sets.course;
  problems = set.problems;
  window.INTEGRALS = problems;
  prefix = set.storagePrefix;
  cards.clear();
  previousCompletion = null;
  document.getElementById('undo-reset').hidden = true;
  list.replaceChildren();
  const jump = document.getElementById('jump');
  const topicJump = document.getElementById('topic-jump');
  jump.replaceChildren();
  topicJump.replaceChildren();
  topicJump.hidden = !problems[0].topic;
  document.getElementById('topic-jump-label').hidden = !problems[0].topic;
  document.getElementById('worksheet-subtitle').textContent = set.subtitle;
  const instructions = document.getElementById('worksheet-instructions');
  instructions.replaceChildren();
  math.appendInline(set.instructions, instructions);
  document.getElementById('worksheet-footer').textContent = set.footer;
  let currentTopic;
  let jumpGroup = jump;
  const fragment = document.createDocumentFragment();
  problems.forEach((problem, index) => {
    const number = index + 1;
    if (problem.topic && problem.topic !== currentTopic) {
      currentTopic = problem.topic;
      const topic = element('div', 'topic-heading');
      const topicTitle = element('h2', '', currentTopic);
      topicTitle.id = `topic-${problem.id}`;
      topicTitle.tabIndex = -1;
      topic.append(element('p', 'eyebrow', `${problem.section} / Questions ${number}–${number + 9}`), topicTitle);
      fragment.append(topic);
      const topicOption = element('option', '', currentTopic);
      topicOption.value = topicTitle.id;
      topicJump.append(topicOption);
      jumpGroup = element('optgroup');
      jumpGroup.label = currentTopic;
      jump.append(jumpGroup);
    }
    const card = element('article', 'question');
    card.id = problem.id;
    card.setAttribute('aria-labelledby', `title-${problem.id}`);
    const heading = element('div', 'question-heading');
    const title = element(problem.topic ? 'h3' : 'h2', '', `Question ${String(number).padStart(2, '0')}`);
    title.id = `title-${problem.id}`;
    title.tabIndex = -1;
    const completion = element('label', 'completion');
    const checkbox = element('input');
    checkbox.type = 'checkbox';
    checkbox.id = `complete-${problem.id}`;
    checkbox.setAttribute('aria-label', `Mark question ${number} complete`);
    checkbox.checked = read(problem.id, 'completed') === 'true';
    completion.append(checkbox, document.createTextNode('Complete'));
    const headingLabel = element('div', 'question-title');
    headingLabel.append(title);
    if (problem.difficulty) headingLabel.append(element('span', `difficulty difficulty-${problem.difficulty.toLowerCase()}`, problem.difficulty));
    heading.append(headingLabel, completion);
    const question = element('div', 'problem-math math-block');
    math.renderFormula(problem.question, question, true);
    const toggle = element('button', 'solution-toggle', 'Show Solution');
    toggle.type = 'button';
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', `solution-${problem.id}`);
    const solution = element('section', 'solution');
    solution.id = `solution-${problem.id}`;
    solution.setAttribute('aria-label', `Worked solution for question ${number}`);
    solution.hidden = true;
    toggle.addEventListener('click', () => {
      const opening = solution.hidden;
      if (opening) populateSolution(problem, solution);
      solution.hidden = !opening;
      toggle.textContent = opening ? 'Hide Solution' : 'Show Solution';
      toggle.setAttribute('aria-expanded', String(opening));
    });
    const label = element('label', 'notes-label', 'Your notes');
    label.htmlFor = `notes-${problem.id}`;
    const notes = element('textarea');
    notes.id = label.htmlFor;
    notes.rows = 3;
    notes.setAttribute('aria-label', `Notes for question ${number}`);
    notes.setAttribute('spellcheck', 'false');
    notes.setAttribute('autocorrect', 'off');
    notes.setAttribute('autocapitalize', 'off');
    notes.setAttribute('autocomplete', 'off');
    notes.setAttribute('aria-describedby', `preview-label-${problem.id}`);
    notes.placeholder = 'Work through it here… try (n+1)/(n+2) or $x^2$';
    notes.value = read(problem.id, 'notes') ?? '';
    const previewLabel = element('p', 'preview-label', 'Live math preview');
    previewLabel.id = `preview-label-${problem.id}`;
    const preview = element('div', 'notes-preview');
    preview.id = `preview-${problem.id}`;
    preview.setAttribute('role', 'region');
    preview.setAttribute('aria-label', `Math preview for question ${number}`);
    math.renderNotes(notes.value, preview);
    let previewTimer;
    notes.addEventListener('input', () => {
      // Persistence is synchronous on every keystroke; only rendering is debounced.
      save(problem.id, 'notes', notes.value);
      clearTimeout(previewTimer);
      previewTimer = setTimeout(() => math.renderNotes(notes.value, preview), 120);
    });
    checkbox.addEventListener('change', () => {
      save(problem.id, 'completed', String(checkbox.checked));
      updateProgress();
    });
    card.append(heading);
    if (problem.prompt) {
      const prompt = element('p', 'question-prompt');
      math.appendInline(problem.prompt, prompt);
      card.append(prompt);
    }
    card.append(question, toggle, solution, label, notes, previewLabel, preview);
    fragment.append(card);
    cards.set(problem.id, { card, checkbox, notes, preview });
    const option = element('option', '', `Question ${number}`);
    option.value = problem.id;
    jumpGroup.append(option);
  });
  list.append(fragment);
  updateProgress();
  }

  const setSelect = document.getElementById('worksheet-set');
  try {
    const savedSet = localStorage.getItem('integrals.active-set');
    if (savedSet && Object.hasOwn(sets, savedSet)) setSelect.value = savedSet;
  } catch (_) { storageFailure(); }
  renderSet(setSelect.value);
  setSelect.addEventListener('change', () => {
    try { localStorage.setItem('integrals.active-set', setSelect.value); }
    catch (_) { storageFailure(); }
    renderSet(setSelect.value);
  });
  document.getElementById('topic-jump').addEventListener('change', event => {
    document.getElementById(event.target.value)?.focus();
  });

  document.getElementById('jump').addEventListener('change', event => {
    document.getElementById(`title-${event.target.value}`).focus();
  });
  document.getElementById('reset').addEventListener('click', () => {
    previousCompletion = new Map();
    for (const [id, { checkbox }] of cards) {
      previousCompletion.set(id, checkbox.checked);
      if (checkbox.checked) {
        checkbox.checked = false;
        save(id, 'completed', 'false');
      }
    }
    updateProgress();
    document.getElementById('undo-reset').hidden = false;
  });
  document.getElementById('undo-reset').addEventListener('click', () => {
    if (!previousCompletion) return;
    for (const [id, checked] of previousCompletion) {
      cards.get(id).checkbox.checked = checked;
      save(id, 'completed', String(checked));
    }
    previousCompletion = null;
    updateProgress();
    document.getElementById('reset').focus();
    document.getElementById('undo-reset').hidden = true;
  });
  // A second open worksheet tab must not silently overwrite another tab's edits.
  window.addEventListener('storage', event => {
    if (!event.key?.startsWith(prefix)) return;
    const match = event.key.slice(prefix.length).match(/^(ans\d+)\.(notes|completed)$/);
    if (!match || !cards.has(match[1])) return;
    const entry = cards.get(match[1]);
    if (match[2] === 'notes') {
      entry.notes.value = event.newValue ?? '';
      math.renderNotes(entry.notes.value, entry.preview);
    } else {
      entry.checkbox.checked = event.newValue === 'true';
      updateProgress();
    }
  });
})();
