import feedparser
import requests
from datetime import datetime
import pytz

# RSS feed URLs
feeds = [
    "https://github.com/hashicorp/terraform/releases.atom",
    "https://github.com/hashicorp/terraform-provider-google/releases.atom"
]

entries = []

# Fetch and parse each feed
for feed_url in feeds:
    response = requests.get(feed_url)
    feed = feedparser.parse(response.content)
    for entry in feed.entries:
        # Provide a default value or try alternative fields if 'published' is missing
        entry.published_parsed = entry.get('published_parsed', entry.get('updated_parsed'))
        entries.append(entry)

# Sort entries by published date, using a default date if necessary
entries.sort(key=lambda entry: entry.published_parsed or datetime(1970, 1, 1, tzinfo=pytz.utc), reverse=True)

# Generate aggregated RSS feed (simplified version)
print("<?xml version='1.0' encoding='UTF-8'?>")
print("<feed xmlns='http://www.w3.org/2005/Atom'>")
print("<title>Aggregated GitHub Releases</title>")
print(f"<updated>{datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}</updated>")
print("<author><name>Aggregated Feed</name></author>")
print("<id>urn:uuid:aggregated-feed</id>")

for entry in entries:
    # Use a fallback for title or link if necessary
    title = entry.get('title', 'No title available')
    link = entry.get('link', 'No link available')
    published = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%dT%H:%M:%SZ') if entry.published_parsed else 'No date available'
    print(f"<entry>")
    print(f"<title>{title}</title>")
    print(f"<link href='{link}'/>")
    print(f"<updated>{published}</updated>")
    print(f"<id>{entry.id}</id>")
    print(f"</entry>")

print("</feed>")
