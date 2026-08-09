import asyncio
import re
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import quote_plus
from xml.etree import ElementTree

import httpx

TOPICS = {
    "broad-market": "stock market Wall Street indexes when:1d",
    "macro-rates": "Federal Reserve inflation interest rates bonds stocks when:1d",
    "technology": "technology stocks semiconductors AI when:1d",
    "energy-materials": "energy oil gas mining stocks when:1d",
    "financials": "banks financial stocks credit markets when:1d",
    "healthcare": "healthcare biotech pharmaceutical stocks when:1d",
    "consumer": "consumer retail travel stocks when:1d",
    "corporate-events": "earnings mergers acquisitions IPO stocks when:1d",
}
DRIVERS = {
    "monetary-policy": ("fed", "rate cut", "rate hike", "interest rate", "powell", "treasury"),
    "inflation-growth": ("inflation", "cpi", "ppi", "jobs", "payroll", "gdp", "recession"),
    "earnings-guidance": ("earnings", "revenue", "profit", "guidance", "forecast", "quarter"),
    "technology-ai": ("artificial intelligence", " ai ", "chip", "semiconductor", "nvidia"),
    "commodities-energy": ("oil", "crude", "opec", "gold", "copper", "natural gas"),
    "geopolitics-trade": ("tariff", "trade war", "sanction", "war", "geopolit", "china"),
    "deals-capital-markets": ("acquisition", "merger", "ipo", "buyout", "offering"),
}


def parse_rss(xml: str, topic: str) -> list[dict[str, Any]]:
    root = ElementTree.fromstring(xml)
    articles: list[dict[str, Any]] = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        published = _date(item.findtext("pubDate"))
        source_node = item.find("source")
        publisher = (source_node.text or "").strip() if source_node is not None else "Unknown"
        if title and link and published:
            articles.append({
                "title": title,
                "publisher": publisher,
                "url": link,
                "publishedAt": published.isoformat(),
                "topic": topic,
            })
    return articles


async def fetch_market_news(lookback_hours: int = 24, max_articles: int = 80) -> dict[str, Any]:
    now = datetime.now(UTC)
    cutoff = now - timedelta(hours=max(1, min(72, lookback_hours)))
    async with httpx.AsyncClient(
        timeout=15,
        follow_redirects=True,
        headers={"User-Agent": "investment-wizard/1.0 market-research digest"},
    ) as client:
        results = await asyncio.gather(
            *(_fetch_topic(client, topic, query) for topic, query in TOPICS.items()),
            return_exceptions=True,
        )
    failures: list[str] = []
    articles: list[dict[str, Any]] = []
    for topic, result in zip(TOPICS, results, strict=True):
        if isinstance(result, Exception):
            failures.append(topic)
        else:
            articles.extend(article for article in result if _date(article["publishedAt"]) >= cutoff)
    deduplicated = _deduplicate(articles)[: max(10, min(200, max_articles))]
    drivers = [
        {
            "driver": driver,
            "headlineCount": len(matches),
            "examples": [article["title"] for article in matches[:3]],
        }
        for driver, keywords in DRIVERS.items()
        if (matches := [article for article in deduplicated if _matches(article["title"], keywords)])
    ]
    topic_counts = {
        topic: sum(article["topic"] == topic for article in deduplicated) for topic in TOPICS
    }
    return {
        "asOf": now.isoformat(),
        "lookbackHours": lookback_hours,
        "articleCount": len(deduplicated),
        "topicCoverage": topic_counts,
        "likelyDrivers": sorted(drivers, key=lambda item: item["headlineCount"], reverse=True),
        "headlines": deduplicated,
        "failedTopics": failures,
        "source": "Google News RSS aggregation",
        "summaryInstructions": (
            "Synthesize the dominant market moves and why they may be happening. Distinguish "
            "facts stated in headlines from causal inference, mention conflicting narratives, "
            "include publisher links, and state that coverage is broad but not exhaustive."
        ),
        "disclaimer": "News aggregation for research only; not investment advice.",
    }


async def _fetch_topic(
    client: httpx.AsyncClient, topic: str, query: str
) -> list[dict[str, Any]]:
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
    response = await client.get(url)
    response.raise_for_status()
    return parse_rss(response.text, topic)


def _deduplicate(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for article in sorted(articles, key=lambda item: item["publishedAt"], reverse=True):
        key = re.sub(r"[^a-z0-9 ]", "", article["title"].lower())
        key = re.sub(r"\s+", " ", key).strip()
        if key not in seen:
            seen.add(key)
            unique.append(article)
    return unique


def _matches(title: str, keywords: tuple[str, ...]) -> bool:
    normalized = f" {title.lower()} "
    return any(keyword in normalized for keyword in keywords)


def _date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value) if "," in value else datetime.fromisoformat(value)
        return parsed.astimezone(UTC) if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    except (TypeError, ValueError):
        return None
