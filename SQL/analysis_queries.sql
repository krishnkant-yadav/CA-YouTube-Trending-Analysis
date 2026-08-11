-- ============================================================
-- CA YouTube Trending Analysis — SQL Queries
-- Database: data/cleaned/ca_trending.db
-- Table: trending_videos (one row per video per trending day)
-- ============================================================

-- 1. Top 10 channels by number of unique trending videos
SELECT channel_title,
       COUNT(DISTINCT video_id) AS unique_trending_videos
FROM trending_videos
GROUP BY channel_title
ORDER BY unique_trending_videos DESC
LIMIT 10;


-- 2. Average views, likes, and comment ratio by category
--    (use only each video's first trending appearance to avoid double count)
WITH first_appearance AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY video_id ORDER BY trending_date ASC
           ) AS rn
    FROM trending_videos
)
SELECT category_name,
       COUNT(*) AS num_videos,
       ROUND(AVG(views), 0) AS avg_views,
       ROUND(AVG(likes), 0) AS avg_likes,
       ROUND(AVG(comment_ratio), 4) AS avg_comment_ratio
FROM first_appearance
WHERE rn = 1
GROUP BY category_name
ORDER BY avg_views DESC;


-- 3. Which category keeps videos trending the longest, on average?
WITH first_appearance AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY video_id ORDER BY trending_date ASC
           ) AS rn
    FROM trending_videos
)
SELECT category_name,
       ROUND(AVG(days_trending), 2) AS avg_days_trending,
       COUNT(*) AS num_videos
FROM first_appearance
WHERE rn = 1
GROUP BY category_name
HAVING num_videos >= 30          -- filter out tiny/noisy categories
ORDER BY avg_days_trending DESC;


-- 4. Does day of week published relate to trending success (avg views)?
WITH first_appearance AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY video_id ORDER BY trending_date ASC
           ) AS rn
    FROM trending_videos
)
SELECT publish_dayofweek,
       COUNT(*) AS num_videos,
       ROUND(AVG(views), 0) AS avg_views
FROM first_appearance
WHERE rn = 1
GROUP BY publish_dayofweek
ORDER BY avg_views DESC;


-- 5. Videos with comments/ratings disabled — does that affect apparent engagement?
SELECT comments_disabled,
       ratings_disabled,
       COUNT(*) AS num_rows,
       ROUND(AVG(views), 0) AS avg_views,
       ROUND(AVG(like_ratio), 4) AS avg_like_ratio
FROM trending_videos
GROUP BY comments_disabled, ratings_disabled;


-- 6. Top 10 single-day trending videos by views
SELECT title, channel_title, category_name, trending_date, views, likes
FROM trending_videos
ORDER BY views DESC
LIMIT 10;
