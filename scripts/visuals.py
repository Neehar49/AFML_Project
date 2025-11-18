import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
import folium
from scipy.stats import zscore

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv("../data/meta_learning_dataset.csv")

regions = {
    "Champaign_IL": (40.12, -87.01),
    "Lubbock_TX": (33.61, -101.82),
    "Yolo_CA": (38.61, -121.83),
    "Lancaster_NE": (40.78, -96.69),
    "Riley_KS": (39.32, -96.73),
    "Story_IA": (42.03, -93.62),
    "Karnal_HR": (29.69, 76.99),
    "Ahmedabad_GJ": (23.02, 72.57),
    "Raichur_KA": (16.20, 77.37),
    "Sitapur_UP": (27.56, 80.68),
    "Thanjavur_TN": (10.79, 79.14),
    "Indore_MP": (22.72, 75.86)
}

# ==========================================================
# 1. TIME SERIES YIELD TREND (unique visual)
# ==========================================================

def plot_yield_trend():
    plt.figure(figsize=(14,6))
    for r in df["region"].unique():
        sub = df[df["region"] == r].groupby("year")["yield"].mean()
        plt.plot(sub.index, sub.values, label=r)

    plt.title("Yield Trends Across Regions (Wheat + Maize)", fontsize=16)
    plt.xlabel("Year")
    plt.ylabel("Yield (t/ha)")
    plt.legend(bbox_to_anchor=(1.02,1), loc="upper left")
    plt.tight_layout()
    plt.savefig("../data/plot_yield_trend.png", dpi=300)
    plt.close()

# ==========================================================
# 2. CORRELATION SPIDER-WEB (climate + NDVI + yield)
# ==========================================================

def plot_spider_correlation():
    features = ["temp_mean","rain_total","humidity_mean",
                "wind_mean","solar_mean","ndvi_mean","yield"]

    corr = df[features].corr()["yield"].iloc[:-1].values
    labels = features[:-1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    corr = np.concatenate((corr, [corr[0]]))
    angles += angles[:1]

    fig = plt.figure(figsize=(7,7))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, corr, linewidth=2)
    ax.fill(angles, corr, alpha=0.3)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    plt.title("Climate–NDVI Feature Influence on Yield", fontsize=14)
    plt.savefig("../data/spider_correlation.png", dpi=300)
    plt.close()

# ==========================================================
# 3. YIELD HEATMAP (REGION x YEAR)
# ==========================================================

def plot_yield_heatmap():
    pivot = df.pivot_table(index="region", columns="year", values="yield", aggfunc="mean")
    plt.figure(figsize=(14,6))
    sns.heatmap(pivot, cmap="viridis")
    plt.title("Yield Heatmap Across Regions and Years", fontsize=16)
    plt.savefig("../data/yield_heatmap.png", dpi=300)
    plt.close()

# ==========================================================
# 4. NDVI vs YIELD SCATTER WITH REGRESSION LINE
# ==========================================================

def plot_ndvi_yield_scatter():
    plt.figure(figsize=(10,6))
    sns.regplot(data=df, x="ndvi_mean", y="yield", scatter_kws={'alpha':0.4})
    plt.title("NDVI vs Yield Relationship", fontsize=16)
    plt.savefig("../data/ndvi_vs_yield.png", dpi=300)
    plt.close()

# ==========================================================
# 5. DUAL-REGION RADAR CHART COMPARISON
# ==========================================================

def region_radar(region1, region2):
    fcols = ["temp_mean","rain_total","humidity_mean","wind_mean","solar_mean","ndvi_mean"]

    r1 = df[df["region"] == region1][fcols].mean()
    r2 = df[df["region"] == region2][fcols].mean()

    r1 = (r1 - r1.min()) / (r1.max() - r1.min())
    r2 = (r2 - r2.min()) / (r2.max() - r2.min())

    labels = fcols
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    r1 = np.concatenate((r1, [r1[0]]))
    r2 = np.concatenate((r2, [r2[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    plt.figure(figsize=(8,8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, r1, label=region1, linewidth=2)
    ax.fill(angles, r1, alpha=0.25)
    ax.plot(angles, r2, label=region2, linewidth=2)
    ax.fill(angles, r2, alpha=0.25)
    plt.title(f"Climate/NDVI Fingerprint: {region1} vs {region2}")
    plt.legend()
    plt.savefig("../data/radar_compare.png", dpi=300)
    plt.close()

# ==========================================================
# 6. MAP OF ALL 12 REGIONS (PLOTLY)
# ==========================================================

def plot_region_map():
    lat = [regions[r][0] for r in regions]
    lon = [regions[r][1] for r in regions]
    names = list(regions.keys())

    fig = px.scatter_geo(
        lat=lat,
        lon=lon,
        text=names,
        title="Geographical Distribution of Selected Regions (USA + India)",
        projection="natural earth"
    )

    fig.write_html("../data/region_map.html")
    print("Saved region_map.html")

# ==========================================================
# 7. FOLIUM INTERACTIVE MAP
# ==========================================================

def plot_interactive_map():
    m = folium.Map(location=[25, 10], zoom_start=2)

    for r, (lat, lon) in regions.items():
        folium.Marker(location=[lat, lon], popup=r).add_to(m)

    m.save("../data/interactive_map.html")

# ==========================================================
# 8. CLIMATE PRINCIPAL COMPONENTS (advanced visual)
# ==========================================================

def plot_pca():
    from sklearn.decomposition import PCA
    fcols = ["temp_mean","rain_total","humidity_mean","wind_mean","solar_mean"]
    X = df[fcols].dropna()
    Xz = X.apply(zscore)

    pca = PCA(n_components=2)
    comps = pca.fit_transform(Xz)

    plt.figure(figsize=(8,6))
    plt.scatter(comps[:,0], comps[:,1], alpha=0.3)
    plt.title("PCA of Climate Features", fontsize=16)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.savefig("../data/pca_climate.png", dpi=300)
    plt.close()

# ==========================================================
# RUN ALL VISUALIZATIONS
# ==========================================================

print("Generating visuals...")

plot_yield_trend()
plot_spider_correlation()
plot_yield_heatmap()
plot_ndvi_yield_scatter()
region_radar("Champaign_IL", "Indore_MP")
plot_region_map()
plot_interactive_map()
plot_pca()

print("All visuals saved in ../data/")
