# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the newly uploaded dataset with the 'unique_id' column specified as string
df_new = pd.read_excel("C:\\Users\MicrobeJ\Documents\R_projects\with_trainees\PhiCB5-AbsorptionAssay\Data\data-master_final.xlsx", dtype={"unique_id": str})

# Calculate the mean titer of the "No Cell Control" for each unique ID
no_cell_control_means_new = df_new[df_new['genotype'] == 'No Cell Control'].groupby('unique_id')['titer'].mean().reset_index()
no_cell_control_means_new.rename(columns={'titer': 'mean_titer_no_cell_control'}, inplace=True)

# Merge this information with the original DataFrame
df_merged_new = pd.merge(df_new, no_cell_control_means_new, on='unique_id', how='left')

# Perform the normalization calculations
df_merged_new['normalized_titer_direct_sub'] = df_merged_new['titer'] - df_merged_new['mean_titer_no_cell_control']
df_merged_new['normalized_titer_ratio'] = df_merged_new['titer'] / df_merged_new['mean_titer_no_cell_control']
df_merged_new['normalized_titer_zscore'] = (df_merged_new['titer'] - df_merged_new['mean_titer_no_cell_control']) / df_merged_new['mean_titer_no_cell_control'].std()

# Initialize an empty DataFrame to store statistical test results
stat_results = pd.DataFrame(columns=['Normalization_Type', 'Test_Name', 'P-Value', 'Result'])

# Function to perform normality test and variance homogeneity test
def perform_stat_tests(df, column_name, norm_type, stat_results):
    p_values = []
    
    # Perform Shapiro-Wilk Test for Normality on each genotype except 'No Cell Control'
    for genotype in df[df['genotype'] != 'No Cell Control']['genotype'].unique():
        data = df[(df['genotype'] == genotype)][column_name]
        _, p_value = stats.shapiro(data)
        p_values.append(p_value)
        stat_results = stat_results.append({'Normalization_Type': norm_type, 'Test_Name': f'Shapiro_{genotype}', 'P-Value': p_value, 'Result': 'Pass' if p_value > 0.05 else 'Fail'}, ignore_index=True)
        
    # Perform Levene's Test for Variance Homogeneity
    all_data = [df[df['genotype'] == genotype][column_name].values for genotype in df['genotype'].unique() if genotype != 'No Cell Control']
    _, p_value = stats.levene(*all_data)
    stat_results = stat_results.append({'Normalization_Type': norm_type, 'Test_Name': 'Levene', 'P-Value': p_value, 'Result': 'Pass' if p_value > 0.05 else 'Fail'}, ignore_index=True)
    
    return p_values, stat_results

# Perform tests on original titer values
p_values, stat_results = perform_stat_tests(df_merged_new, 'titer', 'Original', stat_results)

# Display first few rows of the stat_results DataFrame
stat_results.head()
