# CODHES 2026 Submission Package

## Paper
- **Title:** From Human-Centric to Machine-Optimized: A Technolinguistic Analysis of Documentation Readability in llm.txt Standards
- **Author:** Yehezkiel Gunawan
- **Track:** Track 14: Technolinguistics
- **Conference:** CODHES 2026 (International Conference on Digital Humanities and Social Sciences)
- **Date:** June 2026

## Files Included

### Main Paper
- `codhes2026_paper.pdf` - Final PDF (7 pages, IEEEtran format)
- `codhes2026_paper.tex` - LaTeX source file
- `references.bib` - BibTeX bibliography (24 references)

### Figures
- `figures/figure1_readability_comparison.png` - Traditional readability metrics comparison
- `figures/figure2_token_comparison.png` - Token count comparison
- `figures/figure3_fre_vs_clarity.png` - FRE vs LLM clarity scatter plot
- `figures/figure4_lri_difference_boxplot.png` - LRI difference boxplot
- `figures/figure5_effect_sizes.png` - Cohen's d effect sizes visualization
- All figures also available in SVG format

## Data and Code
All research data, analysis scripts, and raw results are openly available at:
https://github.com/yehezkielgunawan/readability-python-demo

### Repository Contents
- `results/results.csv` - Traditional readability metrics for 10 platforms
- `results/llm_evaluation.csv` - LLM-as-a-Judge evaluation scores
- `results/analysis/` - Statistical analysis reports and summary statistics
- `results/figures/` - Publication-ready charts
- `src/` - Python source code for the readability auditor tool
- `tests/` - 50 passing tests

## Key Findings
1. **Readability Paradox:** Machine-optimized documentation (llm.txt) scores lower on traditional human readability metrics but significantly higher on LLM evaluation
2. **Statistical Significance:** Paired t-test for LRI: t=-3.706, p=0.005
3. **Large Effect Sizes:** Cohen's d ranging from -1.002 to -1.371 across LLM dimensions
4. **No Correlation:** Traditional metrics (FRE, FKGL) do not correlate with LLM scores

## Compilation
To compile the LaTeX paper:
```bash
pdflatex codhes2026_paper.tex
bibtex codhes2026_paper.aux
pdflatex codhes2026_paper.tex
pdflatex codhes2026_paper.tex
```

## Contact
- GitHub: @yehezkielgunawan
- Email: yehezkiel.gunawan@binus.ac.id
