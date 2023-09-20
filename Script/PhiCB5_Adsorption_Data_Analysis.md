# Data Analysis for PhiCB5 Adsorption Data

## Introduction

The experiment is run in biological replicates (have their own unique id) and technical triplicate for the biological replicates. 
The data set is `data_master_final` from the PhiCB5 adsorption data. This document outlines the statistical tests carried out on the dataset.

## Data Preparation

The dataset was loaded and the 'unique_id' column was specified as a string to prevent it from being parsed as a date.

\```python
# Load the newly uploaded dataset with the 'unique_id' column specified as string
df_new = pd.read_excel("Data/data_master_final.xlsx", dtype={"unique_id": str})
\```

## Normalization

Three types of normalization were performed:

1. Direct Subtraction
2. Ratio Normalization
3. Z-Score Normalization

\```python
# Direct Subtraction
df_merged_new['normalized_titer_direct_sub'] = df_merged_new['titer'] - df_merged_new['mean_titer_no_cell_control']

# Ratio Normalization
df_merged_new['normalized_titer_ratio'] = df_merged_new['titer'] / df_merged_new['mean_titer_no_cell_control']

# Z-Score Normalization
df_merged_new['normalized_titer_zscore'] = (df_merged_new['titer'] - df_merged_new['mean_titer_no_cell_control']) / df_merged_new['mean_titer_no_cell_control'].std()
\```

## Preliminary Statistical Tests

### Shapiro-Wilk Test for Normality and Levene's Test for Homogeneity of Variances

The Shapiro-Wilk test is used to check if each genotype's data is normally distributed, and Levene's test is used to check if the variances across the genotypes are homogeneous.

\```plaintext
     Normalization_Type             Test_Name   P-Value Result
0              Original        Shapiro_NA1000  0.458709   Pass
1              Original  Shapiro_NA1000 ▲pilA  0.110242   Pass
2              Original        Shapiro_bNY30a  0.125683   Pass
3              Original      Shapiro_pilAT36C  0.745261   Pass
4              Original                Levene  0.402243   Pass
5    Direct_Subtraction        Shapiro_NA1000  0.114235   Pass
6    Direct_Subtraction  Shapiro_NA1000 ▲pilA  0.249646   Pass
7    Direct_Subtraction        Shapiro_bNY30a  0.171544   Pass
8    Direct_Subtraction      Shapiro_pilAT36C  0.872297   Pass
9    Direct_Subtraction                Levene  0.182243   Pass
10  Ratio_Normalization        Shapiro_NA1000  0.189448   Pass
11  Ratio_Normalization  Shapiro_NA1000 ▲pilA  0.172546   Pass
12  Ratio_Normalization        Shapiro_bNY30a  0.101303   Pass
13  Ratio_Normalization      Shapiro_pilAT36C  0.795403   Pass
14  Ratio_Normalization                Levene  0.186566   Pass
\```

Given that the data meet these assumptions, further statistical tests like the ANOVA or t-tests to compare the means between different genotypes can be performed.

