# Statistical Analysis Report - CODHES 2026

**Date:** June 8, 2026
**Phase:** Day 3 Morning - Statistical Analysis
**Analyst:** Yehezkiel Gunawan
**Tool:** Python (scipy, pandas, numpy)

---

## Executive Summary

Statistical analysis completed for all 10 technical documentation platforms (n=20 document pairs). Key findings:

1. **Significant paired difference in LRI** (p=0.005): Machine docs score +14.69 points higher on average
2. **Large effect sizes** for LLM-related metrics: LRI (d=-1.172), Conciseness (d=-1.347), LLM-Friendliness (d=-1.371)
3. **No significant correlations** between traditional readability metrics and LLM scores, suggesting these measure distinct constructs
4. **8 out of 10 platforms** show higher LLM preference for machine-optimized documentation

---

## 1. Descriptive Statistics

### Table 1: Summary Statistics by Document Type

| Metric                   | Human Mean | Human SD | Human Min | Human Max | Machine Mean | Machine SD | Machine Min | Machine Max | Mean Diff |
| ------------------------ | ---------- | -------- | --------- | --------- | ------------ | ---------- | ----------- | ----------- | --------- |
| Flesch Reading Ease      | 33.39      | 28.66    | -42.30    | 54.80     | -58.18       | 155.28     | -430.09     | 36.81       | +91.58    |
| Flesch-Kincaid Grade     | 13.76      | 6.18     | 8.38      | 29.96     | 23.96        | 20.91      | 10.83       | 74.53       | -10.20    |
| Lexical Density (%)      | 76.86      | 9.23     | 63.93     | 93.87     | 77.25        | 8.70       | 64.82       | 91.14       | -0.40     |
| Token-to-Word Ratio      | 1.67       | 0.36     | 1.32      | 2.44      | 2.73         | 1.48       | 1.74        | 5.57        | -1.06     |
| LLM Readability Index    | 64.03      | 12.13    | 50.00     | 87.00     | 78.72        | 18.88      | 42.00       | 100.00      | -14.69    |
| Clarity (1-5)            | 3.50       | 0.51     | 3.00      | 4.40      | 4.08         | 0.71       | 3.00        | 5.00        | -0.58     |
| Completeness (1-5)       | 3.38       | 0.51     | 3.00      | 4.40      | 4.01         | 0.78       | 2.60        | 5.00        | -0.63     |
| Conciseness (1-5)        | 3.38       | 0.58     | 2.60      | 4.20      | 4.14         | 0.81       | 2.60        | 5.00        | -0.76     |
| Technical Accuracy (1-5) | 4.20       | 0.59     | 3.00      | 5.00      | 4.36         | 0.89       | 2.60        | 5.00        | -0.16     |
| LLM-Friendliness (1-5)   | 3.35       | 0.58     | 2.60      | 4.40      | 4.16         | 0.82       | 2.60        | 5.00        | -0.81     |

**Key Observations:**

- Machine docs show **higher FRE on average** (+91.58 points), but with extreme variance (SD=155.28) due to outlier platforms (React: -430.09, LangChain: -234.73)
- Human docs show **lower FRE variance** (SD=28.66), indicating more consistent readability
- Machine docs score higher on **all LLM dimensions** except Vercel (see exceptions)
- **Token-to-Word Ratio** is substantially higher for machine docs (2.73 vs 1.67), suggesting more tokenization overhead

---

## 2. Effect Size Analysis (Cohen's d)

### Table 2: Paired Comparison Effect Sizes

| Metric                | Cohen's d | Effect Size    | Mean Diff | Std Diff |
| --------------------- | --------- | -------------- | --------- | -------- |
| Flesch Reading Ease   | 0.573     | **Medium**     | 91.58     | 159.89   |
| Flesch-Kincaid Grade  | -0.459    | **Small**      | -10.19    | 22.19    |
| Lexical Density       | -0.028    | **Negligible** | -0.40     | 14.12    |
| Token-to-Word Ratio   | -0.661    | **Medium**     | -1.06     | 1.60     |
| LLM Readability Index | -1.172    | **Large**      | -14.69    | 12.54    |
| Clarity               | -1.002    | **Large**      | -0.58     | 0.57     |
| Completeness          | -0.964    | **Large**      | -0.63     | 0.65     |
| Conciseness           | -1.347    | **Large**      | -0.76     | 0.56     |
| Technical Accuracy    | -0.245    | **Small**      | -0.16     | 0.65     |
| LLM-Friendliness      | -1.371    | **Large**      | -0.81     | 0.59     |

**Interpretation:**

- **Negative d values** indicate machine docs score higher than human docs (since we calculated human - machine)
- **Large effects** for all LLM dimensions (except Technical Accuracy) confirm substantial practical significance
- **Conciseness** shows the largest effect (d=-1.347), suggesting machine docs are perceived as significantly more concise
- **LLM-Friendliness** shows second-largest effect (d=-1.371), validating the core hypothesis
- **FRE shows medium effect** (d=0.573) but high variance due to extreme outliers
- **Lexical Density shows negligible effect**, suggesting both formats are similarly dense

---

## 3. Correlation Analysis

### Table 3: Pearson Correlations (Traditional vs LLM Metrics)

**Human Documents:**

| Traditional Metric  | LLM Metric         | r      | p-value | Significant? |
| ------------------- | ------------------ | ------ | ------- | ------------ |
| FRE                 | LRI                | 0.234  | 0.513   | No           |
| FRE                 | Clarity            | 0.219  | 0.539   | No           |
| FRE                 | Completeness       | 0.295  | 0.409   | No           |
| FRE                 | Conciseness        | 0.198  | 0.579   | No           |
| FRE                 | Technical Accuracy | 0.103  | 0.777   | No           |
| FRE                 | LLM-Friendliness   | 0.357  | 0.312   | No           |
| FKGL                | LRI                | -0.210 | 0.557   | No           |
| Lexical Density     | LRI                | -0.223 | 0.533   | No           |
| Token-to-Word Ratio | LRI                | 0.103  | 0.777   | No           |

**Key Findings:**

- **No significant correlations** (p < 0.05) between any traditional metric and LLM scores
- **Weak positive trend** between FRE and LLM-Friendliness (r=0.357), but not statistically significant
- **Implication:** Traditional readability metrics and LLM-as-a-Judge scores measure **distinct constructs** — validating the need for both approaches

---

## 4. Inferential Statistics

### Paired Samples t-test (LLM Readability Index)

- **t-statistic:** -3.706
- **p-value:** 0.005
- **Degrees of freedom:** 9
- **Conclusion:** **Statistically significant difference** (p < 0.01) between human and machine LRI scores

### Platform-by-Platform LRI Comparison

| Platform   | Human LRI | Machine LRI | Δ LRI      | Direction |
| ---------- | --------- | ----------- | ---------- | --------- |
| Stripe     | 55.00     | 80.00       | +25.00     | Machine   |
| FastAPI    | 87.00     | 100.00      | +13.00     | Machine   |
| Hono       | 73.33     | 87.00       | +13.67     | Machine   |
| Cursor     | 75.00     | 100.00      | +25.00     | Machine   |
| Supabase   | 56.00     | 82.00       | +26.00     | Machine   |
| GitHub     | 55.00     | 81.25       | +26.25     | Machine   |
| **Vercel** | **54.00** | **42.00**   | **-12.00** | **Human** |
| Cloudflare | 63.00     | 80.00       | +17.00     | Machine   |
| React      | 72.00     | 85.00       | +13.00     | Machine   |
| LangChain  | 50.00     | 50.00       | 0.00       | Tie       |

- **8/10 platforms** favor machine docs (80%)
- **1/10 platforms** favors human docs (10%)
- **1/10 platforms** shows no difference (10%)

---

## 5. Scientific Interpretation

### Research Question 1: Do machine-optimized docs score differently on traditional readability?

**Finding:** Mixed results. FRE shows high variance due to outliers (React, LangChain machine docs extremely negative), but FKGL shows consistent increase for machine docs (+10.2 grade levels on average). This suggests machine docs are **more difficult for human readers** (higher grade level) but the FRE paradox is complicated by extreme outliers.

### Research Question 2: Do LLM-as-a-Judge scores favor machine-optimized docs?

**Finding:** **Yes, strongly.** Large effect sizes across all LLM dimensions (d > -0.96 for all except Technical Accuracy). LRI shows large effect (d=-1.172) and statistically significant paired difference (p=0.005). This provides robust empirical support for the hypothesis that LLMs perceive machine-optimized documentation as higher quality.

### Research Question 3: Are traditional readability metrics sufficient for evaluating LLM-optimized docs?

**Finding:** **No.** The lack of significant correlations between traditional metrics (FRE, FKGL) and LLM scores (LRI, Clarity, etc.) suggests these measure **different constructs**. Traditional metrics were designed for human readers (school texts, 1948-1975); LLM scores capture machine-perceived quality. This validates the **complementary need** for both metrics in evaluating modern documentation.

---

## 6. Limitations

1. **Small sample size** (n=10): Results are exploratory; larger samples needed for generalization
2. **Single LLM evaluator** (Llama 3.2 3B): Multi-model consensus would strengthen validity
3. **Outlier sensitivity** (React, LangChain FRE): Extreme values skew traditional metrics; consider robust statistics or outlier analysis
4. **English-only** corpus: Results may not generalize to non-English documentation
5. **Technical docs only** (frameworks, platforms): Results may not generalize to other documentation genres

---

## 7. Files Generated

All analysis artifacts saved to `readability-python-demo/results/analysis/`:

- `merged_dataset.csv` — Combined traditional + LLM metrics for all 10 platforms
- `effect_sizes.csv` — Cohen's d calculations for all 10 metrics
- `correlations.csv` — Pearson correlations between traditional and LLM metrics
- `summary_statistics.csv` — Full descriptive statistics table
- `statistical_analysis_report.md` — This report

---

## 8. Next Steps

**Afternoon Tasks (Day 3):**

- [ ] Create publication-ready charts (matplotlib/seaborn)
  - Bar chart: Readability comparison (FRE + LRI scores)
  - Bar chart: Token count comparison
  - Scatter plot: FRE vs LLM clarity score
  - Box plot: Distribution of LRI differences
- [ ] Save charts as PNG/SVG to `paper/figures/`

**Evening Tasks (Day 3):**

- [ ] Write Results section outline
- [ ] Prepare tables for Results section
- [ ] Document findings in research notes

---

_Report generated by statistical_analysis.py on June 8, 2026_
