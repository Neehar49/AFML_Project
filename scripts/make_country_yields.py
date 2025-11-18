import pandas as pd

# Change these paths to your downloaded files
wheat_file = "../data/wheat-yields.csv"
maize_file = "../data/maize-yields.csv"

# Load
wheat = pd.read_csv(wheat_file)
maize = pd.read_csv(maize_file)

# Standardize column names (OWID uses different names sometimes)
wheat.columns = [c.lower().strip() for c in wheat.columns]
maize.columns = [c.lower().strip() for c in maize.columns]

# Identify the yield column automatically
wheat_ycol = [c for c in wheat.columns if "yield" in c][0]
maize_ycol = [c for c in maize.columns if "yield" in c][0]

# Keep only USA + India
keep = ["United States", "India"]

wheat_small = wheat[wheat["entity"].isin(keep)][["entity", "year", wheat_ycol]].copy()
maize_small = maize[maize["entity"].isin(keep)][["entity", "year", maize_ycol]].copy()

# Rename columns
wheat_small = wheat_small.rename(columns={
    "entity": "country",
    wheat_ycol: "yield_tpha"
})
wheat_small["crop"] = "wheat"

maize_small = maize_small.rename(columns={
    "entity": "country",
    maize_ycol: "yield_tpha"
})
maize_small["crop"] = "maize"

# Combine
country = pd.concat([wheat_small, maize_small], axis=0)

# Clean
country["country"] = country["country"].replace({
    "United States": "USA",
    "India": "India"
})

# Save
country = country.sort_values(["country", "crop", "year"])
country.to_csv("../data/country_yields.csv", index=False)

print("Saved ../data/country_yields.csv")
print(country.head())
