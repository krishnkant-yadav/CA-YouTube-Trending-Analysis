"""
01_data_cleaning.py
Cleans the raw CAvideos dataset (YouTube Canada Trending Videos) and
produces a cleaned CSV ready for analysis.

Input : data/raw/CAvideos.xlsx
Output: data/cleaned/CAvideos_clean.csv
"""

import pandas as pd
import numpy as np

RAW_PATH = "../data/raw/CAvideos.xlsx"
OUT_PATH = "../data/cleaned/CAvideos_clean.csv"

# ---------------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------------
df = pd.read_excel(RAW_PATH)
print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------------
# 2. Standard YouTube category_id -> category name mapping
#    (This dataset's original Kaggle release ships a CA_category_id.json;
#    IDs below are YouTube's global standard category set, which covers
#    every id present in this file.)
# ---------------------------------------------------------------------
CATEGORY_MAP = {
    1: "Film & Animation", 2: "Autos & Vehicles", 10: "Music",
    15: "Pets & Animals", 17: "Sports", 18: "Short Movies",
    19: "Travel & Events", 20: "Gaming", 21: "Videoblogging",
    22: "People & Blogs", 23: "Comedy", 24: "Entertainment",
    25: "News & Politics", 26: "Howto & Style", 27: "Education",
    28: "Science & Technology", 29: "Nonprofits & Activism",
    30: "Movies", 31: "Anime/Animation", 32: "Action/Adventure",
    33: "Classics", 34: "Comedy", 35: "Documentary", 36: "Drama",
    37: "Family", 38: "Foreign", 39: "Horror", 40: "Sci-Fi/Fantasy",
    41: "Thriller", 42: "Shorts", 43: "Shows", 44: "Trailers",
}
df["category_name"] = df["category_id"].map(CATEGORY_MAP).fillna("Unknown")

# ---------------------------------------------------------------------
# 3. Drop rows with missing video_id (can't be reliably analyzed/joined)
# ---------------------------------------------------------------------
before = len(df)
df = df.dropna(subset=["video_id"])
print(f"Dropped {before - len(df)} rows with missing video_id")

# ---------------------------------------------------------------------
# 4. Fix encoding artifacts in text fields (mis-decoded UTF-8, e.g. "Ã©")
# ---------------------------------------------------------------------
def fix_encoding(text):
    if pd.isna(text) or not isinstance(text, str):
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text

# Excel auto-converted some text values that look like dates/numbers
# (e.g. certain tag strings) into datetime/numeric types on load.
# Coerce these text columns back to plain strings before further cleaning.
def to_text(x):
    if pd.isna(x):
        return x
    return str(x)

for col in ["title", "channel_title", "tags", "description"]:
    df[col] = df[col].apply(to_text).apply(fix_encoding)

# ---------------------------------------------------------------------
# 5. Parse dates
#    trending_date is in YY.DD.MM format (Kaggle's odd original format)
#    publish_time is ISO 8601
# ---------------------------------------------------------------------
df["trending_date"] = pd.to_datetime(df["trending_date"], format="%y.%d.%m")
df["publish_time"] = pd.to_datetime(df["publish_time"])

df["publish_date"] = df["publish_time"].dt.date
df["publish_hour"] = df["publish_time"].dt.hour
df["publish_dayofweek"] = df["publish_time"].dt.day_name()

# Days between publish and this trending appearance
df["days_to_trend"] = (df["trending_date"] - df["publish_time"].dt.tz_localize(None)).dt.days

# ---------------------------------------------------------------------
# 6. Feature engineering
# ---------------------------------------------------------------------
df["title_length"] = df["title"].str.len()
df["tag_count"] = df["tags"].apply(
    lambda x: 0 if pd.isna(x) or not isinstance(x, str) or x == "[none]"
    else len(x.split("|"))
)
df["description_length"] = df["description"].fillna("").str.len()

# Engagement ratios (avoid divide-by-zero)
df["like_ratio"] = df["likes"] / df["views"].replace(0, np.nan)
df["dislike_ratio"] = df["dislikes"] / df["views"].replace(0, np.nan)
df["comment_ratio"] = df["comment_count"] / df["views"].replace(0, np.nan)

# ---------------------------------------------------------------------
# 7. Trending-duration feature (how many days each video stayed trending)
#    Computed here and kept on EVERY row (time-series kept intact) so you
#    can filter to unique videos later without losing this info.
# ---------------------------------------------------------------------
trend_counts = df.groupby("video_id")["trending_date"].transform("count")
df["days_trending"] = trend_counts

# ---------------------------------------------------------------------
# 8. Save
#    NOTE ON DUPLICATES: rows are intentionally KEPT (not deduped).
#    Each row = one video's stats on one trending day, which lets you
#    analyze trend trajectories over time (recommended for this project).
#    For snapshot-style aggregates (e.g. "top videos overall"), group by
#    video_id and take the max/last row per group at analysis time.
# ---------------------------------------------------------------------
df.to_csv(OUT_PATH, index=False)
print(f"Saved cleaned data: {OUT_PATH}")
print(f"Final shape: {df.shape}")
print(f"Unique videos: {df['video_id'].nunique():,}")
