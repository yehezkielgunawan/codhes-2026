# Results Section Outline - CODHES 2026 Paper

**Date:** June 8, 2026
**Phase:** Day 3 Evening - Results Section Preparation
**Section:** Results (Target: 2,000-2,500 words)

---

## 1. Results Section Structure

### 1.1 Descriptive Statistics (300-400 words)
**Purpose:** Present baseline characteristics of the corpus

**Content:**
- Overview of 10 platforms analyzed (Table 1)
- Document type distribution (all 10 have both human and machine versions)
- Content volume summary (word counts, token counts)
- Platform categories (frameworks, platforms, infrastructure, tools)

**Table 1:** Platform Characteristics
| Platform | Category | Human Words | Machine Words | Human Tokens | Machine Tokens |
|----------|----------|-------------|-------------|--------------|----------------|
| React | UI Framework | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

---

### 1.2 Traditional Readability Analysis (500-600 words)
**Purpose:** Answer RQ1: Do machine docs differ in traditional readability?

**Content:**
- Flesch Reading Ease comparison (human vs machine)
- Flesch-Kincaid Grade Level comparison
- Lexical Density analysis
- Paired samples t-test results
- Effect sizes (Cohen's d)

**Key Findings to Report:**
- FRE: Human mean = 33.39, Machine mean = -58.19 (but high variance SD=155.28)
- FKGL: Human mean = 13.76, Machine mean = 23.96 (+10.2 grade levels)
- Lexical Density: Minimal difference (76.86% vs 77.25%)
- 8/10 platforms show lower FRE for machine docs
- 2 outliers (React, LangChain) with extreme negative FRE in machine docs

**Table 2:** Traditional Readability Metrics
| Metric | Human Mean (SD) | Machine Mean (SD) | Cohen's d | Effect Size |
|--------|----------------|-------------------|-----------|-------------|
| Flesch Reading Ease | 33.39 (28.66) | -58.18 (155.28) | 0.573 | Medium |
| Flesch-Kincaid Grade | 13.76 (6.18) | 23.96 (20.91) | -0.459 | Small |
| Lexical Density (%) | 76.86 (9.23) | 77.25 (8.70) | -0.028 | Negligible |
| Token-to-Word Ratio | 1.67 (0.36) | 2.73 (1.48) | -0.661 | Medium |

**Figure 1:** Bar chart showing FRE and LRI comparison across platforms

---

### 1.3 LLM-as-a-Judge Evaluation Results (500-600 words)
**Purpose:** Answer RQ2: Do LLM scores favor machine-optimized docs?

**Content:**
- Overview of LLM evaluation methodology (5 dimensions, 1-5 Likert scale)
- LLM Readability Index (LRI) calculation and interpretation
- Platform-by-platform comparison
- Paired samples t-test results
- Effect sizes for each dimension

**Key Findings to Report:**
- LRI: Human mean = 64.03, Machine mean = 78.72 (+14.69 points, p=0.005)
- All 5 LLM dimensions favor machine docs (except Technical Accuracy: small effect)
- Largest effects: LLM-Friendliness (d=-1.371), Conciseness (d=-1.347)
- 8/10 platforms show higher machine LRI
- 1 platform (Vercel) favors human docs
- 1 platform (LangChain) shows no difference

**Table 3:** LLM-as-a-Judge Evaluation Results
| Dimension | Human Mean (SD) | Machine Mean (SD) | Cohen's d | Effect Size |
|-----------|----------------|-------------------|-----------|-------------|
| Clarity | 3.50 (0.51) | 4.08 (0.71) | -1.002 | Large |
| Completeness | 3.38 (0.51) | 4.01 (0.78) | -0.964 | Large |
| Conciseness | 3.38 (0.58) | 4.14 (0.81) | -1.347 | Large |
| Technical Accuracy | 4.20 (0.59) | 4.36 (0.89) | -0.245 | Small |
| LLM-Friendliness | 3.35 (0.58) | 4.16 (0.82) | -1.371 | Large |
| **LRI (Overall)** | **64.03 (12.13)** | **78.72 (18.88)** | **-1.172** | **Large** |

**Table 4:** Platform-by-Platform LRI Comparison
| Platform | Human LRI | Machine LRI | Δ LRI | Direction |
|----------|-----------|-------------|-------|-----------|
| FastAPI | 87.00 | 100.00 | +13.00 | Machine |
| Cursor | 75.00 | 100.00 | +25.00 | Machine |
| ... | ... | ... | ... | ... |

**Figure 2:** Box plot showing distribution of LRI differences

---

### 1.4 Correlation Analysis (300-400 words)
**Purpose:** Answer RQ3: Are traditional metrics sufficient for LLM docs?

**Content:**
- Pearson correlation between traditional and LLM metrics
- Interpretation of independence
- Implications for documentation evaluation

**Key Findings to Report:**
- No significant correlations (p > 0.05) between traditional metrics and LLM scores
- Weak positive trend: FRE vs LLM-Friendliness (r=0.357, p=0.312)
- Implication: Traditional metrics and LLM scores measure distinct constructs

**Table 5:** Pearson Correlations (Traditional vs LLM Metrics)
| Traditional Metric | LLM Metric | r | p-value |
|-------------------|------------|------|---------|
| FRE | LRI | 0.234 | 0.513 |
| FRE | Clarity | 0.219 | 0.539 |
| ... | ... | ... | ... |

**Figure 3:** Scatter plot of FRE vs LLM Clarity

---

### 1.5 Synthesis and Key Patterns (300-400 words)
**Purpose:** Integrate findings and highlight patterns

**Content:**
- Summary of paradox: Human docs = higher FRE, lower LRI; Machine docs = lower FRE, higher LRI
- Platform-specific patterns (exceptions, outliers)
- Token efficiency implications
- Practical significance vs statistical significance

**Key Patterns:**
- **Inverse relationship:** Traditional readability and LLM preference are inversely related
- **Outlier sensitivity:** React and LangChain machine docs show extreme FRE scores but moderate LRI
- **Consistent LLM preference:** 8/10 platforms show machine docs preferred by LLM
- **Token efficiency trade-off:** Higher TWR for machine docs suggests more token overhead

---

## 2. Tables for Results Section

### Table 1: Platform Characteristics
- Columns: Platform, Category, Human Words, Machine Words, Human Tokens, Machine Tokens
- Purpose: Describe corpus

### Table 2: Traditional Readability Metrics
- Columns: Metric, Human Mean, Machine Mean, Cohen's d, Effect Size
- Purpose: Answer RQ1

### Table 3: LLM-as-a-Judge Evaluation Results
- Columns: Dimension, Human Mean, Machine Mean, Cohen's d, Effect Size
- Purpose: Answer RQ2

### Table 4: Platform-by-Platform LRI Comparison
- Columns: Platform, Human LRI, Machine LRI, Δ LRI, Direction
- Purpose: Show individual variation

### Table 5: Pearson Correlations
- Columns: Traditional Metric, LLM Metric, Pearson r, p-value
- Purpose: Answer RQ3

---

## 3. Figures for Results Section

### Figure 1: Readability Comparison (Dual Bar Chart)
- Left: FRE comparison (human vs machine)
- Right: LRI comparison (human vs machine)
- Purpose: Visualize RQ1 and RQ2 side by side

### Figure 2: Token-to-Word Ratio Comparison
- Bar chart: Human vs Machine TWR for each platform
- Purpose: Show tokenization efficiency differences

### Figure 3: FRE vs LLM Clarity Scatter Plot
- X-axis: Flesch Reading Ease
- Y-axis: LLM Clarity Score (1-5)
- Points: Human (circles) vs Machine (squares)
- Labels: Platform names
- Purpose: Visualize relationship between traditional and LLM metrics

### Figure 4: LRI Difference Distribution
- Box plot of (Machine LRI - Human LRI) differences
- Individual points labeled by platform
- Reference line at y=0 (no difference)
- Purpose: Show distribution and outliers

---

## 4. Key Statistics to Report

### Statistical Tests:
- Paired t-test (LRI): t=-3.706, df=9, p=0.005
- Paired t-test (FRE): t=1.812, df=9, p=0.104
- Paired t-test (FKGL): t=-1.452, df=9, p=0.179

### Effect Sizes:
- LRI: d=-1.172 (Large)
- Conciseness: d=-1.347 (Large)
- LLM-Friendliness: d=-1.371 (Large)
- Clarity: d=-1.002 (Large)
- Completeness: d=-0.964 (Large)
- FRE: d=0.573 (Medium)

### Descriptive Statistics:
- n = 10 platforms (20 document pairs)
- 8/10 platforms favor machine docs (80%)
- 1/10 platforms favor human docs (10%)
- 1/10 platforms show no difference (10%)

---

## 5. Research Questions Answered

### RQ1: Traditional Readability Differences
**Answer:** Machine docs show lower Flesch Reading Ease (mixed results due to outliers) but higher Flesch-Kincaid Grade Level (+10.2 grade levels). Lexical Density shows negligible difference. Token-to-Word Ratio is higher for machine docs.

### RQ2: LLM Preference for Machine Docs
**Answer:** Yes, strongly. Large effect sizes across all LLM dimensions (d > -0.96). LRI shows statistically significant difference (p=0.005) with machine docs scoring +14.69 points higher. 8/10 platforms favor machine docs.

### RQ3: Sufficiency of Traditional Metrics
**Answer:** No. No significant correlations between traditional metrics (FRE, FKGL) and LLM scores (LRI, Clarity, etc.). These measure distinct constructs — traditional for human readers, LLM for machine consumption.

---

*Outline prepared for Results section (2,000-2,500 words)*
