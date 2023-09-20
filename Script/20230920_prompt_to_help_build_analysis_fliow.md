Lets explore some statistics, data normalization testing, and significance testing and how to best approach this for an experiment I am setting up. My experiment is run in biological replicates (have their own unique id) and technical triplicate for the biological replicates. Variability bewtween biological replicates can come from both intrinsic biological variability as well as the experimental conditions on the day it was run and the researcher who ran the experiments. Technical triplicates are run on the same day and by the same individual and therefore should be equivalent to the intrinsic noise of the experiment and/or the biology. 

For each unique id in which the experiment was run a "no cell control" was also run alongside it. This serves as a control for the biological replicates in a way meaning that if for that unique ID all values were higher for the day including the control, normalization could helpo to reduce some of the noise amongst the unique ids. 

I want to explore this dataset and see what the unique id comparison variability is like for each genotype by day. Do the datapoints amongst different unique ids overlap in a way that the technical noise and biological replicate noise are the same? Or is there bigger noise between the biological replicates than is intrinsic to the technical replicates ? 



data set is data_master_final from the PhiCB5 adsorption data. 


here is text from a markdown document outlining analysis that I did. However, I was distracted when carrying out all the tests and I want to check to make sure this markdown works and that the data and conclusions seem valid and that the markdown text matches the values from teh data. IIf not I want to make sure to correct before i move to adapt it to other analysis pipelines. 

Could you run the script with the data provided and check it against the values and the logic of the conclusions ? Could you let me know if there are any discrepancies and we can talk them through ? Thanks. 



## Importing Required Libraries

# Load the newly uploaded dataset
df_new = pd.read_excel("/mnt/data/data_master_final.xlsx")

# Calculate the mean titer of the "No Cell Control" for each unique ID
no_cell_control_means_new = df_new[df_new['genotype'] == 'No Cell Control'].groupby('unique_id')['titer'].mean().reset_index()
no_cell_control_means_new.rename(columns={'titer': 'mean_titer_no_cell_control'}, inplace=True)

# Merge this information with the original DataFrame
df_merged_new = pd.merge(df_new, no_cell_control_means_new, on='unique_id', how='left')

# Perform the normalization calculations

# Direct Subtraction
df_merged_new['normalized_titer_direct_sub'] = df_merged_new['titer'] - df_merged_new['mean_titer_no_cell_control']

# Ratio Normalization
df_merged_new['normalized_titer_ratio'] = df_merged_new['titer'] / df_merged_new['mean_titer_no_cell_control']

# Z-Score Normalization
df_merged_new['normalized_titer_zscore'] = (df_merged_new['titer'] - df_merged_new['mean_titer_no_cell_control']) / df_merged_new['mean_titer_no_cell_control'].std()

# Initialize the figure
fig, axes = plt.subplots(1, 3, figsize=(20, 8))

# Direct Subtraction Normalization
sns.violinplot(x='genotype', y='normalized_titer_direct_sub', data=df_merged_new, ax=axes[0], inner=None, color='lightgray')
sns.stripplot(x='genotype', y='normalized_titer_direct_sub', data=df_merged_new, hue='unique_id', dodge=True, marker='o', alpha=0.7, jitter=True, ax=axes[0])
axes[0].set_title('Direct Subtraction Normalization')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')
axes[0].legend(title='Unique ID', bbox_to_anchor=(1.05, 1), loc='upper left')

# Ratio Normalization
sns.violinplot(x='genotype', y='normalized_titer_ratio', data=df_merged_new, ax=axes[1], inner=None, color='lightgray')
sns.stripplot(x='genotype', y='normalized_titer_ratio', data=df_merged_new, hue='unique_id', dodge=True, marker='o', alpha=0.7, jitter=True, ax=axes[1])
axes[1].set_title('Ratio Normalization')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
axes[1].legend(title='Unique ID', bbox_to_anchor=(1.05, 1), loc='upper left')

# Z-Score Normalization
sns.violinplot(x='genotype', y='normalized_titer_zscore', data=df_merged_new, ax=axes[2], inner=None, color='lightgray')
sns.stripplot(x='genotype', y='normalized_titer_zscore', data=df_merged_new, hue='unique_id', dodge=True, marker='o', alpha=0.7, jitter=True, ax=axes[2])
axes[2].set_title('Z-Score Normalization')
axes[2].set_xticklabels(axes[2].get_xticklabels(), rotation=45, ha='right')
axes[2].legend(title='Unique ID', bbox_to_anchor=(1.05, 1), loc='upper left')

# Finalize the layout
plt.tight_layout()
plt.show()



