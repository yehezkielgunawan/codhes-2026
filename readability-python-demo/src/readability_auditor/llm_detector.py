"""Detect and fetch llm.txt or llms.txt from a domain."""

import re
import httpx
from typing import Optional, Tuple, List
from urllib.parse import urljoin

from . import logger


async def detect_llm_txt(
    base_url: str, timeout: float = 10.0, follow_links: bool = True
) -> Tuple[Optional[str], Optional[str]]:
    """
    Check if domain has llm.txt or llms.txt.
    
    If follow_links is True, also fetches linked .txt files and combines content.

    Returns:
        Tuple of (content, file_type) or (None, None) if not found.
    """
    paths_to_check = ["/llm.txt", "/llms.txt"]

    async with httpx.AsyncClient(timeout=timeout) as client:
        for path in paths_to_check:
            target_url = urljoin(base_url, path)
            try:
                response = await client.get(target_url)
                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    if "text/plain" in content_type or target_url.endswith(".txt"):
                        logger.log_found(base_url, path.lstrip("/"))
                        main_content = response.text
                        
                        if follow_links:
                            combined_content = await _fetch_linked_txt_files(
                                client, base_url, main_content, target_url
                            )
                            return combined_content, path.lstrip("/")
                        
                        return main_content, path.lstrip("/")
            except httpx.RequestError:
                continue

    logger.log_not_found(base_url)
    return None, None


async def _fetch_linked_txt_files(
    client: httpx.AsyncClient,
    base_url: str,
    main_content: str,
    source_url: str,
) -> str:
    """
    Parse llm.txt content for links to other .txt files and fetch them.
    
    Returns combined content from main file and all linked .txt files.
    """
    all_content = [main_content]
    
    txt_links = _extract_txt_links(main_content, source_url)
    
    if txt_links:
        logger.console.print(f"  [dim]Found {len(txt_links)} linked .txt file(s)[/dim]")
        
        for link_url in txt_links:
            try:
                response = await client.get(link_url)
                if response.status_code == 200:
                    content = response.text
                    if content.strip():
                        all_content.append(content)
                        logger.console.print(f"  [dim]Fetched: {link_url}[/dim]")
            except httpx.RequestError:
                logger.console.print(f"  [yellow]Failed to fetch: {link_url}[/yellow]")
                continue
    
    return "\n\n".join(all_content)


def _extract_txt_links(content: str, source_url: str) -> List[str]:
    """
    Extract .txt file links from llm.txt content.
    
    Looks for markdown links like [text](url) or plain URLs ending in .txt
    """
    links = []
    
    md_link_pattern = r'\[([^\]]*)\]\(([^)]+\.txt)\)'
    for match in re.finditer(md_link_pattern, content, re.IGNORECASE):
        url = match.group(2)
        full_url = urljoin(source_url, url)
        if full_url not in links:
            links.append(full_url)
    
    url_pattern = r'(https?://[^\s<>"]+\.txt)'
    for match in re.finditer(url_pattern, content, re.IGNORECASE):
        url = match.group(1)
        if url not in links:
            links.append(url)
    
    return links
