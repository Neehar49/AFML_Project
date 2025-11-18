import pandas as pd

def clean_ndvi_csv(file_path, output_path):
    df = pd.read_csv(file_path)

    # Keep only the useful columns and rename mean -> ndvi_mean
    df = df[['region', 'year', 'mean']].rename(columns={'mean': 'ndvi_mean'})
    df['region'] = df['region'].str.strip()
    df['year'] = df['year'].astype(int)
    df = df.sort_values(['region', 'year']).reset_index(drop=True)

    df.to_csv(output_path, index=False)
    print("Saved:", output_path)
    return df

if __name__ == "__main__":
    clean_ndvi_csv("../data/NDVI_MODIS_regions_yearly.csv", "../data/ndvi_clean.csv")
