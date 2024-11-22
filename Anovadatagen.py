# %%
import os
import pandas as pd
import numpy as np
import ast

# Assuming response_time function is defined as provided
def response_time(dff, expnum=1):
    extracted_data = dff[['stim_duration', 'stim', 'coded_response', 'exp_stage', 'trial_num', 'stim_rating']]
    extracted_data = extracted_data.dropna(subset=['trial_num', 'stim_rating'])
    extracted_data[['taste', 'health']] = extracted_data['stim_rating'].apply(lambda x: pd.Series(ast.literal_eval(x)))
    extracted_data.replace("NaN", np.nan, inplace=True, regex=False)
    extracted_data['taste'] = extracted_data['taste'].fillna(1)  # Replace NaN in taste with 1
    extracted_data['health'] = extracted_data['health'].fillna(-1)
    extracted_data['taste'] = extracted_data['taste'].astype(int)
    extracted_data['health'] = extracted_data['health'].astype(int)
    extracted_data['taste'] = extracted_data['taste'].apply(lambda x: np.random.choice([-1, 1]) if x == 0 else x)
    extracted_data['health'] = extracted_data['health'].apply(lambda x: np.random.choice([-1, 1]) if x == 0 else x)

    if expnum == 1:
        filtered_df = extracted_data[(extracted_data['taste'] < 0) & (extracted_data['health'] < 0)]
        return filtered_df['stim_duration']
    elif expnum == 2:
        filtered_df = extracted_data[(extracted_data['taste'] < 0) & (extracted_data['health'] > 0)]
        return filtered_df['stim_duration']
    elif expnum == 3:
        filtered_df = extracted_data[(extracted_data['taste'] > 0) & (extracted_data['health'] < 0)]
        return filtered_df['stim_duration']
    elif expnum == 4:
        filtered_df = extracted_data[(extracted_data['taste'] > 0) & (extracted_data['health'] > 0)]
        return filtered_df['stim_duration']

# Define directories
base_dir = "Experiment-Data"
non_self_controlled_dir = os.path.join(base_dir, "Non-Self-Controlled")
self_controlled_dir = os.path.join(base_dir, "Self-Controlled")
anova_dir = os.path.join(base_dir, "ANOVA")

# Create ANOVA directory if it doesn't exist
os.makedirs(anova_dir, exist_ok=True)

# Helper function to load stim_duration for all CSVs in a directory
def load_stim_duration(directory, expnum=1):
    stim_durations = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):  # Check if the file is a CSV
            file_path = os.path.join(directory, file_name)
            df = pd.read_csv(file_path)  # Load CSV into DataFrame
            stim_duration = response_time(df, expnum=expnum)  # Get stim_duration using response_time
            stim_durations.append(stim_duration)
    return pd.concat(stim_durations, ignore_index=True)  # Combine all stim_duration into one Series

# Function to save stim_duration DataFrame for each expnum
def save_stim_duration(expnum):
    non_self_controlled_stim_duration = load_stim_duration(non_self_controlled_dir, expnum=expnum)
    self_controlled_stim_duration = load_stim_duration(self_controlled_dir, expnum=expnum)

    # Create DataFrames
    non_self_controlled_df = pd.DataFrame(non_self_controlled_stim_duration, columns=['stim_duration'])
    self_controlled_df = pd.DataFrame(self_controlled_stim_duration, columns=['stim_duration'])

    # Define file names
    non_self_controlled_file = os.path.join(anova_dir, f"Non_Self_Controlled_Stim_Duration_Exp{expnum}.csv")
    self_controlled_file = os.path.join(anova_dir, f"Self_Controlled_Stim_Duration_Exp{expnum}.csv")

    # Save CSVs
    non_self_controlled_df.to_csv(non_self_controlled_file, index=False)
    self_controlled_df.to_csv(self_controlled_file, index=False)

    print(f"Exp {expnum}: DataFrames saved to ANOVA directory.")

# Save stim_duration for all expnums (1 to 4)
for expnum in range(1, 5):
    save_stim_duration(expnum)

# %%
