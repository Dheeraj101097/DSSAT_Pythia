import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

# --- Input and Output Folders ---
input_folder = 'cleaned_simulations_500'        # Folder containing your CSV files
output_folder = 'processed_simulations_500'   # Folder to save the processed files
os.makedirs(output_folder, exist_ok=True)

# --- Load the district shapefile ---
gdf_districts = gpd.read_file('C:/pythia/Simulation_Data_India/India/shapes/ROI.shp')  # Update the path if needed

# --- Process each CSV file in the input folder ---
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        print(f"Processing file: {filename}")
        
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)
        
        # Create geometry
        geometry = [Point(xy) for xy in zip(df['LAT'], df['SOIL_ID'])]
        gdf_points = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
        
        # Spatial join to assign district
        gdf_joined = gpd.sjoin(gdf_points, gdf_districts, how='inner', predicate='within')
        
        # Keep relevant columns adjust column names seeing csv file it gives error
        points_with_district = gdf_joined[['LAT', 'SOIL_ID', 'District', 'WSTA', 'CWAM']]
        
        # Group by district and year, calculate mean yield
        summary = points_with_district.groupby(['District', 'WSTA'], as_index=False)['CWAM'].sum()
        summary = summary.rename(columns={'HWAM': 'TOTAL_HWAM'})

        # Group by district and calculate overall mean yield across all years
        district_mean_yield = points_with_district.groupby('District', as_index=False)['CWAM'].mean()
        district_mean_yield = district_mean_yield.rename(columns={'HWAM': 'Mean_Yield_Across_Years'})
        
        # Save the outputs
        base_filename = os.path.splitext(filename)[0]  # Get filename without extension
        points_with_district.to_csv(os.path.join(output_folder, f'{base_filename}_points.csv'), index=False)
        summary.to_csv(os.path.join(output_folder, f'{base_filename}_summary.csv'), index=False)
        district_mean_yield.to_csv(os.path.join(output_folder, f'{base_filename}_district_mean_yield.csv'), index=False)
        
        print(f"Processed and saved: {base_filename}_points.csv, {base_filename}_summary.csv, and {base_filename}_district_mean_yield.csv")

print("All files processed successfully.")