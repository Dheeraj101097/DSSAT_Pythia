import pandas as pd
import numpy as np
import re

cul_file_path = 'SBGRO048.CUL'
csv_output_path = 'generated_parameters5.csv' # This is the output file path cahnge name if you want

n_samples = 50 # This is the number of samples you want to generate

# Fixed DSSAT field widths for parsing
field_widths = [6, 18, 3, 7] + [7] * 18

# Read CUL file
with open(cul_file_path, 'r') as file:
    lines = file.readlines()

# Extract headers and parameter lines
header_line = next(line for line in lines if line.startswith('@VAR#'))
calibration_line = next(line for line in lines if line.startswith('!Calibration'))
minima_line = next(line for line in lines if line.startswith('999991 MINIMA'))
maxima_line = next(line for line in lines if line.startswith('999992 MAXIMA'))
bragg_line = next(line for line in lines if line.startswith('IB0001') and 'BRAGG' in line)

# Parse headers
headers = re.split(r'\s+', header_line.strip())[4:]

# Parse calibration flags
calibration_flags = re.split(r'\s+', calibration_line.strip())[1:]

# Parse minima, maxima, and base (BRAGG) values
minima_values = re.split(r'\s+', minima_line.strip())[4:]
maxima_values = re.split(r'\s+', maxima_line.strip())[4:]
bragg_values = re.split(r'\s+', bragg_line.strip())[4:]

# Prepare the data for CSV
rows = []

for _ in range(n_samples):
    row = []
    for idx, (flag, min_val, max_val, base_val) in enumerate(zip(calibration_flags, minima_values, maxima_values, bragg_values)):
        if flag in ['P', 'G']:
            sampled_val = np.random.uniform(float(min_val), float(max_val))
        else:
            sampled_val = float(base_val)
        
        
        if sampled_val.is_integer():
            formatted_val = f"{int(sampled_val)}." 
        else:
            if abs(sampled_val) < 1:
                formatted_val = f"{sampled_val:.3f}".lstrip('0')  # .400 instead of 0.400 -->check and cahnge if issue still exists
            else:
                formatted_val = f"{sampled_val:.3f}"
        
        row.append(formatted_val)
    
    rows.append(row)

# Save to CSV
df = pd.DataFrame(rows, columns=headers)
df.to_csv(csv_output_path, index=False)

print(f"CSV file generated successfully: {csv_output_path}")
