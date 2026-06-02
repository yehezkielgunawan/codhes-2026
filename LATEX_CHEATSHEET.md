# LaTeX Quick Cheatsheet for CODHES 2026

## Essential Commands

| Command | What it does |
|---------|-------------|
| `pdflatex file.tex` | Compile LaTeX to PDF (basic) |
| `bibtex file` | Process bibliography (run after first pdflatex) |
| `latexmk -pdf file.tex` | Auto-compile (runs pdflatex + bibtex + pdflatex) |
| `latexmk -pvc file.tex` | Auto-recompile on file changes (live preview) |

## Full Compile Workflow for This Template

```bash
pdflatex codhes2026_template.tex
bibtex codhes2026_template
pdflatex codhes2026_template.tex
pdflatex codhes2026_template.tex
```

Or simply:
```bash
latexmk -pdf codhes2026_template.tex
```

## Common File Extensions

| Extension | Meaning |
|-----------|---------|
| `.tex` | LaTeX source file |
| `.bib` | BibTeX bibliography database |
| `.pdf` | Output PDF |
| `.aux` | Auxiliary file (cross-references, citations) |
| `.log` | Compilation log (check for errors) |
| `.bbl` | Generated bibliography |
| `.blg` | BibTeX log |
| `.toc` | Table of contents data |

## Useful Tips

- **Check errors**: Open `codhes2026_template.log` and search for `!` or `Error`
- **Clean temp files**: `latexmk -c` or manually delete `.aux`, `.log`, `.bbl`, etc.
- **Install missing packages**: `tlmgr install <package-name>`
- **Update packages**: `tlmgr update --self && tlmgr update --all`

## Key LaTeX Syntax in This Template

| What you want | How to write it |
|---------------|-----------------|
| **Bold text** | `\textbf{bold}` |
| *Italic text* | `\textit{italic}` |
| Math inline | `$E = mc^2$` |
| Math display | `\[ E = mc^2 \]` |
| Citation | `\cite{Eason1955}` |
| Figure reference | `Fig.~\ref{fig:label}` |
| Table reference | `Table~\ref{tab:label}` |
| Section | `\section{Title}` |
| Subsection | `\subsection{Title}` |
| Sub-subsection | `\subsubsection{Title}` |
| New paragraph | Leave a blank line |
| Forced line break | `\\` |
| Non-breaking space | `~` |
| En-dash | `--` |
| Em-dash | `---` |
| Quotation marks | ``quoted'' |
| Ellipsis | `\ldots` |
| Superscript | `\textsuperscript{a}` |
| Subscript | `$\mu_0$` |

## Adding a Figure

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\columnwidth]{image-file.pdf}
    \caption{Your caption here.}
    \label{fig:your-label}
\end{figure}
```

## Adding a Table

```latex
\begin{table}[htbp]
    \centering
    \caption{Table caption.}
    \label{tab:your-label}
    \begin{tabular}{ccc}
        \toprule
        \tablecolhead{Col 1} & \tablecolhead{Col 2} \\
        \midrule
        \tablecopy{Data} & \tablecopy{Data} \\
        \bottomrule
    \end{tabular}
\end{table}
```

## Adding a Reference to `references.bib`

```bibtex
@article{Smith2026,
  author  = {J. Smith and A. Doe},
  title   = {Title of the Paper},
  journal = {Journal Name},
  volume  = {10},
  number  = {2},
  pages   = {100--120},
  year    = {2026}
}
```

Then cite it: `\cite{Smith2026}`

## Recommended LaTeX Editors

- **VS Code** with [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) extension
- **TeXstudio** (free, cross-platform)
- **Overleaf** (online, no installation needed)

## Where to Learn More

- [Overleaf Learn LaTeX](https://www.overleaf.com/learn) — Best for beginners
- [LaTeX Project Documentation](https://www.latex-project.org/help/documentation/) — Official docs
- [CTAN (Comprehensive TeX Archive Network)](https://ctan.org/) — All packages
- [IEEEtran Documentation](https://www.ctan.org/pkg/ieeetran) — For this template's class

## Troubleshooting Common Issues

| Problem | Fix |
|---------|-----|
| `File not found` | Check path or run `tlmgr install <package>` |
| `Overfull \hbox` | Text too wide; break words or adjust spacing |
| `Citation undefined` | Run `bibtex` then `pdflatex` twice |
| `Reference undefined` | Re-run `pdflatex` |
| `pdfTeX error` | Check `*.log` file for specific error message |

## What Was Installed

The `brew install texlive` command installed:
- **pdflatex** — PDF compiler
- **bibtex** — Bibliography processor
- **xelatex** — Modern compiler (supports system fonts)
- **lualatex** — Lua-based compiler (most modern)
- **latexmk** — Auto-build tool
- **tlmgr** — TeX Live package manager
- Thousands of LaTeX packages (graphics, math, fonts, etc.)

Installation location: `/opt/homebrew/Cellar/texlive/20260301/`

## Uninstall (if ever needed)

```bash
brew uninstall texlive
```
