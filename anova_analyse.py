# %%
import pandas as pd
import scipy.stats as stats

# Load the combined data for an experiment
def load_combined_data(expnum):
    combined_file = f"Experiment-Data/ANOVA2/Combined_Stim_Duration_Exp{expnum}.csv"
    df = pd.read_csv(combined_file)
    return df

# Perform One-Way ANOVA
def perform_anova(df):
    # Separate the data by category
    self_control_group = df[df['category'] == 'self-control']['stim_duration']
    non_self_control_group = df[df['category'] == 'non-self-control']['stim_duration']
    
    # Perform ANOVA
    f_statistic, p_value = stats.f_oneway(self_control_group, non_self_control_group)
    
    return f_statistic, p_value

# Report Descriptive Statistics
def report_statistics(df):
    # Descriptive statistics for self-control group
    self_control_group = df[df['category'] == 'self-control']['stim_duration']
    non_self_control_group = df[df['category'] == 'non-self-control']['stim_duration']
    
    # Calculate means and standard deviations
    self_control_mean = self_control_group.mean()
    self_control_std = self_control_group.std()
    non_self_control_mean = non_self_control_group.mean()
    non_self_control_std = non_self_control_group.std()
    
    # Report statistics
    print("Descriptive Statistics:")
    print(f"Self-Control Group: Mean = {self_control_mean:.3f}, Std = {self_control_std:.3f}")
    print(f"Non-Self-Control Group: Mean = {non_self_control_mean:.3f}, Std = {non_self_control_std:.3f}")
    
    # Perform ANOVA
    f_statistic, p_value = perform_anova(df)
    print("\nANOVA Results:")
    print(f"F-statistic = {f_statistic:.3f}, p-value = {p_value:.3f}")
    
    # Interpret the p-value
    if p_value < 0.05:
        print("The result is statistically significant (p < 0.05).")
    else:
        print("The result is not statistically significant (p >= 0.05).")

# For each experiment (exp1 to exp4), perform ANOVA and report the statistics
for expnum in range(1, 5):
    df = load_combined_data(expnum)
    print(f"\nExperiment {expnum}:")
    report_statistics(df)
    print("="*50)

# %%
