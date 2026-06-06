"""Scrape human documentation using Crawl4AI."""

import asyncio
from typing import Optional
from urllib.parse import urljoin

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

from . import logger
from .text_cleaner import clean_human_documentation


async def scrape_human_documentation(
    base_url: str, max_depth: int = 2, max_pages: int = 10, timeout: float = 120.0
) -> Optional[str]:
    """
    Scrape human-readable documentation from a URL using deep crawling.

    Uses BFS strategy to crawl multiple pages starting from /docs or root.
    Returns combined clean markdown content from all pages.
    """
    doc_urls = [
        urljoin(base_url, "/docs"),
        urljoin(base_url, "/documentation"),
        base_url,
    ]

    strategy = BFSDeepCrawlStrategy(
        max_depth=max_depth,
        max_pages=max_pages,
        include_external=False,
    )
    config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler() as crawler:
        for doc_url in doc_urls:
            try:
                results = await asyncio.wait_for(
                    crawler.arun(url=doc_url, config=config),
                    timeout=timeout
                )

                if results and len(results) > 0:
                    all_content = []
                    for result in results:
                        if result.success and result.markdown:
                            content = result.markdown.fit_markdown or result.markdown.raw_markdown
                            if content and len(content.strip()) > 100:
                                all_content.append(content)

                    if all_content:
                        combined = "\n\n".join(all_content)
                        logger.log_scrape(doc_url, len(combined))
                        logger.console.print(f"  [dim]Crawled {len(results)} pages[/dim]")
                        
                        # Clean the content to extract only prose
                        cleaned = clean_human_documentation(combined)
                        logger.console.print(
                            f"  [dim]Cleaned: {len(combined):,} → {len(cleaned):,} chars "
                            f"({len(cleaned)/len(combined)*100:.1f}% retained)[/dim]"
                        )
                        return cleaned
            except asyncio.TimeoutError:
                continue
            except Exception:
                continue

    return None
