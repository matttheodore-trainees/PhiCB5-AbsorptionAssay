Lets explore some statistics, data normalization testing, and significance testing and how to best approach this for an experiment I am setting up. My experiment is run in biological replicates (have their own unique id) and technical triplicate for the biological replicates. Variability bewtween biological replicates can come from both intrinsic biological variability as well as the experimental conditions on the day it was run and the researcher who ran the experiments. Technical triplicates are run on the same day and by the same individual and therefore should be equivalent to the intrinsic noise of the experiment and/or the biology. 

For each unique id in which the experiment was run a "no cell control" was also run alongside it. This serves as a control for the biological replicates in a way meaning that if for that unique ID all values were higher for the day including the control, normalization could helpo to reduce some of the noise amongst the unique ids. 

I want to explore this dataset and see what the unique id comparison variability is like for each genotype by day. Do the datapoints amongst different unique ids overlap in a way that the technical noise and biological replicate noise are the same? Or is there bigger noise between the biological replicates than is intrinsic to the technical replicates ? 



data set is data_master_final from the PhiCB5 adsorption data. 


here is text from a markdown document outlining analysis that I did. However, I was distracted when carrying out all the tests and I want to check to make sure this markdown works and that the data and conclusions seem valid and that the markdown text matches the values from teh data. IIf not I want to make sure to correct before i move to adapt it to other analysis pipelines. 

Could you run the script with the data provided and check it against the values and the logic of the conclusions ? Could you let me know if there are any discrepancies and we can talk them through ? Thanks. 



## Importing Required Libraries

```{python}

## Data Import


# Load the dataset
file_path = 'data_master.xlsx'  # Replace with your file path
data_master = pd.read_excel(file_path)
`

## Data Normalization

We normalize the titer values to the 'No Cell Control' for each date.


# Merge the "No Cell Control" data with the main data to normalize
merged_data = pd.merge(data_master, data_master[data_master['genotype'] == 'No Cell Control'][['date', 'titer']], on='date', suffixes=('', '_control'))
merged_data['normalized_titer'] = merged_data['titer'] / merged_data['titer_control']
`

## Summary Statistics


# Calculate summary statistics
summary_stats = data_master.groupby(['date', 'genotype']).agg(
    avg_titer=('titer', np.mean),
    stdev_titer=('titer', np.std),
    n=('titer', 'count')
).reset_index()
summary_stats['se_titer'] = summary_stats['stdev_titer'] / np.sqrt(summary_stats['n'])
`

## ANOVA and Tukey's Test


# Run one-way ANOVA
f_stat, p_value = f_oneway(*[data['normalized_titer'].dropna() for name, data in merged_data.groupby("genotype")])

# Run Tukey's test
mc = MultiComparison(merged_data['normalized_titer'], merged_data['genotype'])
result = mc.tukeyhsd(alpha=0.05)
`

## Plotting


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
`

```
## Overview of the Strategy 

#### Normalizing using Individual Observations 

You could normalize each individual titer value (both biological and technical replicates) by dividing it by the corresponding "No Cell Control" for the same date. Then, you can use these normalized values for statistical tests. The 
n (number of observations) in this case would be the total number of observations (biological replicates x technical replicates).

In this approach, each titer value is normalized by the corresponding "No Cell Control" value for the same date. This method uses all the available data points, treating them as independent observations.

#### Normalizing then Using Weighted Statistical Methods 

If you want to use the average of the technical replicates, you could weight your statistical tests by the inverse of the standard error squared. This would give more weight to averages that are based on a larger number of replicates and are thus more reliable. However, the
n would still be the number of biological replicates, reducing the statistical power.

In this approach, we first calculate the average titer and standard error for each genotype on each date. We then normalize these averages by the corresponding average "No Cell Control" value for the same date. This method uses averages and considers the number of biological replicates for each genotype.


```{python}
# Importing required libraries
import pandas as pd
import numpy as np
from scipy.stats import f_oneway, ttest_ind
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
import matplotlib.pyplot as plt
import seaborn as sns



```

```{python}
# Load the dataset from 'data_complete.xlsx'
file_path = 'Data/data_master.xlsx'
data_master = pd.read_excel(file_path)




```
```{python}

merged_data = pd.merge(data_master, data_master[data_master['genotype'] == 'No Cell Control'][['date', 'titer']], on='date', suffixes=('', '_control'))
merged_data['normalized_titer'] = merged_data['titer'] / merged_data['titer_control']


```

```{python}
# Calculate summary statistics
summary_stats = data_master.groupby(['date', 'genotype']).agg(
    avg_titer=('titer', np.mean),
    stdev_titer=('titer', np.std),
    n=('titer', 'count')
).reset_index()
summary_stats['se_titer'] = summary_stats['stdev_titer'] / np.sqrt(summary_stats['n'])

# Extract control data
control_data = summary_stats[summary_stats['genotype'] == 'No Cell Control'].copy()
control_data.rename(columns={'avg_titer': 'control_avg_titer', 'stdev_titer': 'control_stdev_titer', 'se_titer': 'control_se_titer'}, inplace=True)
control_data.drop(columns=['genotype', 'n'], inplace=True)

# Merge control data with original summary statistics data based on 'date'
avg_data_with_controls = pd.merge(summary_stats, control_data, on='date')

# Calculate normalized average
avg_data_with_controls['normalized_avg'] = avg_data_with_controls['avg_titer'] / avg_data_with_controls['control_avg_titer']

# Error propagation for standard deviation
avg_data_with_controls['normalized_stdev_propagation'] = avg_data_with_controls['normalized_avg'] * np.sqrt(
    (avg_data_with_controls['stdev_titer'] / avg_data_with_controls['avg_titer']) ** 2 +
    (avg_data_with_controls['control_stdev_titer'] / avg_data_with_controls['control_avg_titer']) ** 2
)

# Standard error based on propagated standard deviation
avg_data_with_controls['normalized_se_propagation'] = avg_data_with_controls['normalized_stdev_propagation'] / np.sqrt(avg_data_with_controls['n'])



```

## Performing ANOVA 

ANOVA Variables
In one-way ANOVA, you essentially have one independent variable (genotype) that you are trying to see if it affects a dependent variable (normalized average of remaining phages). The different genotypes are the "levels" of your one independent variable.

```{python}

# Importing required libraries for statistical analysis
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.regression.mixed_linear_model import MixedLM

# Performing one-way ANOVA
anova_model = ols('normalized_avg ~ C(genotype)', data=avg_data_with_controls).fit()
anova_table = anova_lm(anova_model, typ=2)

# Display the ANOVA table
anova_table

```

Here's a breakdown of the ANOVA table:

Sum of Squares (sum_sq): This represents the variation explained by the model (for the 'genotype' factor) and the unexplained variation (residual).

Degrees of Freedom (df): This indicates the number of independent pieces of information that went into the calculation of the estimates.

F-value (F): The F-statistic is a ratio of two variances (explained variance to unexplained variance). Higher values indicate a more significant effect.

p-value (PR(>F)): This is the probability that the observed F-value could occur by random chance alone. A small p-value (< 0.05) suggests that you can reject the null hypothesis (no effect).

#### Discussion:
  
  Both approaches yield significant results, implying that the choice of normalization method does not drastically change the overall conclusion that genotype affects phage adsorption. However, the method using individual observations yields a slightly lower p-value, possibly because it utilizes more data points, thereby increasing statistical power.
  
  
"In our investigation of the role of genotype in shaping the outcomes of the assay, we employed a one-way Analysis of Variance (ANOVA) to test the hypothesis that genotype significantly influences the normalized average of the measured variable. The ANOVA model revealed a highly significant effect of genotype on the assay outcomes (F(df1, df2) = F-value, p < 0.05). This compelling statistical evidence underscores the biological relevance of genotype in modulating the assay metrics and establishes a basis for further mechanistic investigations. These findings are integral for understanding the genotype-specific variations and offer a robust statistical foundation for downstream analyses."


## Post-hoc Tests for Pairwise Comparisons

Since we find a significant effect in the ANOVA, ywe will proceed with post-hoc tests to determine which specific groups (genotypes) differ from each other. Commonly used post-hoc tests include Tukey's Honest Significant Difference (HSD), Bonferroni, and others. These tests adjust for multiple comparisons to ensure that you're not getting false positives.

#### First we will look at all genotypes against the no cell control. 

To do so we will use Dunnet's test as it is specifically designed for thsi purpose of testing vs controls. 

Dunnett's test is a post-hoc test used after an ANOVA to compare each of a number of treatments with a single control. One of its primary advantages is that it controls the family-wise error rate while making multiple comparisons to a single control group.

Key Concepts:
Family-wise Error Rate: The probability of making one or more Type I errors in a set of comparisons. Dunnett's test controls this rate, usually set at α=0.05.

Comparison to Control: Unlike other post-hoc tests that compare every possible pair of means, Dunnett's test specifically compares each experimental group mean to the control group mean. This is often the comparison of interest in experimental setups.

T-statistic: The test uses a modified t-statistic, calculated similarly to the standard t-statistic but using a pooled standard error term from the ANOVA table.
  
### Dunnets test/ Tukeys test function loop

The standard approach is to perform a series of t-tests comparing each treatment group against the control group. We then adjust the p-values to account for multiple comparisons. This approach maintains the family-wise error rate (the probability of making one or more Type I errors) at or below the alpha level. Since we're interested in comparing each genotype against the "No Cell Control," this is a goof approach for significance against control as a threshold for post-hoc analysis (though we already know we will do the post-hoc due to teh data separation)


```{python}

# There is no function for dunnets test in the package so we will make the function
# Importing the correct package for Tukey's HSD, which we'll use for Dunnett's test
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Running Dunnett's test on the filtered dataset
dunnett_result_filtered = pairwise_tukeyhsd(avg_data_with_controls_filtered['normalized_avg'].dropna(), 
                                             avg_data_with_controls_filtered['genotype'].dropna(), 
                                             alpha=0.05)

# Re-run the Tukey's HSD test for both normalization approaches
mc_individual = MultiComparison(normalized_data_individual['normalized_titer'], normalized_data_individual['genotype'])
result_individual = mc_individual.tukeyhsd(alpha=0.05)

mc_averages = MultiComparison(avg_data_with_controls['normalized_avg'], avg_data_with_controls['genotype'])
result_averages = mc_averages.tukeyhsd(alpha=0.05)

# Extract the result of Tukey's test to a DataFrame for better visualization
tukey_result_individual_df = pd.DataFrame(result_individual._results_table.data[1:], columns=result_individual._results_table.data[0])
tukey_result_averages_df = pd.DataFrame(result_averages._results_table.data[1:], columns=result_averages._results_table.data[0])

tukey_result_individual_df, tukey_result_averages_df






```


### Interpretation of Tukey's HSD Post-hoc Analysis

#### Approach 1: Normalizing Individual Observations

In this approach, the following pairwise comparisons were made:

1. NA1000 vs bNY30a: Significant difference (\(p < 0.001\)).
2. NA1000 vs pilAT36C: Significant difference (\(p < 0.001\)).
3. NA1000 ▲pilA vs bNY30a: Significant difference (\(p < 0.001\)).
4. NA1000 ▲pilA vs pilAT36C: Significant difference (\(p < 0.001\)).

#### Approach 2: Using Averages and Error Propagation

In this approach, the following pairwise comparisons were made:

1. NA1000 vs pilAT36C: Significant difference (\(p = 0.0389\)).
2. NA1000 ▲pilA vs pilAT36C: Significant difference (\(p = 0.0335\)).
3. No Cell Control vs bNY30a: Significant difference (\(p = 0.0024\)).
4. No Cell Control vs pilAT36C: Significant difference (\(p = 0.0010\)).

### Summary

In both approaches, we observed significant differences between genotypes in relation to phage adsorption. The "pilAT36C" genotype stands out for showing a significant difference from the control and other genotypes in both statistical approaches. The "bNY30a" genotype also showed significant differences when individual observations were normalized. 








## Plotting

```{python}

# Re-plotting the barplot with stripplot for individual data points
# Increasing the figure size for better visibility
# Adding asterisks for significant differences based on Tukey's test

import matplotlib.pyplot as plt
import seaborn as sns

# Set figure size
plt.figure(figsize=(12, 8))

# Create the barplot
barplot = sns.barplot(x='genotype', y='normalized_avg', data=avg_data_with_controls, ci=None, color='gray', capsize=.2)

# Add individual data points as a stripplot on top of the barplot
stripplot = sns.stripplot(x='genotype', y='normalized_titer', data=normalized_data_individual, color="black", jitter=True, dodge=True)

# Add error bars
barplot.errorbar(x=avg_data_with_controls['genotype'], 
                 y=avg_data_with_controls['normalized_avg'], 
                 yerr=avg_data_with_controls['normalized_se_propagation'], 
                 fmt='none', c='black', capsize=5)

# Add asterisks for significance levels above the bars
# for bNY30a and pilAT36C when compared to "No Cell Control"
for i, genotype in enumerate(avg_data_with_controls['genotype'].unique()):
    if genotype == 'bNY30a':
        plt.text(i, avg_data_with_controls[avg_data_with_controls['genotype'] == 'bNY30a']['normalized_avg'].max() + 0.02, '*', ha='center')
    elif genotype == 'pilAT36C':
        plt.text(i, avg_data_with_controls[avg_data_with_controls['genotype'] == 'pilAT36C']['normalized_avg'].max() + 0.02, '*', ha='center')

# Adjusting axis labels and title
plt.xlabel('Genotype')
plt.ylabel('Normalized Average Titer')
plt.title('Normalized Phage Adsorption by Genotype')

# Show the plot
plt.show()








```