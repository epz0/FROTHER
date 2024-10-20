#%%
import math

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

#%%
# Example usage
population_size = 933  # Specify population size
margin_of_error = 5  # Desired margin of error in percentage
confidence_level = 90  # Desired confidence level (80, 85, 90, 95, 99)
proportion = 0.5  # Expected proportion of the population (default is 0.5 for maximum variability)

sample_size = calculate_sample_size(population_size, margin_of_error, confidence_level, proportion)

# %%
