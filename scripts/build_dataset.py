import pandas as pd

def main():
    climate = pd.read_csv("../data/climate_all_regions.csv")
    ndvi    = pd.read_csv("../data/ndvi_clean.csv")
    yields  = pd.read_csv("../data/yield_labels.csv")

    # Merge climate + NDVI
    merged = climate.merge(
        ndvi,
        left_on=["region", "YEAR"],
        right_on=["region", "year"],
        how="inner"
    ).drop(columns=["year"])

    merged = merged.rename(columns={"YEAR": "year"})

    # Merge with yields
    full = merged.merge(
        yields,
        on=["region", "year"],
        how="inner"
    )

    full = full.sort_values(["region", "crop", "year"]).reset_index(drop=True)
    full.to_csv("../data/meta_learning_dataset.csv", index=False)
    print("Saved meta_learning_dataset.csv", full.shape)

if __name__ == "__main__":
    main()
