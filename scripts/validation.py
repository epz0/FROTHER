#%%
import math
import random
import pandas as pd

#%%
def calculate_sample_size(pop, err, cl, prop=0.5):
    # Convert margin of error into decimal
    err /= 100
    
    # Z-score corresponding to the confidence level
    z_scores = {
        80: 1.28,
        85: 1.44,
        90: 1.645,
        95: 1.96,
        99: 2.576
    }

    # Get the Z-score based on the confidence level
    z = z_scores.get(cl, 1.96)  # Default to 95%

    # Calculate sample size without population adjustment
    sample_size = (z ** 2 * prop * (1 - prop)) / (err ** 2)

    # Adjust sample size for finite population
    finite_population_correction = sample_size / (1 + (sample_size - 1) / pop)

    return math.ceil(finite_population_correction)

population_size = 933  # Specify population size
margin_of_error = 5  # Desired margin of error in percentage
confidence_level = 90  # Desired confidence level (80, 85, 90, 95, 99)
proportion = 0.5  # Expected proportion of the population

sample_size = calculate_sample_size(population_size, margin_of_error, confidence_level, proportion)

# %% random list of ids for validation
random.seed(42) #set the seed

# Generate list of 210 unique random numbers (these will be indexes in the exported xlsx file)
random_numbers = random.sample(range(933), 210)
#! random_numbers were used to create de validation file

#%%
# reading validation file
f_path = '../validation.xlsx'

df_vdesc = pd.read_excel(f_path,sheet_name='val_description')   # description
df_vsumry = pd.read_excel(f_path,sheet_name='val_summary')       # summary

s_size = len(df_vdesc)

def calc_margin_error(sample_error, sample_size, cl):
    # Z-scores corresponding to confidence levels
    z_scores = {
        80: 1.28,
        85: 1.44,
        90: 1.645,
        95: 1.96,
        99: 2.576
    }
    
    # Get the Z-score for the chosen confidence level
    z = z_scores.get(cl, 1.645)  # 90% confidence level Z-score
    
    # Calculate the margin of error
    margin_of_error = z * math.sqrt((sample_error * (1 - sample_error)) / sample_size)
    
    return margin_of_error

# from validation spreadsheet
# count n=0 in column DescVal
err_desc_abs = df_vdesc['DescVal'].value_counts().get(0, 0)
print(err_desc_abs)

# count n=0 (2) in DescVal & Obs does not contain "Minor mistake"
err_desc_minormist = df_vdesc[(df_vdesc['DescVal'] == 0) & (~df_vdesc['Obs'].str.contains("Minor mistake"))].shape[0]
print(err_desc_minormist)

err_sumry_abs = df_vsumry['SumVal'].value_counts().get(0, 0)
print(err_sumry_abs)

sample_error_abs_desc = (err_desc_abs/s_size) #description absolute
sample_error_minor_desc = (err_desc_minormist/s_size) #description disconsidering minor mistakes
sample_error_abs_summ = (err_sumry_abs/s_size) #summary disconsidering minor mistakes)

sample_errors = [sample_error_abs_desc,sample_error_minor_desc,sample_error_abs_summ]

sample_size = 210  # Sample size of 210
cl = 90            # 90% confidence level

moe =[]
l_bound =[]
u_bound =[]

# Calculate margin of error
for i in range(len(sample_errors)):
    moe.append(calc_margin_error(sample_errors[i], sample_size, cl))

    l_bound.append((sample_errors[i]-moe[i])*100)
    u_bound.append((sample_errors[i]+moe[i])*100)

# %%
