"""
02_eda_visuals.py
Exploratory analysis + charts answering the project's core business
questions. Saves each chart as a PNG in ../visuals/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
IN_PATH = "../data/cleaned/CAvideos_clean.csv"
VIZ_DIR = "../visuals"

df = pd.read_csv(IN_PATH, parse_dates=["trending_date", "publish_time"])

# Deduped view: one row per video (first trending appearance), used for
# any chart where counting the same video multiple times would distort
# the picture (e.g. "which category trends most often").
df_unique = df.sort_values("trending_date").drop_duplicates("video_id", keep="first")

# ---------------------------------------------------------------------
# Q1: Which categories dominate trending?
# ---------------------------------------------------------------------
plt.figure(figsize=(10, 6))
order = df_unique["category_name"].value_counts().index
sns.countplot(data=df_unique, y="category_name", order=order, hue="category_name",
              palette="viridis", legend=False)
plt.title("Number of Unique Trending Videos by Category (CA)")
plt.xlabel("Number of Videos")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/01_category_counts.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------
# Q2: How long do videos stay trending, by category?
# ---------------------------------------------------------------------
top_cats = df_unique["category_name"].value_counts().head(8).index
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_unique[df_unique["category_name"].isin(top_cats)],
    x="days_trending", y="category_name", hue="category_name",
    order=top_cats, palette="mako", legend=False,
)
plt.title("Days Spent Trending by Category (Top 8 Categories)")
plt.xlabel("Days Trending")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/02_trending_duration_by_category.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------
# Q3: Does publish timing (day of week / hour) relate to trending success?
# ---------------------------------------------------------------------
plt.figure(figsize=(10, 6))
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sns.countplot(data=df_unique, x="publish_dayofweek", order=day_order,
              hue="publish_dayofweek", palette="crest", legend=False)
plt.title("Trending Videos by Publish Day of Week")
plt.xlabel("Day Published")
plt.ylabel("Number of Videos")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/03_publish_day_of_week.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------
# Q4: Relationship between engagement (likes) and views
# ---------------------------------------------------------------------
plt.figure(figsize=(8, 6))
sample = df_unique.sample(min(3000, len(df_unique)), random_state=42)
sns.scatterplot(data=sample, x="views", y="likes", alpha=0.4, s=20)
plt.xscale("log")
plt.yscale("log")
plt.title("Views vs. Likes (log-log scale)")
plt.xlabel("Views (log scale)")
plt.ylabel("Likes (log scale)")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/04_views_vs_likes.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------
# Q5: Title length vs. views — does a shorter/longer title trend better?
# ---------------------------------------------------------------------
plt.figure(figsize=(8, 6))
sns.regplot(
    data=df_unique.sample(min(3000, len(df_unique)), random_state=42),
    x="title_length", y="views", scatter_kws={"alpha": 0.3, "s": 15},
    line_kws={"color": "red"}, lowess=False,
)
plt.yscale("log")
plt.title("Title Length vs. Views")
plt.xlabel("Title Length (characters)")
plt.ylabel("Views (log scale)")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/05_title_length_vs_views.png", dpi=150)
plt.close()

print("Saved 5 charts to", VIZ_DIR)

# ---------------------------------------------------------------------
# Print a few headline stats for the README
# ---------------------------------------------------------------------
print("\n--- Headline stats ---")
print("Total unique videos:", df_unique.shape[0])
print("Date range:", df["trending_date"].min().date(), "to", df["trending_date"].max().date())
print("\nTop 5 categories by video count:")
print(df_unique["category_name"].value_counts().head(5))
print("\nAvg days trending overall:", round(df_unique["days_trending"].mean(), 2))
print("\nAvg days trending, top category (",
      df_unique["category_name"].value_counts().idxmax(), "):",
      round(df_unique[df_unique["category_name"] == df_unique["category_name"].value_counts().idxmax()]["days_trending"].mean(), 2))
print("\nBest publish day (most trending videos):", df_unique["publish_dayofweek"].value_counts().idxmax())
print("\nCorrelation views vs likes:", round(df_unique[["views", "likes"]].corr().iloc[0, 1], 3))
print("Correlation title_length vs views:", round(df_unique[["title_length", "views"]].corr().iloc[0, 1], 3))
