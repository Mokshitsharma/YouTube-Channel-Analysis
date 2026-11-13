<!-- readme-refresh 2026-11 -->
<div align="center">

# ▶️ YouTube Channel Analysis

**Every video of a channel via the YouTube Data API, analysed in Power BI**

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas" /> <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI" />

</div>

## ✨ Highlights

- Pulls every video's stats with YouTube Data API v3
- Computes engagement metrics
- Exports to Power BI

<!-- body -->
A Python script to fetch detailed video statistics from a YouTube channel using the YouTube Data API. The script extracts video metadata, view counts, likes, comments, durations, and engagement metrics, and saves this data as a CSV file.

## Features

- Supports fetching data from channel URLs by handle, custom URL, or channel ID
- Retrieves all videos (up to API limits) from the specified channel
- Extracts video details including:
  - Title
  - Publish date
  - Views, likes, comments
  - Video duration (in seconds)
  - Like rate (%), comment rate (%), engagement rate (%)
- Saves consolidated data to `yt_channel_data.csv` for analysis

## Requirements

- Python 3.x
- pandas
- requests

Install dependencies using:

```bash
pip install pandas requests
```

## Setup

1. Obtain a YouTube Data API key from [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
2. Set your API key as an environment variable named `YT_KEY` or replace the placeholder in the script directly.

## Usage

Run the script and enter the YouTube channel URL when prompted:

```bash
python youtube_channel_fetcher.py
```

Example channel URL formats supported:

- https://www.youtube.com/@channelhandle
- https://www.youtube.com/c/customname
- https://www.youtube.com/channel/CHANNELID

The script will fetch all videos, extract statistics, and save to `yt_channel_data.csv`.

## How It Works

- Parses the YouTube channel URL to detect handle, custom URL, or channel ID.
- Converts handle to channel ID using YouTube Data API search.
- Fetches video IDs using the channel's video list endpoint.
- Retrieves detailed statistics for videos in batches of 50.
- Calculates engagement metrics as percentage of views.
- Outputs data as a CSV file for further analysis.

## Notes

- The YouTube Data API has quota limits. Excessive requests may lead to temporary blocking.
- Video like counts or comments might be disabled on some videos, presenting as zero.
- The script converts ISO 8601 video duration format to seconds.

## License

MIT License — free for personal and educational use.

***

---

<div align="center"><sub>Built by <a href="https://github.com/Mokshitsharma">Mokshit Sharma</a> · <a href="https://mokshitsharma27.vercel.app/">Portfolio</a> · <a href="https://www.linkedin.com/in/mokshit-sharma-75b5ab305">LinkedIn</a></sub></div>
