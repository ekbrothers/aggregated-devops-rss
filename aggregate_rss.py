import feedparser
import requests
from datetime import datetime
import pytz

# RSS feed URLs with their respective provider names for prefixing titles
feeds = {
    "https://github.com/hashicorp/terraform/releases.atom": "Terraform CLI",
    "https://github.com/hashicorp/terraform-provider-google/releases.atom": "GCP Provider",
    "https://github.com/hashicorp/terraform-provider-azurerm/releases.atom": "AzureRM Provider",
    "https://github.com/hashicorp/terraform-provider-aws/releases.atom": "AWS Provider",
    "https://github.com/hashicorp/vault/releases.atom": "Vault",
    "https://github.com/terraform-docs/terraform-docs/releases.atom": "terraform-docs",
}

entries = []

# Fetch and parse each feed
for feed_url, provider_name in feeds.items():
    response = requests.get(feed_url)
    feed = feedparser.parse(response.content)
    for entry in feed.entries:
        entry['provider_name'] = provider_name  # Add provider name to each entry
        entry.published_parsed = entry.get('published_parsed', entry.get('updated_parsed'))
        entries.append(entry)

# Sort entries by published date, using a default date if necessary
entries.sort(key=lambda entry: entry.published_parsed or datetime(1970, 1, 1, tzinfo=pytz.utc), reverse=True)

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<feed xmlns="http://www.w3.org/2005/Atom">\n')
    f.write('<title>Aggregated GitHub Releases</title>\n')
    f.write('<link href="https://example.com/feed.xml" rel="self"/>\n')
    f.write(f"<updated>{datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}</updated>\n")
    f.write('<author><name>Aggregated Feed</name></author>\n')
    f.write('<id>urn:uuid:aggregated-feed</id>\n')

    for entry in entries:
        provider_name = entry['provider_name']
        title = f"{provider_name} Release: {entry.title}"
        link = entry.link
        published = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%dT%H:%M:%SZ') if entry.published_parsed else 'No date available'
        summary = entry.summary if 'summary' in entry else 'No summary available'
        author = entry.author if 'author' in entry else 'No author available'
        
        f.write('<entry>\n')
        f.write(f"<title>{title}</title>\n")
        f.write(f"<link href='{link}'/>\n")
        f.write(f"<id>{entry.id}</id>\n")
        f.write(f"<updated>{published}</updated>\n")
        if summary:  # Only include summary if available
            f.write(f"<summary>{summary}</summary>\n")
        if author:  # Only include author if available
            f.write(f"<author><name>{author}</name></author>\n")
        f.write('</entry>\n')
    
    f.write('</feed>')
