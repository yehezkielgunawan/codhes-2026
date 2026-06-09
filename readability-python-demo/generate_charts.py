"""
Chart Generation Script for CODHES 2026 Paper
Day 3 Afternoon Task: Create publication-ready charts
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuration
RESULTS_DIR = Path("./results/analysis")
FIGURES_DIR = Path("./results/figures")
FIGURES_DIR.mkdir(exist_ok=True)

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10


def load_data():
    """Load merged dataset."""
    return pd.read_csv(RESULTS_DIR / "merged_dataset.csv")


def get_display_name(url):
    """Extract clean display name from URL."""
    url_name_map = {
        'react.dev': 'React',
        'docs.github.com': 'GitHub',
        'github.com': 'GitHub',
        'supabase.com': 'Supabase',
        'vercel.com': 'Vercel',
        'stripe.com': 'Stripe',
        'docs.langchain.com': 'LangChain',
        'langchain.com': 'LangChain',
        'developers.cloudflare.com': 'Cloudflare',
        'cloudflare.com': 'Cloudflare',
        'docs.cursor.com': 'Cursor',
        'cursor.com': 'Cursor',
        'hono.dev': 'Hono',
        'fastapi.tiangolo.com': 'FastAPI',
    }
    
    for key, value in url_name_map.items():
        if key in url:
            return value
    
    # Fallback: extract first meaningful part of domain
    parts = url.replace('https://', '').replace('http://', '').split('/')[0].split('.')
    if parts[0] == 'docs' or parts[0] == 'developers':
        return parts[1].capitalize()
    return parts[0].capitalize()


def create_readability_comparison_chart(df):
    """
    Figure 1: Bar chart comparing FRE and LRI scores.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    platforms = [get_display_name(p) for p in df['platform']]
    x = np.arange(len(platforms))
    width = 0.35
    
    # FRE comparison
    ax1.bar(x - width/2, df['human_fre'], width, label='Human Docs', alpha=0.8)
    ax1.bar(x + width/2, df['machine_fre'], width, label='Machine Docs', alpha=0.8)
    ax1.set_xlabel('Platform')
    ax1.set_ylabel('Flesch Reading Ease')
    ax1.set_title('(a) Flesch Reading Ease Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(platforms, rotation=45, ha='right')
    ax1.legend()
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # LRI comparison
    ax2.bar(x - width/2, df['human_lri'], width, label='Human Docs', alpha=0.8)
    ax2.bar(x + width/2, df['machine_lri'], width, label='Machine Docs', alpha=0.8)
    ax2.set_xlabel('Platform')
    ax2.set_ylabel('LLM Readability Index (0-100)')
    ax2.set_title('(b) LLM Readability Index Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(platforms, rotation=45, ha='right')
    ax2.legend()
    ax2.set_ylim(0, 110)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure1_readability_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure1_readability_comparison.svg', bbox_inches='tight')
    print("✓ Figure 1: Readability comparison chart saved")
    plt.close()


def create_token_comparison_chart(df):
    """
    Figure 2: Bar chart comparing token-to-word ratios.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    platforms = [get_display_name(p) for p in df['platform']]
    x = np.arange(len(platforms))
    width = 0.35
    
    ax.bar(x - width/2, df['human_twr'], width, label='Human Docs', alpha=0.8)
    ax.bar(x + width/2, df['machine_twr'], width, label='Machine Docs', alpha=0.8)
    
    ax.set_xlabel('Platform')
    ax.set_ylabel('Token-to-Word Ratio')
    ax.set_title('Token-to-Word Ratio: Human vs Machine Documentation')
    ax.set_xticks(x)
    ax.set_xticklabels(platforms, rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure2_token_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure2_token_comparison.svg', bbox_inches='tight')
    print("✓ Figure 2: Token comparison chart saved")
    plt.close()


def create_fre_vs_clarity_scatter(df):
    """
    Figure 3: Scatter plot of FRE vs LLM Clarity scores.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Human docs
    ax.scatter(df['human_fre'], df['human_clarity'], 
              s=100, alpha=0.7, label='Human Docs', marker='o')
    
    # Machine docs
    ax.scatter(df['machine_fre'], df['machine_clarity'], 
              s=100, alpha=0.7, label='Machine Docs', marker='s')
    
    # Add platform labels
    for i, platform in enumerate(df['platform']):
        short_name = get_display_name(platform)
        ax.annotate(short_name, 
                   (df['human_fre'].iloc[i], df['human_clarity'].iloc[i]),
                   xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.7)
        ax.annotate(short_name, 
                   (df['machine_fre'].iloc[i], df['machine_clarity'].iloc[i]),
                   xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.7)
    
    ax.set_xlabel('Flesch Reading Ease')
    ax.set_ylabel('LLM Clarity Score (1-5)')
    ax.set_title('Flesch Reading Ease vs LLM Clarity Assessment')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure3_fre_vs_clarity.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure3_fre_vs_clarity.svg', bbox_inches='tight')
    print("✓ Figure 3: FRE vs Clarity scatter plot saved")
    plt.close()


def create_lri_difference_boxplot(df):
    """
    Figure 4: Box plot of LRI differences (machine - human).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate differences
    lri_diff = df['machine_lri'] - df['human_lri']
    
    # Create box plot
    box_data = [lri_diff]
    bp = ax.boxplot(box_data, tick_labels=['LRI Difference\n(Machine - Human)'], 
                    patch_artist=True, widths=0.5)
    
    # Color the box
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][0].set_alpha(0.7)
    
    # Add individual points
    x = np.random.normal(1, 0.04, size=len(lri_diff))
    ax.scatter(x, lri_diff, alpha=0.6, s=50, color='red', zorder=3)
    
    # Add platform labels
    for i, (diff, platform) in enumerate(zip(lri_diff, df['platform'])):
        short_name = get_display_name(platform)
        ax.annotate(short_name, (x[i], diff), 
                   xytext=(10, 0), textcoords='offset points', 
                   fontsize=8, alpha=0.7)
    
    ax.set_ylabel('LRI Difference (Machine - Human)')
    ax.set_title('Distribution of LRI Differences Across Platforms')
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='No difference')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure4_lri_difference_boxplot.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure4_lri_difference_boxplot.svg', bbox_inches='tight')
    print("✓ Figure 4: LRI difference box plot saved")
    plt.close()


def create_effect_size_chart():
    """
    Figure 5: Effect sizes visualization (bonus chart).
    """
    effect_sizes = pd.read_csv(RESULTS_DIR / "effect_sizes.csv")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Sort by absolute effect size
    effect_sizes['abs_d'] = effect_sizes['Cohen_d'].abs()
    effect_sizes = effect_sizes.sort_values('abs_d')
    
    # Colors based on effect size direction
    colors = ['red' if d < 0 else 'blue' for d in effect_sizes['Cohen_d']]
    
    # Create horizontal bar chart
    bars = ax.barh(effect_sizes['Metric'], effect_sizes['Cohen_d'], color=colors, alpha=0.7)
    
    # Add effect size labels
    for i, (bar, d) in enumerate(zip(bars, effect_sizes['Cohen_d'])):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
               f' {d:.2f}', ha='left' if width > 0 else 'right', 
               va='center', fontsize=9)
    
    ax.set_xlabel("Cohen's d (negative = machine docs higher)")
    ax.set_title('Effect Sizes: Human vs Machine Documentation')
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    ax.axvline(x=0.2, color='gray', linestyle='--', alpha=0.3, label='Small effect')
    ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5, label='Medium effect')
    ax.axvline(x=0.8, color='gray', linestyle='--', alpha=0.7, label='Large effect')
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure5_effect_sizes.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure5_effect_sizes.svg', bbox_inches='tight')
    print("✓ Figure 5: Effect sizes chart saved (bonus)")
    plt.close()


def main():
    print("=" * 60)
    print("CODHES 2026 - Chart Generation")
    print("=" * 60)
    
    df = load_data()
    print(f"\nLoaded {len(df)} platforms")
    
    print("\n1. Creating Figure 1: Readability comparison...")
    create_readability_comparison_chart(df)
    
    print("\n2. Creating Figure 2: Token comparison...")
    create_token_comparison_chart(df)
    
    print("\n3. Creating Figure 3: FRE vs Clarity scatter...")
    create_fre_vs_clarity_scatter(df)
    
    print("\n4. Creating Figure 4: LRI difference box plot...")
    create_lri_difference_boxplot(df)
    
    print("\n5. Creating Figure 5: Effect sizes (bonus)...")
    create_effect_size_chart()
    
    print(f"\n{'='*60}")
    print(f"All charts saved to {FIGURES_DIR}/")
    print("Generated files:")
    for f in sorted(FIGURES_DIR.iterdir()):
        print(f"  • {f.name}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
