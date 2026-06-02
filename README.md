# CODHES 2026 LaTeX Paper Template

Converted from `CODHES 2026 Paper Template.docx` to a clean, open-source LaTeX template.

## Why LaTeX?

- **No Microsoft Word license required**
- **Free and open-source**
- **Superior typesetting quality** for academic papers
- **Version control friendly** (works with Git)
- **Cross-platform** (Windows, macOS, Linux)

## Files

- `codhes2026_template.tex` — Main LaTeX template file
- `references.bib` — BibTeX bibliography database (sample entries included)
- `README.md` — This file

## Compilation

### Requirements

- A TeX distribution: **TeX Live** (recommended), **MiKTeX**, or **MacTeX**
- `IEEEtran.cls` document class (included in most distributions)

### Compile the Template

Use the following commands in your terminal:

```bash
# Step 1: Compile main file
pdflatex codhes2026_template.tex

# Step 2: Process bibliography
bibtex codhes2026_template

# Step 3: Re-compile to resolve references
pdflatex codhes2026_template.tex
pdflatex codhes2026_template.tex
```

Or use an automated build tool like `latexmk`:

```bash
latexmk -pdf codhes2026_template.tex
```

### Using an IDE

Most LaTeX editors (TeXstudio, Overleaf, VS Code with LaTeX Workshop) handle compilation automatically. Just open `codhes2026_template.tex` and press the compile button.

## Template Structure

The template follows the exact structure of the original DOCX:

1. **Title** — 24pt, centered
2. **Authors & Affiliations** — Up to 6 authors in a 3-column grid
3. **Abstract** — 9pt bold, justified, 150–250 words
4. **Keywords** — Italic, indented
5. **Body Sections** — Two-column layout:
   - Introduction
   - Literature Review / Theoretical Framework
   - Method
   - Result and Discussion
   - Conclusion
6. **Acknowledgment** — Including Author Contributions
7. **Data Availability Statement**
8. **References** — IEEE citation style

## Customization

### Adding Authors

Edit the `\author{}` blocks in the preamble. Each block supports:

```latex
\author{%
    \IEEEauthorblockN{Given Name Surname}
    \IEEEauthorblockA{Department Name\\
    Organization Name\\
    City, Country\\
    email@example.com}
}
```

For fewer than 6 authors, remove the unused `\and` blocks.

For more than 6 authors, add additional rows using the same pattern.

### Adding Figures

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\columnwidth]{your-figure.pdf}
    \caption{Your figure caption.}
    \label{fig:your-label}
\end{figure}
```

### Adding Tables

```latex
\begin{table}[htbp]
    \centering
    \caption{Table caption.}
    \label{tab:your-label}
    \begin{tabular}{ccc}
        \toprule
        \tablecolhead{Column 1} & \tablecolhead{Column 2} \\
        \midrule
        \tablecopy{Data} & \tablecopy{Data} \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Adding References

Add new entries to `references.bib` in BibTeX format, then cite them:

```latex
\cite{Eason1955}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `IEEEtran.cls not found` | Install it via your TeX package manager (`tlmgr install ieeeconf` or `MiKTeX Console`) |
| Figures not showing | Ensure image files are in the same directory or provide the correct path |
| Overfull/underfull boxes | Tweak text or add `\sloppy` before the problematic paragraph |

## Notes on Formatting

This template replicates the DOCX formatting as closely as possible:

- **Font:** Times New Roman (via `times` package)
- **Page size:** A4
- **Margins:** ~45pt left/right, 54pt top, 72pt bottom
- **Body text:** 10pt, justified, first-line indent, 11.4pt line spacing
- **Headings:** Match DOCX spacing and italic styles for H2–H4
- **Tables/Figures:** 8pt captions and labels
- **References:** 8pt, IEEE format

## License

This template is provided for academic use. Please follow the CODHES 2026 conference submission guidelines for final formatting requirements.

## Credits

Converted from the official `CODHES 2026 Paper Template.docx` by [Your Name].
