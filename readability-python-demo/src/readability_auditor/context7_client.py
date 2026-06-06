"""Context7 API client for fetching library documentation."""

import os
import httpx
from typing import Optional
from urllib.parse import urlparse

from . import logger


CONTEXT7_API_BASE = "https://context7.com/api/v2"


def _get_api_token() -> Optional[str]:
    """Get Context7 API token from environment."""
    return os.environ.get("CONTEXT7_TOKEN")


def _extract_library_name(url: str) -> str:
    """Extract library name from URL for Context7 search."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    
    # Common mappings
    mappings = {
        "fastapi.tiangolo.com": "fastapi",
        "docs.pydantic.dev": "pydantic",
        "langchain.com": "langchain",
        "vercel.com": "vercel/next.js",
        "developers.cloudflare.com": "cloudflare",
        "stripe.com": "stripe",
        "docs.github.com": "github",
        "supabase.com": "supabase",
        "docs.cursor.com": "cursor",
        "hono.dev": "honojs/hono",
    }
    
    return mappings.get(domain, domain.split(".")[0])


async def search_library(library_name: str, query: str, token: str) -> Optional[str]:
    """Search for a library in Context7 and return its ID.
    
    Uses GET /v2/libs/search endpoint with libraryName and query parameters.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{CONTEXT7_API_BASE}/libs/search",
                params={
                    "libraryName": library_name,
                    "query": query,
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    best_match = results[0]
                    library_id = best_match.get("id")
                    title = best_match.get("title", "Unknown")
                    logger.console.print(f"  [cyan]Found library: {title} ({library_id})[/cyan]")
                    return library_id
        except httpx.RequestError as e:
            logger.console.print(f"  [yellow]Context7 search error: {e}[/yellow]")
    
    return None


async def fetch_context(library_id: str, query: str, token: str) -> Optional[str]:
    """Fetch documentation context from Context7 API."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(
                f"{CONTEXT7_API_BASE}/context",
                params={
                    "libraryId": library_id,
                    "query": query,
                    "type": "txt",
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            
            if response.status_code == 200:
                return response.text
        except httpx.RequestError:
            pass
    
    return None


async def get_llm_text_via_context7(base_url: str) -> Optional[str]:
    """
    Fetch machine-optimized documentation via Context7 API.
    
    This is used as a fallback when llms.txt is not found directly on the URL.
    Uses the official GET /v2/libs/search endpoint.
    """
    token = _get_api_token()
    if not token:
        logger.console.print("[yellow]CONTEXT7_TOKEN not set, skipping Context7 fallback[/yellow]")
        return None
    
    library_name = _extract_library_name(base_url)
    
    # Search for the library using libraryName and query
    library_id = await search_library(
        library_name=library_name,
        query="full documentation for library",
        token=token,
    )
    
    if not library_id:
        logger.console.print(f"[yellow]Library not found in Context7: {library_name}[/yellow]")
        return None
    
    # Fetch full documentation context
    context = await fetch_context(library_id, "full documentation", token)
    if context and len(context.strip()) > 100:
        logger.console.print(f"[green]Fetched {len(context):,} chars from Context7[/green]")
        return context
    
    return None
