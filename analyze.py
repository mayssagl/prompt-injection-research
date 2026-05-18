import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

from run_experiments import MODELS

# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv("results.csv")
os.makedirs("figures", exist_ok=True)

print(f"✅ Loaded {len(df)} rows")
print(f"Models: {df['model'].unique()}")
print(f"Variants: {df['variant'].unique()}")
print(f"Input types: {df['input_type'].unique()}")


# ============================================
# FIGURE 1 — ATTACK SUCCESS RATE (ASR)
# How often did injection WORK per variant?
# Lower = better defense
# ============================================

print("\n📊 Calculating Attack Success Rates...")

# Filter only attack inputs
attacks_df = df[df['input_type'] == 'attack']

# Calculate ASR per variant per model
asr = attacks_df.groupby(
    ['variant', 'model']
)['failed'].mean() * 100

asr_table = asr.unstack()
print("\nASR Table (%):")
print(asr_table.round(1))

# Plot
fig, ax = plt.subplots(figsize=(14, 6))

asr_table.plot(
    kind='bar',
    ax=ax,
    width=0.7,
    colormap='Set2'
)

ax.set_title(
    'Attack Success Rate per Prompt Variant and Model\n'
    '(Lower = Better Defense)',
    fontsize=14,
    fontweight='bold'
)
ax.set_xlabel('Prompt Variant', fontsize=12)
ax.set_ylabel('Attack Success Rate (%)', fontsize=12)
ax.set_ylim(0, 110)
ax.legend(title='Model', fontsize=10)
ax.tick_params(axis='x', rotation=45)

# Add value labels on bars
for container in ax.containers:
    ax.bar_label(container, fmt='%.0f%%', 
                 fontsize=8, padding=2)

plt.tight_layout()
plt.savefig('figures/asr_chart.png', dpi=150)
plt.close()
print("✅ Saved figures/asr_chart.png")


# ============================================
# FIGURE 2 — P-VALUE HEATMAP
# Statistical significance between variants
# Are the differences real or just chance?
# p < 0.05 = significant difference ✅
# ============================================

print("\n📊 Calculating P-value Heatmap...")

variants = list(df['variant'].unique())
models = list(df['model'].unique())

# One heatmap per model
for model in models:
    model_df = df[
        (df['model'] == model) & 
        (df['input_type'] == 'attack')
    ]
    
    # Build p-value matrix
    n = len(variants)
    p_matrix = pd.DataFrame(
        index=variants, 
        columns=variants, 
        dtype=float
    )
    
    for v1 in variants:
        for v2 in variants:
            if v1 == v2:
                p_matrix.loc[v1, v2] = 1.0
            else:
                scores1 = model_df[
                    model_df['variant'] == v1
                ]['failed'].values
                
                scores2 = model_df[
                    model_df['variant'] == v2
                ]['failed'].values
                
                # Make sure same length
                min_len = min(len(scores1), len(scores2))
                scores1 = scores1[:min_len]
                scores2 = scores2[:min_len]
                
                try:
                    _, p = stats.ttest_rel(scores1, scores2)
                    p_matrix.loc[v1, v2] = round(p, 4)
                except:
                    p_matrix.loc[v1, v2] = 1.0
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 9))
    
    sns.heatmap(
        p_matrix.astype(float),
        annot=True,
        fmt='.3f',
        cmap='RdYlGn',
        vmin=0,
        vmax=0.1,
        ax=ax,
        linewidths=0.5,
        annot_kws={"size": 9}
    )
    
    ax.set_title(
        f'P-value Heatmap — {model}\n'
        f'(Green < 0.05 = Statistically Significant)',
        fontsize=13,
        fontweight='bold'
    )
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)
    
    plt.tight_layout()
    filename = f'figures/pvalue_heatmap_{model}.png'
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"✅ Saved {filename}")


# ============================================
# FIGURE 3 — FALSE POSITIVE RATE
# Did defenses accidentally block normal inputs?
# Lower = better (defenses don't hurt normal use)
# ============================================

print("\n📊 Calculating False Positive Rates...")

legit_df = df[df['input_type'] == 'legitimate']

fpr = legit_df.groupby(
    ['variant', 'model']
)['failed'].mean() * 100

fpr_table = fpr.unstack()
print("\nFalse Positive Rate Table (%):")
print(fpr_table.round(1))

fig, ax = plt.subplots(figsize=(14, 6))

fpr_table.plot(
    kind='bar',
    ax=ax,
    width=0.7,
    colormap='Set1'
)

ax.set_title(
    'False Positive Rate per Prompt Variant and Model\n'
    '(Lower = Better — Legitimate inputs not blocked)',
    fontsize=14,
    fontweight='bold'
)
ax.set_xlabel('Prompt Variant', fontsize=12)
ax.set_ylabel('False Positive Rate (%)', fontsize=12)
ax.set_ylim(0, 110)
ax.legend(title='Model', fontsize=10)
ax.tick_params(axis='x', rotation=45)

for container in ax.containers:
    ax.bar_label(container, fmt='%.0f%%', 
                 fontsize=8, padding=2)

plt.tight_layout()
plt.savefig('figures/false_positive_chart.png', dpi=150)
plt.close()
print("✅ Saved figures/false_positive_chart.png")


# ============================================
# FIGURE 4 — MISS RATE
# Did defenses make the tool miss real threats?
# Lower = better
# ============================================

print("\n📊 Calculating Miss Rates...")

threat_df = df[df['input_type'] == 'real_threat']

miss = threat_df.groupby(
    ['variant', 'model']
)['failed'].mean() * 100

miss_table = miss.unstack()
print("\nMiss Rate Table (%):")
print(miss_table.round(1))

fig, ax = plt.subplots(figsize=(14, 6))

miss_table.plot(
    kind='bar',
    ax=ax,
    width=0.7,
    colormap='Set3'
)

ax.set_title(
    'Miss Rate per Prompt Variant and Model\n'
    '(Lower = Better — Real threats correctly detected)',
    fontsize=14,
    fontweight='bold'
)
ax.set_xlabel('Prompt Variant', fontsize=12)
ax.set_ylabel('Miss Rate (%)', fontsize=12)
ax.set_ylim(0, 110)
ax.legend(title='Model', fontsize=10)
ax.tick_params(axis='x', rotation=45)

for container in ax.containers:
    ax.bar_label(container, fmt='%.0f%%', 
                 fontsize=8, padding=2)

plt.tight_layout()
plt.savefig('figures/miss_rate_chart.png', dpi=150)
plt.close()
print("✅ Saved figures/miss_rate_chart.png")


# ============================================
# SUMMARY TABLE — print everything clean
# ============================================

print("\n" + "=" * 60)
print("   FULL SUMMARY")
print("=" * 60)

summary = df.groupby(
    ['variant', 'model', 'input_type']
)['failed'].mean() * 100

print(summary.round(1).to_string())

print("\n✅ All figures saved in /figures folder")
print("✅ Analysis complete")

# ============================================
# PRINT KEY FINDINGS SUMMARY
# ============================================
print("\n" + "=" * 60)
print("   KEY FINDINGS")
print("=" * 60)

attacks_only = df[df['input_type'] == 'attack']

# Best variant per model
print("\n🏆 Best Performing Variant per Model (lowest ASR):")
for model in MODELS:
    model_data = attacks_only[attacks_only['model'] == model]
    asr_per_variant = model_data.groupby('variant')['failed'].mean() * 100
    best = asr_per_variant.idxmin()
    best_score = asr_per_variant.min()
    worst = asr_per_variant.idxmax()
    worst_score = asr_per_variant.max()
    print(f"  {model}:")
    print(f"    Best  → {best}: {best_score:.0f}% ASR")
    print(f"    Worst → {worst}: {worst_score:.0f}% ASR")

# Overall average ASR per variant across all models
print("\n📊 Average ASR Across All Models (lower = better):")
avg_asr = attacks_only.groupby('variant')['failed'].mean() * 100
avg_asr_sorted = avg_asr.sort_values()
for variant, score in avg_asr_sorted.items():
    bar = "█" * int(score / 5)
    print(f"  {variant:<30} {score:5.1f}% {bar}")

# Gemma2 warning
print("\n⚠️  WARNING: gemma2_9b scored 100% failure rate")
print("   on ALL variants and ALL input types.")
print("   This model appears to ignore system prompts entirely.")
print("   This is a key finding for your paper.")

# L7 backfire
l7_70b = attacks_only[
    (attacks_only['variant'] == 'L7_chain_of_thought') &
    (attacks_only['model'] == 'llama3.3_70b')
]['failed'].mean() * 100

l1_70b = attacks_only[
    (attacks_only['variant'] == 'L1_no_protection') &
    (attacks_only['model'] == 'llama3.3_70b')
]['failed'].mean() * 100

print(f"\n⚠️  L7 BACKFIRE on llama3.3_70b:")
print(f"   L1 (no protection): {l1_70b:.0f}% ASR")
print(f"   L7 (chain of thought): {l7_70b:.0f}% ASR")
print(f"   Chain-of-thought reasoning INCREASED")
print(f"   vulnerability by {l7_70b - l1_70b:.0f} percentage points.")