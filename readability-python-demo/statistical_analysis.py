"""
Statistical Analysis Script for CODHES 2026 Paper
Day 3 Morning Task: Effect size, Pearson correlation, summary statistics
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# Configuration
RESULTS_DIR = Path("./results")
OUTPUT_DIR = Path("./results/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)


def cohens_d_paired(x, y):
    """
    Calculate Cohen's d for paired samples.
    d = mean(diff) / std(diff)
    """
    diff = np.array(x) - np.array(y)
    mean_diff = np.mean(diff)
    std_diff = np.std(diff, ddof=1)
    
    if std_diff == 0:
        return 0.0
    
    return mean_diff / std_diff


def interpret_cohens_d(d):
    """Interpret Cohen's d effect size."""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "Negligible"
    elif abs_d < 0.5:
        return "Small"
    elif abs_d < 0.8:
        return "Medium"
    else:
        return "Large"


def load_data():
    """Load and merge traditional metrics with LLM scores."""
    # Load traditional metrics
    results = pd.read_csv(RESULTS_DIR / "results.csv")
    
    # Load LLM evaluation
    llm_eval = pd.read_csv(RESULTS_DIR / "llm_evaluation.csv")
    
    # Pivot LLM data to have human and machine side by side
    llm_human = llm_eval[llm_eval['doc_type'] == 'human_docs'].set_index('base_url')
    llm_machine = llm_eval[llm_eval['doc_type'] == 'llm.txt'].set_index('base_url')
    
    # Create merged dataset
    data = []
    for _, row in results.iterrows():
        url = row['base_url']
        
        if url in llm_human.index and url in llm_machine.index:
            data.append({
                'platform': url,
                'human_fre': row['human_fre'],
                'human_fk': row['human_fk'],
                'human_ld': row['human_ld'],
                'human_twr': row['human_twr'],
                'human_lri': row['human_lri'],
                'machine_fre': row['machine_fre'],
                'machine_fk': row['machine_fk'],
                'machine_ld': row['machine_ld'],
                'machine_twr': row['machine_twr'],
                'machine_lri': row['machine_lri'],
                'human_clarity': llm_human.loc[url, 'clarity'],
                'human_completeness': llm_human.loc[url, 'completeness'],
                'human_conciseness': llm_human.loc[url, 'conciseness'],
                'human_technical': llm_human.loc[url, 'technical_accuracy'],
                'human_llm_friendly': llm_human.loc[url, 'llm_friendliness'],
                'machine_clarity': llm_machine.loc[url, 'clarity'],
                'machine_completeness': llm_machine.loc[url, 'completeness'],
                'machine_conciseness': llm_machine.loc[url, 'conciseness'],
                'machine_technical': llm_machine.loc[url, 'technical_accuracy'],
                'machine_llm_friendly': llm_machine.loc[url, 'llm_friendliness'],
            })
    
    return pd.DataFrame(data)


def calculate_effect_sizes(df):
    """Calculate Cohen's d for paired comparisons."""
    metrics = [
        ('Flesch Reading Ease', 'human_fre', 'machine_fre'),
        ('Flesch-Kincaid Grade', 'human_fk', 'machine_fk'),
        ('Lexical Density', 'human_ld', 'machine_ld'),
        ('Token-to-Word Ratio', 'human_twr', 'machine_twr'),
        ('LLM Readability Index', 'human_lri', 'machine_lri'),
        ('Clarity', 'human_clarity', 'machine_clarity'),
        ('Completeness', 'human_completeness', 'machine_completeness'),
        ('Conciseness', 'human_conciseness', 'machine_conciseness'),
        ('Technical Accuracy', 'human_technical', 'machine_technical'),
        ('LLM-Friendliness', 'human_llm_friendly', 'machine_llm_friendly'),
    ]
    
    results = []
    for name, human_col, machine_col in metrics:
        d = cohens_d_paired(df[human_col], df[machine_col])
        results.append({
            'Metric': name,
            'Cohen_d': round(d, 3),
            'Effect_Size': interpret_cohens_d(d),
            'Mean_Diff': round(np.mean(df[human_col] - df[machine_col]), 2),
            'Std_Diff': round(np.std(df[human_col] - df[machine_col], ddof=1), 2),
        })
    
    return pd.DataFrame(results)


def calculate_correlations(df):
    """Calculate Pearson correlations between traditional and LLM metrics."""
    correlations = []
    
    # Traditional metrics vs LLM LRI
    traditional = ['human_fre', 'human_fk', 'human_ld', 'human_twr']
    llm_metrics = ['human_lri', 'human_clarity', 'human_completeness', 
                   'human_conciseness', 'human_technical', 'human_llm_friendly']
    
    for trad in traditional:
        for llm in llm_metrics:
            r, p = stats.pearsonr(df[trad], df[llm])
            correlations.append({
                'Traditional_Metric': trad,
                'LLM_Metric': llm,
                'Pearson_r': round(r, 3),
                'p_value': round(p, 3),
                'Significant': 'Yes' if p < 0.05 else 'No',
            })
    
    return pd.DataFrame(correlations)


def generate_summary_statistics(df):
    """Generate comprehensive summary statistics."""
    # Human docs summary
    human_cols = ['human_fre', 'human_fk', 'human_ld', 'human_twr', 'human_lri',
                  'human_clarity', 'human_completeness', 'human_conciseness', 
                  'human_technical', 'human_llm_friendly']
    
    # Machine docs summary
    machine_cols = ['machine_fre', 'machine_fk', 'machine_ld', 'machine_twr', 'machine_lri',
                    'machine_clarity', 'machine_completeness', 'machine_conciseness', 
                    'machine_technical', 'machine_llm_friendly']
    
    summary = []
    
    for i, (human_col, machine_col) in enumerate(zip(human_cols, machine_cols)):
        metric_name = human_col.replace('human_', '').replace('_', ' ').title()
        
        summary.append({
            'Metric': metric_name,
            'Human_Mean': round(df[human_col].mean(), 2),
            'Human_Std': round(df[human_col].std(), 2),
            'Human_Min': round(df[human_col].min(), 2),
            'Human_Max': round(df[human_col].max(), 2),
            'Machine_Mean': round(df[machine_col].mean(), 2),
            'Machine_Std': round(df[machine_col].std(), 2),
            'Machine_Min': round(df[machine_col].min(), 2),
            'Machine_Max': round(df[machine_col].max(), 2),
            'Mean_Difference': round(df[human_col].mean() - df[machine_col].mean(), 2),
        })
    
    return pd.DataFrame(summary)


def main():
    print("=" * 60)
    print("CODHES 2026 - Statistical Analysis")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading and merging data...")
    df = load_data()
    print(f"   ✓ Loaded {len(df)} platforms")
    
    # Save merged dataset
    df.to_csv(OUTPUT_DIR / "merged_dataset.csv", index=False)
    print(f"   ✓ Saved merged dataset to {OUTPUT_DIR}/merged_dataset.csv")
    
    # Calculate effect sizes
    print("\n2. Calculating Cohen's d effect sizes...")
    effect_sizes = calculate_effect_sizes(df)
    print(effect_sizes.to_string(index=False))
    effect_sizes.to_csv(OUTPUT_DIR / "effect_sizes.csv", index=False)
    print(f"   ✓ Saved to {OUTPUT_DIR}/effect_sizes.csv")
    
    # Calculate correlations
    print("\n3. Calculating Pearson correlations...")
    correlations = calculate_correlations(df)
    # Filter for significant correlations
    sig_corr = correlations[correlations['Significant'] == 'Yes']
    print(f"\n   Significant correlations (p < 0.05):")
    if len(sig_corr) > 0:
        print(sig_corr[['Traditional_Metric', 'LLM_Metric', 'Pearson_r', 'p_value']].to_string(index=False))
    else:
        print("   No significant correlations found")
    correlations.to_csv(OUTPUT_DIR / "correlations.csv", index=False)
    print(f"   ✓ Saved to {OUTPUT_DIR}/correlations.csv")
    
    # Generate summary statistics
    print("\n4. Generating summary statistics...")
    summary = generate_summary_statistics(df)
    print(summary.to_string(index=False))
    summary.to_csv(OUTPUT_DIR / "summary_statistics.csv", index=False)
    print(f"   ✓ Saved to {OUTPUT_DIR}/summary_statistics.csv")
    
    # Generate key findings report
    print("\n5. Key Findings:")
    print(f"   • Human docs FRE mean: {df['human_fre'].mean():.2f} (SD: {df['human_fre'].std():.2f})")
    print(f"   • Machine docs FRE mean: {df['machine_fre'].mean():.2f} (SD: {df['machine_fre'].std():.2f})")
    print(f"   • Human docs LRI mean: {df['human_lri'].mean():.2f} (SD: {df['human_lri'].std():.2f})")
    print(f"   • Machine docs LRI mean: {df['machine_lri'].mean():.2f} (SD: {df['machine_lri'].std():.2f})")
    
    # Count how many platforms have higher machine LRI
    higher_machine = (df['machine_lri'] > df['human_lri']).sum()
    print(f"   • Platforms where machine LRI > human LRI: {higher_machine}/10")
    
    # Paired t-test for LRI
    t_stat, p_val = stats.ttest_rel(df['human_lri'], df['machine_lri'])
    print(f"   • Paired t-test (LRI): t={t_stat:.3f}, p={p_val:.3f}")
    
    print(f"\n{'='*60}")
    print("Analysis complete! All files saved to ./results/analysis/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
