import numpy as np
import subprocess
import pandas as pd
import os
# --- File paths ---
output_folder = 'cleaned_simulations'
os.makedirs(output_folder, exist_ok=True)
cul_file_path = "C:/pythia/Simulation_Data_India/India/CUL_files/SBGRO048.CUL"
csv_param_path = "generated_parameters2.csv"
summary_csv_path = "C:/pythia/Simulation_Data_India/OUTPUT/India/Soybean/India_soybean_yield_est/India_soybean_yield.csv"
json_config_path = "C:/pythia/Simulation_Data_India/India/IN_SYB.json"

# --- DSSAT Field Widths ---
field_widths = [6, 6, 16, 7] + ([6] * 18) # Total 22 fields

# --- Each Field Decimal Points ---
decimal_precision = {
   4: 2, 5: 3, 6: 1, 7: 1, 8: 1, 9: 2, 10: 2, 11: 3, 12: 0, 13: 1, 14: 2, 15: 3, 16: 1, 17: 2, 18: 1, 19: 1, 20: 3, 21: 3
}

# --- Fixed-width line parser ---
def parse_fixed_width_line(line, field_widths):
    fields = []
    position = 0
    for width in field_widths:
        fields.append(line[position:position + width].strip())
        position += width
    return fields

# --- values are replaced here with the new values ---
def format_fixed_width_line(fields, field_widths):
    formatted = ""
    for idx, (value, width) in enumerate(zip(fields, field_widths)):
        try:
            num_val = float(value)
            if idx in decimal_precision:
                precision = decimal_precision[idx]
                if precision == 0 and num_val.is_integer():
                    formatted += f"{num_val:>{width}.0f}."
                else:
                    formatted_number = f"{num_val:.{precision}f}"
                    if formatted_number.startswith("0.") and precision > 0:
                        formatted_number = formatted_number[1:]
                    formatted += f"{formatted_number:>{width}}"
            else:
                formatted += f"{value:>{width}}"
        except ValueError:
            formatted += f"{value:>{width}}"
    return formatted + '\n'

param_df = pd.read_csv(csv_param_path)

with open(cul_file_path, 'r') as file:
    cul_lines = file.readlines()

# Find the cultivar line index best for the simulation in INDIA 
target_cultivar_code = "IB0001"
target_cultivar_name = "BRAGG"
cultivar_idx = None
for idx, line in enumerate(cul_lines):
    if line.startswith(target_cultivar_code) and target_cultivar_name in line:
        cultivar_idx = idx
        break

if cultivar_idx is None:
    raise ValueError("Target cultivar not found in .CUL file.")

original_line = cul_lines[cultivar_idx]
fixed_part = original_line[:37]  # IB0001 BRAGG                . SB0701 fixed this part 

fixed_fields = [
        fixed_part[:6].strip(),    # IB0001
        fixed_part[6:21].strip(),  # BRAGG
        fixed_part[21:24].strip(), # " . "
        fixed_part[24:37].strip()  # SB0701
    ]
results = []

# --- Run Simulation for each parameter set ---
for idx, row in param_df.iterrows():
    print(f"Running simulation {idx + 1}/{len(param_df)}")

    new_params = row.values.tolist()
    all_fields = fixed_fields + [str(x) for x in new_params]

    # Format the full line with correct widths
    updated_line = format_fixed_width_line(all_fields, field_widths)
    cul_lines[cultivar_idx] = updated_line

    # Save the updated .CUL file
    with open(cul_file_path, 'w') as file:
        file.writelines(cul_lines)

    # Run Pythia simulation
    try:
        subprocess.run(['pythia', '--all', json_config_path], check=True)
        df = pd.read_csv(summary_csv_path)
        sim_yield = df['HWAM'].mean()
        # --- Clean and Save CSV ---
        # Select required columns You can add more columns if you want
        selected_columns = ['LATITUDE', 'LONGITUDE', 'LAT', 'LONG', 'SDAT', 'WYEAR', 'HWAM']
        df_cleaned = df[selected_columns]
        # Drop rows where all values are NaN (completely empty rows)
        df_cleaned = df_cleaned.dropna(how='all')

         # Save the cleaned CSV inside the folder
        cleaned_csv_path = os.path.join(output_folder, f'simulation_{idx + 1}.csv')
        df_cleaned.to_csv(cleaned_csv_path, index=False)

    except Exception as e:
        print(f"Simulation {idx + 1} failed: {str(e)}")
        sim_yield = np.nan

    # Save results
    result_row = row.to_dict()
    result_row['sim_yield'] = sim_yield
    results.append(result_row)

    print(f"Simulation {idx + 1} | Yield: {sim_yield:.2f} kg/ha")

# --- Save final results ---
results_df = pd.DataFrame(results)
results_df.to_csv("cul_batch_simulation_results.csv", index=False)
print("All simulations completed and results saved.")
