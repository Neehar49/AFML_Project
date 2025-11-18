import pandas as pd

# Load country-level yields
country = pd.read_csv("../data/country_yields.csv")

# Region → country mapping
region_country = {
    "Champaign_IL": "USA",
    "Lubbock_TX": "USA",
    "Yolo_CA": "USA",
    "Lancaster_NE": "USA",
    "Riley_KS": "USA",
    "Story_IA": "USA",

    "Karnal_HR": "India",
    "Ahmedabad_GJ": "India",
    "Raichur_KA": "India",
    "Sitapur_UP": "India",
    "Thanjavur_TN": "India",
    "Indore_MP": "India",
}

# Productivity multipliers per region (fixed offsets)
region_offset = {
    "Champaign_IL": 1.15,
    "Lubbock_TX":   0.95,
    "Yolo_CA":      1.05,
    "Lancaster_NE": 1.10,
    "Riley_KS":     1.00,
    "Story_IA":     1.12,

    "Karnal_HR":    1.10,
    "Ahmedabad_GJ": 0.95,
    "Raichur_KA":   0.90,
    "Sitapur_UP":   1.00,
    "Thanjavur_TN": 0.92,
    "Indore_MP":    1.05,
}

years = list(range(2000, 2024))  # longest possible 2000–2023
crops = ["wheat", "maize"]

rows = []

for region, country_name in region_country.items():
    for year in years:
        for crop in crops:

            row = country[
                (country["country"] == country_name) &
                (country["year"] == year) &
                (country["crop"] == crop)
            ]

            if row.empty:
                continue

            nat_yield = float(row.iloc[0]["yield_tpha"])  # t/ha
            factor = region_offset[region]

            reg_yield = nat_yield * factor

            rows.append({
                "region": region,
                "year": year,
                "crop": crop,
                "yield": reg_yield
            })

yield_df = pd.DataFrame(rows)
yield_df = yield_df.sort_values(["region", "crop", "year"])

yield_df.to_csv("../data/yield_labels.csv", index=False)
print("Saved yield_labels.csv with shape:", yield_df.shape)
print(yield_df.head())
