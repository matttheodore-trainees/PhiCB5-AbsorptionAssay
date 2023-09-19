# Phage Adsorption Assay Analysis

This document outlines the steps to analyze a bacteriophage adsorption assay. We'll use Python for data manipulation, statistical testing, and plotting. The analysis includes:

- Data Import
- Data Normalization
- Summary Statistics
- ANOVA and Tukey's Test
- Plotting

## Importing Required Libraries

\`\`\`python
import pandas as pd
import numpy as np
from scipy.stats import f_oneway, ttest_ind
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
import matplotlib.pyplot as plt
import seaborn as sns
\`\`\`

## Data Import

\`\`\`python
# Load the dataset
file_path = 'data_master.xlsx'  # Replace with your file path
data_master = pd.read_excel(file_path)
\`\`\`

## Data Normalization

We normalize the titer values to the 'No Cell Control' for each date.

\`\`\`python
# Merge the "No Cell Control" data with the main data to normalize
merged_data = pd.merge(data_master, data_master[data_master['genotype'] == 'No Cell Control'][['date', 'titer']], on='date', suffixes=('', '_control'))
merged_data['normalized_titer'] = merged_data['titer'] / merged_data['titer_control']
\`\`\`

## Summary Statistics

\`\`\`python
# Calculate summary statistics
summary_stats = data_master.groupby(['date', 'genotype']).agg(
    avg_titer=('titer', np.mean),
    stdev_titer=('titer', np.std),
    n=('titer', 'count')
).reset_index()
summary_stats['se_titer'] = summary_stats['stdev_titer'] / np.sqrt(summary_stats['n'])
\`\`\`

## ANOVA and Tukey's Test

\`\`\`python
# Run one-way ANOVA
f_stat, p_value = f_oneway(*[data['normalized_titer'].dropna() for name, data in merged_data.groupby("genotype")])

# Run Tukey's test
mc = MultiComparison(merged_data['normalized_titer'], merged_data['genotype'])
result = mc.tukeyhsd(alpha=0.05)
\`\`\`

## Plotting

\`\`\`python
# Create a barplot
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
sns.barplot(x='genotype', y='normalized_titer', data=merged_data, ci='sd', capsize=.2, palette='muted')
sns.swarmplot(x='genotype', y='normalized_titer', data=merged_data, color='black')
plt.title('Normalized Titers by Genotype')
plt.ylabel('Normalized Titer')
plt.xlabel('Genotype')

# Add asterisks for significance above the bars
# (Replace 'some_value' with the actual value where you want to place the asterisks)
plt.text(1, some_value, '*', ha='center')
plt.text(2, some_value, '**', ha='center')

plt.show()
\`\`\`

