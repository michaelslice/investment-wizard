from investment_wizard_mcp.news import parse_rss


def test_parse_rss() -> None:
    xml = """<rss><channel><item><title>Stocks rise after inflation report</title>
    <link>https://example.com/story</link><pubDate>Sun, 09 Aug 2026 15:00:00 GMT</pubDate>
    <source>Example News</source></item></channel></rss>"""
    articles = parse_rss(xml, "broad-market")
    assert articles[0]["publisher"] == "Example News"
    assert articles[0]["topic"] == "broad-market"
