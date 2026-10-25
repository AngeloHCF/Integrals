# Integration practice

1. Double-click **Open worksheet.html** in this folder to open the worksheet in Chrome, Edge, or Firefox.
2. Check off questions and type in the notes boxes. Both save automatically in the same browser and restore when you reopen the same file.
3. Click **Show Solution** for the worked steps and final answer. Click **Hide Solution** to hide them again.

The new set has **100 questions across your 10 course topics**: 70 medium, 20 hard, and 10 tricky, with 10 questions per topic. Use **Topic** to jump to a section. It covers u-substitution, integration by parts, trig integrals, trigonometric substitution, partial fractions, mixed techniques, improper integrals, areas between curves, volumes by slicing, and cylindrical shells.

Your earlier questions and saved work are available under **Question set → Original 100**. The two sets keep separate notes and progress, so old notes never get attached to different questions.

Everything works offline. No server or installation is needed. Keep the `worksheet` folder beside `Open worksheet.html`.

Notes preview math such as `a^x`, `a/b`, `(n+1)/(n+2)`, and `x^(n+1)`. Use `$...$` for math inside ordinary text, or enter LaTeX such as `\frac{x^2}{2}`. Spelling correction and automatic capitalization are disabled.

**Reset progress** clears only checkmarks; your notes stay. **Undo reset** restores the previous checkmarks. Saved data belongs to this browser and file location; keep using the same file, and avoid private browsing or clearing browser data if you want to retain it.

The original LaTeX and PDF are still available: `main.tex` and `output/pdf/integration-techniques-interactive.pdf`. The PDF answer toggles work in Adobe Acrobat Reader.

## Editing the content

Edit `scripts/course_content.py` for the new course questions and worked solutions. The original set still comes from `main.tex` and the two `worksheet/steps-*.json` files. Regenerate the browser content after edits with:

```powershell
python scripts/build_worksheet.py
```

To rebuild the original PDF: `latexmk -pdf main.tex`.

## Developer checks

These tools are only needed for development, never for opening the worksheet:

- `python scripts/verify_math.py` checks every original answer by differentiation (requires SymPy and `antlr4-python3-runtime==4.11.1`).
- `python scripts/verify_course.py` checks the new answers, exact definite/improper integrals, and area/volume expressions with the same dependencies.
- `node scripts/verify_worksheet.cjs` checks local asset loading, all formulas and solutions, note previews, saved-state restoration, reset, and safe handling of unavailable storage (requires `jsdom` on Node's module path).

Math rendering uses the bundled [KaTeX](https://katex.org/docs/browser) 0.19.0 assets and fonts. Its license is in `worksheet/vendor/KATEX-LICENSE.txt`.
