# Titer Data Analysis

## Importing Libraries

\`\`\`python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
\`\`\`

## Loading and Preparing Data

\`\`\`python
# Load the data from Excel file
df = pd.read_excel("data_master_final.xlsx", dtype={"unique_id": str})

# Calculate the mean titer of the "No Cell Control" for each unique ID
no_cell_control_means = df[df['genotype'] == 'No Cell Control'].groupby('unique_id')['titer'].mean().reset_index()
no_cell_control_means.rename(columns={'titer': 'mean_titer_no_cell_control'}, inplace=True)

# Merge this information with the original DataFrame
df_merged = pd.merge(df, no_cell_control_means, on='unique_id', how='left')
\`\`\`

## Normalization Methods

### Direct Subtraction

\`\`\`python
df_merged['normalized_titer_direct_sub'] = df_merged['titer'] - df_merged['mean_titer_no_cell_control']
\`\`\`

### Ratio Normalization

\`\`\`python
df_merged['normalized_titer_ratio'] = df_merged['titer'] / df_merged['mean_titer_no_cell_control']
\`\`\`

### Z-Score Normalization

\`\`\`python
df_merged['normalized_titer_zscore'] = (df_merged['titer'] - df_merged['mean_titer_no_cell_control']) / df_merged['mean_titer_no_cell_control'].std()
\`\`\`

## Data Visualization

\`\`\`python
# (Insert the plotting code here)
\`\`\`

## Preliminary Statistical Tests

### Shapiro-Wilk Test for Normality

\`\`\`python
# (Insert the Shapiro-Wilk test code here)
\`\`\`

### Levene's Test for Homogeneity of Variances

\`\`\`python
# (Insert the Levene's test code here)
\`\`\`

## One-Way ANOVA and Tukey's HSD

\`\`\`python
# (Insert the ANOVA and Tukey's HSD code here)
\`\`\`

DataFrame
shapiro_results_incl_control = pd.DataFrame(shapiro_results_list)

# Conduct Levene's test for all normalization methods
levene_test_results = []
for col in ['titer', 'normalized_titer_direct_sub', 'normalized_titer_ratio', 'normalized_titer_zscore']:
    levene_stat, levene_p = levene(*[df_merged_new[df_merged_new['genotype'] == genotype][col] for genotype in df_merged_new['genotype'].unique()])
    levene_test_results.append({'Normalization_Type': col, 'Test_Name': 'Levene', 'P-Value': levene_p})

# Convert the list of dictionaries to a DataFrame
levene_test_df = pd.DataFrame(levene_test_results)

# Display Shapiro and Levene test results
shapiro_results_incl_control, levene_test_df
```

## One-Way ANOVA and Tukey's HSD Test

```python
# One-way ANOVA on original data and all three normalization methods
anova_test_results = []
for col in ['titer', 'normalized_titer_direct_sub', 'normalized_titer_ratio', 'normalized_titer_zscore']:
    f_stat, p_value = f_oneway(*[df_merged_new[df_merged_new['genotype'] == genotype][col].dropna() for genotype in df_merged_new['genotype'].unique()])
    anova_test_results.append({'Normalization_Type': col, 'F-Statistic': f_stat, 'P-Value': p_value})

# Convert the list of dictionaries to a DataFrame
anova_test_df = pd.DataFrame(anova_test_results)

# Tukey's HSD Test on original data and all three normalization methods
tukey_test_results = []
for col in ['titer', 'normalized_titer_direct_sub', 'normalized_titer_ratio', 'normalized_titer_zscore']:
    tukey_result = pairwise_tukeyhsd(df_merged_new[col].dropna(), df_merged_new['genotype'])
    tukey_test_results.append({'Normalization_Type': col, 'Tukey_HSD_Result': tukey_result})

# Convert the list of dictionaries to a DataFrame
tukey_test_df = pd.DataFrame(tukey_test_results)

# Display One-Way ANOVA and Tukey's HSD test results
anova_test_df, tukey_test_df
```

## Conclusion

This completes the script for the full analysis, including data loading, manipulation, normalization, visualization, and statistical testing. Each section should be executed in sequence.
