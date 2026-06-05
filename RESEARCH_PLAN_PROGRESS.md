# CODHES 2026 Research Plan: 1-Week Sprint to Submission

**Researcher:** Yehezkiel Gunawan  
**Current Date:** 2025-06-05  
**Deadline:** 2025-06-15 (Phase 1) — 10 days remaining  
**Status:** Tool complete, data collection pending  

---

## Executive Summary

**Current State:** The analysis tool is fully functional with 25 tests passing. We have a working web application that can scrape, analyze, and export results. The LaTeX template is ready. 

**Goal:** Collect data from 10 documentation pairs, write the full paper, and submit within 10 days.

**Confidence Level:** High. The tool is ready; the main bottleneck is writing 8,000-10,000 words of academic English.

---

## Day-by-Day Plan

### Day 1: Data Collection (June 5-6)

**Morning (2-3 hours):**
- [ ] Identify 10 target platforms with both HTML docs and llms.txt
- [ ] Verify URLs are accessible
- [ ] Test scraping with the tool on 2-3 platforms

**Afternoon (2-3 hours):**
- [ ] Scrape all 10 HTML documentation pages
- [ ] Collect all 10 llm.txt files
- [ ] Validate data quality (word count, completeness)
- [ ] Save raw data to `data/` directory

**Evening (1 hour):**
- [ ] Export results as CSV
- [ ] Calculate descriptive statistics
- [ ] Verify we have sufficient data (> 30,000 words total)

**Target Platforms:**
1. FastAPI (fastapi.tiangolo.com)
2. LangChain (python.langchain.com)
3. Supabase (supabase.com/docs)
4. Vercel (vercel.com/docs)
5. Stripe (stripe.com/docs)
6. GitHub (docs.github.com)
7. Cloudflare (developers.cloudflare.com)
8. Anthropic (docs.anthropic.com)
9. Hugging Face (huggingface.co/docs)
10. Cursor (docs.cursor.com)

**Deliverable:** `data/` directory with 20 files (10 HTML + 10 llm.txt) + CSV analysis export

---

### Day 2: Deep Analysis (June 6-7)

**Morning (2-3 hours):**
- [ ] Run statistical analysis on collected data
- [ ] Paired t-test: HTML vs llm.txt (FRE, FKGL, token count)
- [ ] Effect size calculation (Cohen's d)
- [ ] Pearson correlation: lexical density ↔ token efficiency
- [ ] Generate summary statistics table

**Afternoon (2-3 hours):**
- [ ] Create publication-ready charts
  - Bar chart: Readability comparison (FRE)
  - Bar chart: Token count comparison
  - Scatter plot: FRE vs token ratio
  - Box plot: Distribution of differences
- [ ] Save charts as PNG/SVG to `paper/figures/`

**Evening (1 hour):**
- [ ] Write Results section outline
- [ ] Prepare tables for Results section
- [ ] Document findings in research notes

**Deliverable:** Statistical analysis complete + 4 charts ready

---

### Day 3: Paper Writing - Introduction + Related Work (June 7-8)

**Morning (3-4 hours):**
- [ ] Write Introduction (800-1000 words)
  - Background: HTML documentation bloat
  - The emergence of llm.txt (Sept 2024)
  - Research gap: no readability comparison exists
  - Three Research Questions (RQ1-3)

**Afternoon (3-4 hours):**
- [ ] Write Related Work (1200-1500 words)
  - Readability metrics: Flesch (1948), Kincaid (1975)
  - Tokenization: BPE (Sennrich et al., 2016)
  - LLM context windows: "Lost in the Middle" (Liu et al., 2023)
  - Prompt compression: LLMLingua (Jiang et al., 2023)
  - Documentation formats: plain text vs HTML
  - Gap analysis: no study compares HTML vs llm.txt

**Evening (1 hour):**
- [ ] Compile and verify LaTeX builds
- [ ] Check word count progress
- [ ] Review citations

**Deliverable:** 2,000-2,500 words written

---

### Day 4: Paper Writing - Methodology (June 8-9)

**Morning (3-4 hours):**
- [ ] Write Methodology (1500-2000 words)
  - Research design: Paired comparison, quantitative content analysis
  - Corpus selection: 10 platforms, criteria
  - Data collection: scraping protocol
  - Metrics: Table 2 (formulas, instruments)
  - Validation: spot checks, regex verification

**Afternoon (2-3 hours):**
- [ ] Write Analysis Procedure
  - Statistical tests: paired t-test, Cohen's d, Pearson correlation
  - Software: text-readability, js-tiktoken, Node.js
  - Validation steps

**Evening (1 hour):**
- [ ] Compile and verify
- [ ] Add methodology tables
- [ ] Review with advisor (if possible)

**Deliverable:** 3,500-4,500 words total

---

### Day 5: Paper Writing - Results (June 9-10)

**Morning (3-4 hours):**
- [ ] Write Results (2000-2500 words)
  - Descriptive statistics table
  - Readability comparison table
  - Token efficiency table
  - Lexical density analysis
  - Statistical significance (p-values, CI)
  - Insert charts (Figure 1, 2, 3)

**Afternoon (2-3 hours):**
- [ ] Write aggregate findings
- [ ] Create comparison tables
- [ ] Verify all charts display correctly
- [ ] Add figure captions

**Evening (1 hour):**
- [ ] Compile and verify
- [ ] Check word count: should be 5,500-7,000

**Deliverable:** Results section complete with all tables and charts

---

### Day 6: Paper Writing - Discussion + Conclusion (June 10-11)

**Morning (3-4 hours):**
- [ ] Write Discussion (1500-2000 words)
  - Interpretation: Why is llm.txt more token-efficient?
  - Implications for technical writers
  - Implications for LLM users
  - Limitations: small sample, English-only, no causal claims
  - Future work: expand to 50 platforms, Markdown comparison, user studies

**Afternoon (2-3 hours):**
- [ ] Write Conclusion (500-800 words)
  - Summarize key findings
  - Answer RQ1, RQ2, RQ3
  - Final statement

**Evening (1 hour):**
- [ ] Write Abstract (150-250 words)
- [ ] Write Keywords (5 terms)
- [ ] Compile and verify LaTeX

**Deliverable:** Full draft complete (8,000-10,000 words)

---

### Day 7: Polish and Quality Check (June 11-12)

**Morning (2-3 hours):**
- [ ] Spell check (aspell)
- [ ] Grammar check (Grammarly or similar)
- [ ] Verify all citations in IEEE format
- [ ] Check all figures/tables referenced in text
- [ ] Verify no placeholder text

**Afternoon (2-3 hours):**
- [ ] Run similarity check (Turnitin)
- [ ] Review with fresh eyes (or ask peer)
- [ ] Fix any compilation issues
- [ ] Generate final PDF

**Evening (1 hour):**
- [ ] Create submission package
- [ ] Prepare zip file (PDF + LaTeX source + figures)
- [ ] Verify file size < 10MB

**Deliverable:** Final PDF ready for submission

---

### Day 8: Submit (June 12-13)

**Morning (1-2 hours):**
- [ ] Log into CODHES CMT system
- [ ] Upload submission package
- [ ] Fill in metadata (title, authors, abstract, keywords)
- [ ] Select Track 14: Technolinguistics

**Afternoon (1 hour):**
- [ ] Verify submission received
- [ ] Save confirmation email
- [ ] Create git tag: `v1.0-submission`
- [ ] Push to GitHub

**Evening:**
- [ ] Celebrate! 🎉

**Deliverable:** Paper submitted to CODHES 2026

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Some platforms lack llm.txt** | Medium | High | Have 3 backup platforms ready (Next.js, Postman, Mintlify) |
| **LaTeX compilation errors** | Low | Medium | Test compilation daily; use Overleaf as fallback |
| **Word count short** | Medium | High | Expand discussion section; add examples |
| **Statistical significance weak** | Medium | Medium | Report as exploratory; focus on effect sizes |
| **Writing fatigue** | High | Medium | Write in 2-hour blocks; take breaks |
| **Turnitin similarity high** | Low | High | Check early; paraphrase if needed |

---

## Daily Writing Target

| Day | Section | Target Words | Cumulative |
|-----|---------|-------------|------------|
| 1 | - | - | - |
| 2 | - | - | - |
| 3 | Intro + Related Work | 2,500 | 2,500 |
| 4 | Methodology | 2,000 | 4,500 |
| 5 | Results | 2,500 | 7,000 |
| 6 | Discussion + Conclusion | 2,000 | 9,000 |
| 7 | Polish | - | 9,000+ |
| 8 | Submit | - | 9,000+ |

**Average daily writing:** 2,000 words (manageable in 4-5 hours)

---

## Tools Ready

- **Analysis:** `readibility-demo` web app (deployed or local)
- **Writing:** LaTeX template (`codhes2026_template.tex`)
- **Charts:** Python matplotlib or Chart.js (from analysis results)
- **Stats:** Python scipy (t-test, correlation)
- **Citation:** Zotero or Mendeley (if needed)

---

## Success Metrics

- [ ] 10 documentation pairs collected and analyzed
- [ ] 25 tests passing (current: ✅ 25/25)
- [ ] 8,000+ words in final paper
- [ ] All charts publication-ready
- [ ] Statistical tests complete
- [ ] LaTeX compiles with 0 errors
- [ ] Turnitin similarity < 20%
- [ ] Submitted before June 15, 2026

---

## Motivation

**Why this is achievable:**
1. The hard part (tool building) is DONE
2. We have 10 days, not 2 weeks
3. The data is public and accessible
4. The analysis is automated
5. The paper structure is clear (6 sections)

**Why this matters:**
- First academic study on llm.txt readability
- Novel contribution to technolinguistics
- Direct impact on technical writing practices
- Conference presentation opportunity

---

**Let's do this. 🚀**
