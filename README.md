# CA YouTube Trending Video Analysis

**A data analytics project exploring what drives videos to trend on YouTube Canada, and what keeps them there.**

## Problem Statement

YouTube Canada's daily "Trending" tab surfaces a small fraction of uploaded videos. For a content strategist or marketing team, understanding *what characteristics correlate with trending success* — category, publish timing, engagement patterns — can directly inform content and posting strategy.

This project analyzes ~40,000 trending-video snapshots (24,000+ unique videos, Nov 2017–Jun 2018) to answer:

1. Which content categories dominate CA trending?
2. How long do videos typically stay trending, and does that vary by category?
3. Does publish day of week relate to trending success?
4. How strongly do views and likes correlate — is engagement predictable from reach?
5. Does title length have any relationship to view count?

## Data Source

[Kaggle: Trending YouTube Video Statistics](https://www.kaggle.com/datasnaek/youtube-new) (CA region, `CAvideos.csv`).

## Methodology

1. **Cleaning** (`notebooks/01_data_cleaning.py`): parsed non-standard date formats, fixed UTF-8 encoding artifacts in titles/descriptions, mapped numeric `category_id` to readable names, engineered features (title length, tag count, engagement ratios, days spent trending).
2. **SQL analysis** (`sql/analysis_queries.sql`): loaded cleaned data into SQLite; wrote window-function queries to deduplicate multi-day trending videos and aggregate by category/channel/publish day.
3. **EDA & visualization** (`notebooks/02_eda_visuals.py`): five charts answering the questions above using pandas + seaborn.

**Note on duplicates:** the raw data has one row per video *per day it trended*. Rows were intentionally kept (not deduplicated) so trending duration could be analyzed as a time series; a `days_trending` feature and a deduplicated "first appearance" view are used for any aggregate that shouldn't double-count a video.

## Key Findings

- **Entertainment dominates**: ~34% of all unique trending videos fall under "Entertainment" — more than 2.5x the next-largest category (News & Politics).
- **Trending is short-lived**: the average video stays on the trending list for only ~1.7 days, with little variation across top categories — trending status is more of a spike than a sustained state.
- **Friday is the strongest publish day** for videos that go on to trend, consistent with content strategies that target weekend viewing.
- **Views and likes are strongly correlated** (r ≈ 0.71), suggesting like-count is a reasonably reliable proxy for reach when likes data is unavailable.
- **Title length has no meaningful relationship with views** (r ≈ -0.01) — for this dataset, a punchy vs. long title made no measurable difference to view count.

## Business Recommendation

For a channel targeting the CA market, category and publish-day choices appear to matter far more than title-length optimization. Entertainment-adjacent framing and Friday releases align with the highest historical trending activity — though causation isn't established here and would need A/B testing to confirm.

## Repo Structure

```
CA-YouTube-Trending-Analysis/
├── README.md
├── data/
│   ├── raw/CAvideos.xlsx
│   └── cleaned/CAvideos_clean.csv, ca_trending.db
├── notebooks/
│   ├── 01_data_cleaning.py
│   ├── 02_eda_visuals.py
│   └── 03_load_to_sqlite.py
├── sql/analysis_queries.sql
├── visuals/ (5 PNG charts)
└── requirements.txt
```

## Limitations

- Dataset covers a fixed ~7-month window (2017–2018); findings reflect that period's platform algorithm and audience behavior, not necessarily current trends.
- "Trending" is CA-region only and reflects YouTube's own (undisclosed) ranking algorithm, not raw popularity.
- Category mapping uses YouTube's standard global category set since the original per-region JSON file wasn't available; all IDs in this dataset are covered by it.

## How to Run

```bash
pip install -r requirements.txt
cd notebooks
python 01_data_cleaning.py
python 03_load_to_sqlite.py
python 02_eda_visuals.py
```
