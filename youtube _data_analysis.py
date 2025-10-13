import requests
import pandas as pd
import re
import os

API_KEY = os.getenv("YT_KEY", "AIzaSyDTa1rH8KuX9s3BbX30pyHaRCW9xefV7eE")

def duration_to_sec(d):
    # convert PTxxHxxMxxS → seconds
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d)
    if not m: return 0
    h, mnt, s = m.groups()
    return int(h or 0) * 3600 + int(mnt or 0) * 60 + int(s or 0)

def extract_channel(url):
    if "youtube.com/@" in url:
        return url.split("@")[1], "handle"
    elif "/c/" in url:
        return url.split("/c/")[1], "custom"
    elif "/channel/" in url:
        return url.split("/channel/")[1], "id"
    else:
        raise Exception("Channel URL not recognised")

def handle_to_id(handle):
    api = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=@{handle}&type=channel&key={API_KEY}"
    r = requests.get(api).json()
    if "items" in r and r["items"]:
        return r["items"][0]["snippet"]["channelId"]
    else:
        raise Exception("Handle not found")

def fetch_videos(cid):
    vids = []
    base = f"https://www.googleapis.com/youtube/v3/search?part=id&channelId={cid}&maxResults=50&type=video&key={API_KEY}"
    nextpg = base
    while nextpg:
        res = requests.get(nextpg).json()
        if "items" not in res: break
        vids += [v["id"]["videoId"] for v in res["items"] if "id" in v]
        nxt = res.get("nextPageToken")
        nextpg = f"{base}&pageToken={nxt}" if nxt else None
    return vids

def fetch_details(vids):
    data = []
    for i in range(0, len(vids), 50):
        chunk = ",".join(vids[i:i+50])
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={chunk}&key={API_KEY}"
        res = requests.get(url).json()
        for v in res.get("items", []):
            stats, snip, cont = v.get("statistics", {}), v.get("snippet", {}), v.get("contentDetails", {})
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            cmts = int(stats.get("commentCount", 0))
            sec = duration_to_sec(cont.get("duration", "PT0S"))

            like_rate = round((likes/views*100) if views else 0, 2)
            cmt_rate  = round((cmts/views*100) if views else 0, 2)
            engage    = round(((likes+cmts)/views*100) if views else 0, 2)

            data.append({
                "VideoID": v["id"],
                "Title": snip.get("title"),
                "Published": snip.get("publishedAt"),
                "Views": views,
                "Likes": likes,
                "Comments": cmts,
                "DurationSec": sec,
                "LikeRate%": like_rate,
                "CommentRate%": cmt_rate,
                "Engagement%": engage
            })
    return data

if __name__ == "__main__":
    url = input("Enter YouTube channel link: ").strip()
    cid, t = extract_channel(url)
    if t == "handle":
        cid = handle_to_id(cid)

    print("Fetching video list...")
    vids = fetch_videos(cid)
    print(f"Total videos found: {len(vids)}")

    details = fetch_details(vids)
    if not details:
        print("No details found.")
    else:
        df = pd.DataFrame(details)
        df.to_csv("yt_channel_data.csv", index=False)
        print("Saved as yt_channel_data.csv")
