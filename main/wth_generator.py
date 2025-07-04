import pandas as pd
import requests
import os
from datetime import datetime

input_csv = "lat_long.csv"  # Your CSV OBJECTID, Lat, Long
output_dir = "D:/Weather_data_wth"
os.makedirs(output_dir, exist_ok=True)

# NASA POWER base URL
base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params_template = {
    "parameters": "T2M,T2M_MAX,T2M_MIN,ALLSKY_SFC_SW_DWN,RH2M,PRECTOTCORR,WS2M,T2MDEW",
    "start": "19900101",
    "end": "20241231",
    "community": "AG",
    "format": "JSON"
}

# Load your CSV
df = pd.read_csv(input_csv)

# Iterate over each row
for idx, row in df.iterrows():
    object_id = row["OBJECTID"]
    lat = row["Lat"]
    lon = row["Long"]

    print(f"📡 Fetching data for {object_id} ({lat}, {lon})...")

    params = params_template.copy()
    params["latitude"] = lat
    params["longitude"] = lon

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()["properties"]["parameter"]

        # Extract required parameters
        t2m = data.get("T2M", {})
        tmax = data.get("T2M_MAX", {})
        tmin = data.get("T2M_MIN", {})
        srad = data.get("ALLSKY_SFC_SW_DWN", {})
        rhum = data.get("RH2M", {})
        rain = data.get("PRECTOTCORR", {})
        wind = data.get("WS2M", {})
        tdew = data.get("T2MDEW", {})

        
        wth_path = os.path.join(output_dir, f"{int(object_id)}.WTH")
        with open(wth_path, "w") as f:
            f.write(f"$WEATHER DATA: NASA\n\n")
            f.write(f"@ INSI       LAT      LONG    ELEV   TAV   AMP REFHT WNDHT\n")
            f.write(f"  NASA   {lat:<8.5f} {lon:<8.5f}  100.00  22.1   5.6   2.0   2.0\n\n")
            f.write(f"@  DATE   T2M   TMIN   TMAX   TDEW   RHUM   RAIN2   WIND   SRAD   RAIN\n")

            for date_str in tmin.keys():
                dt = datetime.strptime(date_str, "%Y%m%d")
                julian = dt.strftime("%Y") + dt.strftime("%j")
                
                wind_km_day = wind[date_str] * 86.4


                f.write(f"{julian}  {t2m[date_str]:5.1f}  {tmin[date_str]:5.1f}  {tmax[date_str]:5.1f}  {tdew[date_str]:6.1f}  {rhum[date_str]:6.1f}  {rain[date_str]:6.1f}  {wind_km_day:6.1f}  {srad[date_str]:6.1f}  {rain[date_str]:6.1f}\n")

        print(f"Saved: {wth_path}")


    except Exception as e:
        print(f"Failed for {object_id} ({lat}, {lon}): {e}")

print("All WTH files generated.")
