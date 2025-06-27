import random
import requests

# NewsAPI (requires API key)
NEWSAPI_KEY = "Y5407bb8bb38b433b8f9973bf024e2f61"

def fetch_newsapi_headlines(topic='general', max_results=10):
    url = f"https://newsapi.org/v2/top-headlines?category={topic}&language=en&pageSize={max_results}&apiKey={NEWSAPI_KEY}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            return [(a['title'], "newsapi", random.uniform(-1, 1), random.uniform(0, 1)) for a in articles]
    except Exception:
        pass
    return []

# Reddit via PRAW
import praw

REDDIT_CLIENT_ID = "YOUR_CLIENT_ID"
REDDIT_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDDIT_USER_AGENT = "PrometheusSim/0.1"

def fetch_reddit_headlines(subreddit="news", max_results=10):
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        headlines = []
        for submission in reddit.subreddit(subreddit).hot(limit=max_results):
            headlines.append((submission.title, "reddit", 0, 0.5))
        return headlines
    except Exception:
        return []

# Twitter/X via snscrape
try:
    import snscrape.modules.twitter as sntwitter
    HAS_SN = True
except ImportError:
    HAS_SN = False

def fetch_twitter_headlines(query="news", max_results=10):
    if not HAS_SN:
        return []
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_results:
            break
        tweets.append((tweet.content, "twitter", 0, 0.5))
    return tweets

# TikTok via TikTokApi
try:
    from TikTokApi import TikTokApi
    HAS_TT = True
except ImportError:
    HAS_TT = False

def fetch_tiktok_headlines(query="news", max_results=10):
    if not HAS_TT:
        return []
    api = TikTokApi()
    try:
        results = api.search.videos(query, count=max_results)
        headlines = []
        for video in results:
            headlines.append((video['desc'], "tiktok", 0, 0.5))
        return headlines
    except Exception:
        return []

# Demo fallback
def get_sample_headlines():
    return [
        ("Major earthquake strikes city", "demo", -0.8, 0.9),
        ("School opens new playground", "demo", 0.6, 0.4),
        ("Election results spark protests", "demo", -0.7, 0.7),
        ("Medical breakthrough in cancer treatment", "demo", 0.85, 0.8),
        ("Celebrity wins humanitarian award", "demo", 0.5, 0.3),
        ("Rumors of economic downturn", "demo", -0.6, 0.5),
        ("Community hosts festival", "demo", 0.3, 0.3)
    ]

def get_all_headlines(
    sources=("newsapi", "reddit", "twitter", "tiktok", "demo"),
    topic="news",
    max_results=10
):
    headlines = []
    if "newsapi" in sources:
        headlines.extend(fetch_newsapi_headlines(topic, max_results))
    if "reddit" in sources:
        headlines.extend(fetch_reddit_headlines(topic, max_results))
    if "twitter" in sources:
        headlines.extend(fetch_twitter_headlines(topic, max_results))
    if "tiktok" in sources:
        headlines.extend(fetch_tiktok_headlines(topic, max_results))
    if not headlines and "demo" in sources:
        headlines = get_sample_headlines()
    random.shuffle(headlines)
    return headlines[:max_results * len(sources)]

