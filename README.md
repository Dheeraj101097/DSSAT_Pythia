# DSSAT-Pythia Installation Guide

## Software Requirements

To install and run DSSAT-Pythia on your PC, you will need the following software:

1. **DSSAT**:  
   Download and install DSSAT from [DSSAT website](https://get.dssat.net/request/?sft=4).

2. **Python 3.12**:  
   Download the Python 3.12 installer for Windows or macOS from [Python 3.12 release page](https://www.python.org/downloads/release/python-312/).

   - During installation, select "Customize installation."
   - Select all options under "Optional Features" and "Advanced Options."
   - Note: DSSAT-Pythia works with Python 3.12. If you have another version, uninstall it and download Python 3.8 from the above link.
   - Also install pip from []().

3. **Git**:  
   Download and install Git from [Git download page](https://git-scm.com/download/win).

4. **Community Version of Visual Studio**:  
   Download and install Visual Studio from [Visual Studio website](https://visualstudio.microsoft.com/downloads/).  
   Select the **Desktop development with C++** workload during installation.

5. **RStudio**:  
   To use RStudio on your PC, install both R and RStudio:
   - Download and install R from [CRAN website](https://cran.rstudio.com/).
   - Download and install RStudio from [RStudio website](https://posit.co/download/rstudio-desktop/).

---

## Steps to Install DSSAT-Pythia on PC

1. Enable **Developer Mode**:

   - Open Windows Settings > Update & Security > For Developers.
   - Switch on Developer Mode and restart the computer.

2. Open the **Command Prompt** in the C Drive:

   - Open the C drive and type `cmd` in the address bar and press Enter.

3. Clone the DSSAT-Pythia repository:

   ```bash
   git clone https://github.com/dssat/pythia.git pythia
   ```

4. Navigate to the cloned directory:

   ```bash
   cd pythia
   ```

5. Delete the `poetry.lock` file:

   ```bash
   del poetry.lock
   ```

6. Install Poetry:

   ```bash
   pip install poetry
   ```

7. Install DSSAT-Pythia:
   ```bash
   <full path to poetry>\poetry install
   <full path to poetry>\poetry build
   ```
   - On Windows, poetry will be found in "C:\Users\username\AppData\Local\Programs\Python\Python312\Scripts"
8. Install the Pythia wheel file:

   - Navigate to the `dist` folder and install the `.whl` file:
     ```bash
     cd dist
     pip install pythia-2.3.0-py3-none-any.whl
     ```
   - **Note**: Check the version in the `dist` folder and adjust the command if necessary.If received error

   ```bash
    pip install numpy matplotlib
   ```

9. Add the path to `pythia.exe` to your environment variables.

   - On Windows, file will be found in "C:\username\Python312\Scripts"

10. Close the command prompt.

---

## Troubleshooting

- If you encounter any issues during installation, delete the folder `C:\pythia` and repeat the installation steps.

---

## Input Files Setup

1. Download the `InputFiles.zip` folder from [Google Drive link](https://drive.google.com/file/d/1vlBeWEavNggcuhRMgmO79aHTYZ7aq_Im/view?usp=sharing), unzip it, and save the `Simulation_Data_India` folder in `C:\pythia\`.

2. Open the folder `C:\pythia\Simulation_Data_India\OUTPUT\India` and remove all folders (if any).

   **Note**: Remove the contents from the `OUTPUT` folder every time you run the model.

---

## Running the Model

1. Open the command prompt at `C:\pythia\Simulation_Data_India\India` by typing `cmd` in the folder address bar.

2. Run the following commands to simulate maize and rice:

   ```bash
   pythia --all C:/pythia/Simulation_Data_India/India/IN_SYB.json
   ```

3. To view the output:
   - Open the `.json` file in `C:\pythia\Simulation_Data_India\India\`.
   - Find the working directory in `"workDir": "C:/pythia/Simulation_Data_India/OUTPUT/India/…"` and navigate to that folder.
   - The output will be available in `.csv` format.

---

## Plotting Output in RStudio

1. Open the R code file: ``.

2. Install all required packages and modify the file location on line 22 to match the output `.csv` file.

3. Run the R script to generate the yield plot.

4. The plot will be saved at the location specified in line 62.

   **Note**: If you encounter errors reading the `.csv` file, open the file and delete all columns except `LATITUDE`, `LONGITUDE`, and `HWAH`.

---

# DSSAT-Pythia: End-to-End Workflow Documentation

## 1. Overview

This section details the complete workflow for setting up and running the DSSAT-Pythia modeling framework, including installation, environment setup, weather data generation for India, and automation scripts for file formatting. The process is based on the official [DSSAT-Pythia GitHub repository](https://github.com/DSSAT/pythia.git).

---

## 2. Weather File Generation for India

### 2.1. Purpose

DSSAT requires daily weather files (`.WTH`) for each simulation point. These are generated using NASA POWER API for all required coordinates in India.

### 2.2. Required Input: lat_long.csv

The script expects a CSV file with the following structure:

```
OBJECTID,Lat,Long
1,23.20043513,79.10972744
2,23.20043513,79.40972743
3,23.30043513,78.80972744
... (more rows)
```

- `OBJECTID`: Unique identifier for each location
- `Lat`: Latitude (decimal degrees)
- `Long`: Longitude (decimal degrees)

Place this file in the same directory as the script or update the path in the script.

### 2.3. Script: run_to_gen_wth.py

- **Location:** Simulation_Data/OUTPUT/run_to_gen_wth.py
- **Input:** lat_long.csv
- **Output:** .WTH files in D:/Weather_data_wth/

#### How it works:

1. Reads coordinates from `lat_long.csv`.
2. For each coordinate, queries NASA POWER API for daily weather data (1990–2024).
3. Extracts parameters: temperature, rainfall, humidity, wind, solar radiation, etc.
4. Writes a DSSAT-compatible `.WTH` file for each location.

#### Usage:

1. Open PowerShell or CMD (Ctrl+Shift+`in VS Code, or type`cmd` in the folder address bar).
2. Navigate to the script directory:
   ```sh
   cd C:\pythia\Simulation_Data\OUTPUT
   ```
3. Run the script:
   ```sh
   python wth_generator.py
   ```

- Output `.WTH` files will be saved in `D:/Weather_data_wth/`.

#### Code Explanation:

- The script uses pandas to read the CSV, requests to fetch data from NASA POWER, and writes formatted `.WTH` files for DSSAT.
- Each `.WTH` file contains daily weather data for a specific location, formatted as required by DSSAT.

---

## 3. Automation Code: CSV to CUL Format

### 3.1. Purpose

DSSAT uses `.CUL` files for cultivar information. The automation script (`run_pythia.py`) converts CSV data into DSSAT-compatible `.CUL` files, streamlining the process for large datasets.

### 3.2. Required Input: Cultivar Parameter CSV

- The script expects a CSV file (e.g., `localized_parameters_gaussian350.csv`) containing cultivar parameters for each simulation.
- Make sure to update the file paths in the script for your environment.

### 3.3. Script: run_pythia.py

- **Location:** Kritika maam desktop data/python code/4_csv_cul_formt_atm.py
- **Input:** Cultivar parameter CSV
- **Output:** Updated .CUL file and simulation results CSV

#### How it works:

1. Reads the input CSV containing cultivar parameters.
2. Locates the target cultivar line in the `.CUL` file.
3. Updates the `.CUL` file with new parameters for each simulation.
4. Runs DSSAT-Pythia for each parameter set using subprocess.
5. Collects and saves simulation results (e.g., yield) to a results CSV.

#### Usage:

1. Open PowerShell or CMD (Ctrl+Shift+`in VS Code, or type`cmd` in the folder address bar).
2. Run the script:
   ```sh
   python run_pythia.py
   ```

- The script will update the `.CUL` file and run multiple simulations automatically.
- Results will be saved in a CSV file.

#### Code Explanation:

- The script uses pandas for CSV handling, subprocess to run DSSAT-Pythia, and formats `.CUL` files according to DSSAT requirements.
- Each simulation uses a different set of cultivar parameters, enabling batch processing and sensitivity analysis.

---

## 4. Running Multiple Simulations

- You can open PowerShell in VS Code using ` Ctrl+Shift+`` or open CMD by typing  `cmd` in the folder address bar.
- Use `cd` to navigate to the directory containing your scripts or configuration files.
- Run the desired Python or DSSAT-Pythia commands as shown above.
- For batch simulations, ensure your input files (CSV, JSON, etc.) are correctly set up and referenced in your scripts.

---

## 5. References

- [DSSAT-Pythia GitHub](https://github.com/DSSAT/pythia.git)

---

This workflow enables automated, reproducible DSSAT-Pythia simulations for large-scale, gridded crop modeling, from environment setup to weather data generation and file formatting.
