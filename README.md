# Meta-Learning for Climate-Adaptive Crop Yield Prediction

**Course:** Advanced Foundations of Machine Learning  
**Author:** \<Your Name\>  
**Project:** Meta-learning for wheat & maize yield prediction across USA + India using climate and NDVI features.

---

## 1. Overview

This project builds a **meta-learning pipeline** to predict **wheat and maize yields** using:

- **Climate features** from NASA POWER (temperature, rainfall, humidity, wind, solar radiation),
- **Vegetation index** from MODIS NDVI,
- **Crop type** (wheat vs maize),

for **12 regions** (6 US counties + 6 Indian districts).

Each **(region, crop)** pair is treated as a **task**. A shared encoder is trained across all tasks, and then evaluated in an **ANIL-style meta-learning setting**: for a held-out region, the encoder is frozen and a small task-specific head is adapted using only a few years of data.

The project demonstrates:

- Multi-source data integration (climate + NDVI + yield),
- Basic meta-learning ideas (shared representation + fast adaptation),
- Rich visualizations for exploratory analysis.

---

## 2. Regions and Crops

**USA counties**

- Champaign_IL (Illinois)  
- Lubbock_TX (Texas)  
- Yolo_CA (California)  
- Lancaster_NE (Nebraska)  
- Riley_KS (Kansas)  
- Story_IA (Iowa)  

**Indian districts**

- Karnal_HR (Haryana)  
- Ahmedabad_GJ (Gujarat)  
- Raichur_KA (Karnataka)  
- Sitapur_UP (Uttar Pradesh)  
- Thanjavur_TN (Tamil Nadu)  
- Indore_MP (Madhya Pradesh)  

**Crops**

- `wheat`
- `maize` (corn)

---

## 3. Data Pipeline

All data lives in `data/`.

### 3.1 Climate (NASA POWER)

Raw monthly/annual agro-climatology CSVs downloaded for each region:

- Stored in `data/climate_raw/`
- Parsed by `scripts/climate_parser.py` into annual features:
  - `temp_mean`, `rain_total`, `humidity_mean`, `wind_mean`, `solar_mean`
- Output: **`data/climate_all_regions.csv`**

### 3.2 NDVI (MODIS)

Annual mean NDVI per region from MODIS (exported from GEE):

- Raw export: `data/NDVI_MODIS_regions_yearly.csv`
- Cleaned by `scripts/ndvi_clean.py`
- Output: **`data/ndvi_clean.csv`** with columns:
  - `region, year, ndvi_mean`

### 3.3 Yield (Country-level → Region-level)

1. National wheat and maize yields (t/ha) for USA and India downloaded from
   Our World in Data (or FAO/World Bank) as:
   - `data/wheat-yields.csv`
   - `data/maize-yields.csv`

2. `scripts/make_country_yields.py` extracts only USA + India and normalizes to:

   ```text
   country, year, crop, yield_tpha