# %%
import os
import pandas as pd
import numpy as np
import ast

# Assuming response_time function is defined as provided
np.random.seed(42)

def response_time(dff):
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
    
    # Filters based on taste and health conditions
    filter1 = (extracted_data['taste'] < 0) & (extracted_data['health'] < 0)
    filter2 = (extracted_data['taste'] < 0) & (extracted_data['health'] > 0)
    filter3 = (extracted_data['taste'] > 0) & (extracted_data['health'] < 0)
    filter4 = (extracted_data['taste'] > 0) & (extracted_data['health'] > 0)

    # Return stim_duration for each filter
    return [
        extracted_data[filter1]['stim_duration'],
        extracted_data[filter2]['stim_duration'],
        extracted_data[filter3]['stim_duration'],
        extracted_data[filter4]['stim_duration']
    ]

# Define directories
base_dir = "Experiment-Data"
non_self_controlled_dir = os.path.join(base_dir, "Non-Self-Controlled")
self_controlled_dir = os.path.join(base_dir, "Self-Controlled")
anova_dir = os.path.join(base_dir, "ANOVA2")

# Create ANOVA directory if it doesn't exist
os.makedirs(anova_dir, exist_ok=True)

# Helper function to load stim_duration for all CSVs in a directory and return all results for all experiments
def load_all_stim_durations(directory):
    all_stim_durations = {
        'filter1': [],
        'filter2': [],
        'filter3': [],
        'filter4': []
    }
    
    # Loop through all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            df = pd.read_csv(file_path)
            filter_results = response_time(df)  # Get the stim_duration values based on the filters
            
            # Append stim_duration for each filter to the corresponding list
            all_stim_durations['filter1'].append(filter_results[0])
            all_stim_durations['filter2'].append(filter_results[1])
            all_stim_durations['filter3'].append(filter_results[2])
            all_stim_durations['filter4'].append(filter_results[3])
    
    # Combine all stim_duration lists into a single series per filter
    all_stim_durations = {k: pd.concat(v, ignore_index=True) for k, v in all_stim_durations.items()}
    
    return all_stim_durations

# Function to save combined stim_duration DataFrame with self-controlled and non-self-controlled
def save_combined_stim_duration():
    # Load stim_duration for both directories
    non_self_controlled_stim_durations = load_all_stim_durations(non_self_controlled_dir)
    self_controlled_stim_durations = load_all_stim_durations(self_controlled_dir)
    
    # Iterate over the filters (exp1 to exp4)
    for expnum in range(1, 5):
        # Extract the appropriate filter for the experiment (expnum - 1 maps to filter1, filter2, etc.)
        non_self_controlled_stim_duration = non_self_controlled_stim_durations[f'filter{expnum}']
        self_controlled_stim_duration = self_controlled_stim_durations[f'filter{expnum}']
        
        # Create a combined DataFrame with one column for stim_duration
        # and another column 'category' to indicate the group it came from
        non_self_controlled_df = pd.DataFrame({
            'stim_duration': non_self_controlled_stim_duration,
            'category': ['non-self-control'] * len(non_self_controlled_stim_duration)
        })
        
        self_controlled_df = pd.DataFrame({
            'stim_duration': self_controlled_stim_duration,
            'category': ['self-control'] * len(self_controlled_stim_duration)
        })
        
        # Combine both DataFrames into one
        combined_df = pd.concat([non_self_controlled_df, self_controlled_df], ignore_index=True)
        
        # Define file name for the combined CSV
        combined_file = os.path.join(anova_dir, f"Combined_Stim_Duration_Exp{expnum}.csv")

        # Save the DataFrame to CSV
        combined_df.to_csv(combined_file, index=False)

        print(f"Exp {expnum}: Combined DataFrame saved to ANOVA directory.")


# Run the function to save combined stim_duration for all experiments
save_combined_stim_duration()

# %%
