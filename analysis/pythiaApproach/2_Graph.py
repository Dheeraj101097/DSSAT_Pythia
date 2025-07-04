import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- Input and Output Folders ---
input_folder = 'processed_simulations_500'  # Folder containing the simulation CSV files

# Load observed data
obs = pd.read_csv('ValidationObserved.csv')

# Compute average observed yield (kg) per district
obs_avg = obs.groupby('District', as_index=False)['Yield_in_kg'].mean()

# Lists to store results
results = []

for filename in os.listdir(input_folder):
    if filename.endswith('.csv') and 'district' in filename.lower():
        print(f"Processing file: {filename}")

        filepath = os.path.join(input_folder, filename)
        sim = pd.read_csv(filepath)
        sim = sim.rename(columns={'PREDICTED': 'Pred_Yield_kg'})

        # Merge on District
        merged = pd.merge(obs_avg, sim, on='District', how='inner')

        # Calculate error metrics
        mse = mean_squared_error(merged['Yield_in_kg'], merged['Pred_Yield_kg'])
        rmse = np.sqrt(mse)
        mean = np.mean(merged['Yield_in_kg'])
        nrmse = rmse / mean
        # mae = mean_absolute_error(merged['Yield_in_kg'], merged['Pred_Yield_kg'])

        # Append results
        results.append({
            'File': filename,
            'RMSE': rmse,
            'NRMSE': nrmse,
            # 'MAE': mae
        })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save all results to CSV if you want
results_df.to_csv('all_results.csv', index=False)

# Find best RMSE and NRMSE
best_rmse_row = results_df.loc[results_df['RMSE'].idxmin()]
best_nrmse_row = results_df.loc[results_df['NRMSE'].idxmin()]

print("\nBest run based on RMSE:")
print(best_rmse_row)

print("\nBest run based on NRMSE:")
print(best_nrmse_row)

# Add a run index for plotting
results_df = results_df.reset_index().rename(columns={'index': 'RunIndex'})

# Plot both RMSE and NRMSE on separate subplots
sns.set_theme(style="white")
# fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
plt.figure(figsize=(10, 5))

# # RMSE Plot
# sns.lineplot(ax=axs[0], data=results_df, x='RunIndex', y='RMSE', color='lightblue', label='RMSE')
# axs[0].scatter(best_rmse_row.name, best_rmse_row['RMSE'], color='red', s=100, label='Best RMSE')
# axs[0].set_ylabel('RMSE')
# axs[0].legend()

# Line plot
sns.lineplot(data=results_df, x='RunIndex', y='RMSE', color='lightgreen', label='RMSE')

# Scatter the best RMSE point
plt.scatter(best_rmse_row.name, best_rmse_row['RMSE'], color='red', s=100, label='Best RMSE')

# Axis labels and legend
plt.ylabel('RMSE')
plt.xlabel('No. of runs')
plt.title('RMSE Across 500 Runs')
plt.legend()

# Text box at top-right
textstr = f"Best RMSE: {best_rmse_row['RMSE']:.2f}"
plt.text(0.95, 0.95, textstr,
         transform=plt.gca().transAxes,
         fontsize=12,
         verticalalignment='top',
         horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='white', edgecolor='black'))

# # NRMSE Plot
# sns.lineplot(ax=axs[1], data=results_df, x='RunIndex', y='NRMSE', color='lightgreen', label='NRMSE')
# axs[1].scatter(best_nrmse_row.name, best_nrmse_row['NRMSE'], color='red', s=100, label='Best NRMSE')
# axs[1].set_xlabel('Run Index')
# axs[1].set_ylabel('NRMSE')
# axs[1].legend()

# plt.suptitle('RMSE and NRMSE across 500 runs', fontsize=14)
# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("error_metrics_pythia_calrmse.jpg")
plt.show()