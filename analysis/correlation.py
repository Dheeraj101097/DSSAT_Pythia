import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

file_path = '' # This is the file path of the results paste csv file here
df = pd.read_csv(file_path)

print("Data Loaded Successfully!")

column_mapping = {
    'HWAM': 'Yield (kg/ha)',
    'PRCP': 'Rainfall',
    'TMAXA': 'Max Temp.',
    'TMINA': 'Min Temp.',
    'SRADA': 'Solar Radiation'
}

# Select columns
weather_columns = ['PRCP', 'TMAXA', 'TMINA', 'SRADA']
analysis_columns = ['HWAM'] + weather_columns

corr_matrix = df[analysis_columns].corr()

# Rename columns and index for better readability
corr_matrix.rename(columns=column_mapping, index=column_mapping, inplace=True)

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='PuRd', vmin=-1, vmax=1, annot_kws={"size": 14})
plt.title('Correlation Between Yield and Weather Variables', fontsize=12)
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("correlation.jpg", dpi=300)
plt.show()
