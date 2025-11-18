import os
import pandas as pd

def parse_nasa_power_monthly(file_path, region_name):
    """
    Parse one NASA POWER monthly CSV (PARAMETER, YEAR, JAN..DEC, ANN format)
    into yearly features for one region.
    """
    # Find where the data table starts (PARAMETER row)
    with open(file_path, "r") as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("PARAMETER"):
            start_idx = i
            break

    if start_idx is None:
        raise ValueError(f"'PARAMETER' header not found in {file_path}")

    df = pd.read_csv(file_path, skiprows=start_idx)
    df.columns = df.columns.str.strip()

    parameter_map = {
        "T2M": "temp_mean",
        "RH2M": "humidity_mean",
        "WS2M": "wind_mean",
        "ALLSKY_SFC_SW_DWN": "solar_mean",
        "ALLSKY_SF": "solar_mean",          # sometimes abbreviated
        "IMERG_PRECTOT": "rain_total",
        "PRECTOTCORR": "rain_total"
    }

    keep = [p for p in df["PARAMETER"].unique() if p in parameter_map]
    df = df[df["PARAMETER"].isin(keep)]

    # Pivot so each parameter becomes a column; use ANN as yearly value
    pivot_df = df.pivot(index="YEAR", columns="PARAMETER", values="ANN")
    pivot_df.rename(columns=parameter_map, inplace=True)

    pivot_df["region"] = region_name
    pivot_df = pivot_df.sort_index().reset_index()  # YEAR back as a column

    return pivot_df


def parse_all_regions(input_folder, output_csv):
    region_map = {
        # India
        "Thanjavur_TN":  "POWER_Point_Monthly_20000101_20251231_010d79N_079d14E_LST.csv",
        "Raichur_KA":    "POWER_Point_Monthly_20000101_20251231_016d20N_077d37E_LST.csv",
        "Indore_MP":     "POWER_Point_Monthly_20000101_20251231_022d72N_075d86E_LST.csv",
        "Ahmedabad_GJ":  "POWER_Point_Monthly_20000101_20251231_023d02N_072d57E_LST.csv",
        "Sitapur_UP":    "POWER_Point_Monthly_20000101_20251231_027d56N_080d68E_LST.csv",
        "Karnal_HR":     "POWER_Point_Monthly_20000101_20251231_029d69N_076d99E_LST.csv",

        # USA
        "Lubbock_TX":    "POWER_Point_Monthly_20000101_20251231_033d61N_0101d82W_LST.csv",
        "Yolo_CA":       "POWER_Point_Monthly_20000101_20251231_038d61N_0121d83W_LST.csv",
        "Riley_KS":      "POWER_Point_Monthly_20000101_20251231_039d32N_096d73W_LST.csv",
        "Champaign_IL":  "POWER_Point_Monthly_20000101_20251231_040d12N_087d01W_LST.csv",
        "Lancaster_NE":  "POWER_Point_Monthly_20000101_20251231_040d78N_096d69W_LST.csv",
        "Story_IA":      "POWER_Point_Monthly_20000101_20251231_042d03N_093d62W_LST.csv",
    }

    all_dfs = []
    for region_name, filename in region_map.items():
        fp = os.path.join(input_folder, filename)
        print("Parsing:", region_name)
        df = parse_nasa_power_monthly(fp, region_name)
        all_dfs.append(df)

    final_df = pd.concat(all_dfs, axis=0)
    final_df.to_csv(output_csv, index=False)
    print("Saved:", output_csv)
    return final_df


if __name__ == "__main__":
    parse_all_regions("../data/climate_raw", "../data/climate_all_regions.csv")
