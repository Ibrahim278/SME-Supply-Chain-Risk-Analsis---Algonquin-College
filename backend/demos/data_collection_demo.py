#!/usr/bin/env python3
"""
Simple Data Collection Agent Demo

A standalone LangGraph demo that:
1. Takes a supplier URL
2. Scrapes corporate info and ESG data using Playwright
3. Uses LLM to process and summarize findings
4. Outputs a formatted report

Usage:
    python demos/data_collection_demo.py "https://example-supplier.com"
"""

import argparse
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import TypedDict
from urllib.parse import urljoin, urlparse

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from playwright.async_api import async_playwright


# ---------------------------------------------------------------------------
# State Definition
# ---------------------------------------------------------------------------
class CollectorState(TypedDict):
    supplier_url: str
    supplier_name: str
    corporate_info: dict
    esg_info: dict
    processed_summary: str
    errors: list[str]


# ---------------------------------------------------------------------------
# Playwright Scraping Functions
# ---------------------------------------------------------------------------
async def scrape_page(url: str, timeout: int = 30000) -> dict:
    """Scrape a single page and return its content."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="SME-DueDiligence-Bot/1.0 (Research Demo)"
        )
        page = await context.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=timeout)
            title = await page.title()
            # Get main text content
            text_content = await page.evaluate(
                """
                () => {
                    const body = document.body.cloneNode(true);
                    // Remove script and style elements
                    body.querySelectorAll('script, style, nav, footer, header').forEach(el => el.remove());
                    return body.innerText.substring(0, 10000);
                }
            """
            )
            # Get all links for ESG page discovery
            links = await page.evaluate(
                """
                () => Array.from(document.querySelectorAll('a[href]'))
                    .map(a => ({href: a.href, text: a.innerText.trim()}))
                    .filter(l => l.text.length > 0 && l.text.length < 100)
            """
            )

            return {
                "url": url,
                "title": title,
                "content": text_content,
                "links": links,
                "success": True,
            }
        except Exception as e:
            return {
                "url": url,
                "title": "",
                "content": "",
                "links": [],
                "success": False,
                "error": str(e),
            }
        finally:
            await browser.close()


def find_esg_links(links: list[dict], base_url: str) -> list[str]:
    """Find links that might lead to ESG/sustainability pages."""
    esg_keywords = [
        "sustainability",
        "sustainable",
        "esg",
        "environment",
        "environmental",
        "csr",
        "responsibility",
        "ethics",
        "governance",
        "modern slavery",
        "supply chain",
        "carbon",
        "climate",
        "social",
    ]

    esg_links = []
    seen = set()

    for link in links:
        href = link.get("href", "")
        text = link.get("text", "").lower()

        # Check if link text or URL contains ESG keywords
        matches_keyword = any(kw in text or kw in href.lower() for kw in esg_keywords)

        if matches_keyword and href not in seen:
            # Ensure it's a valid URL on the same domain
            parsed = urlparse(href)
            base_parsed = urlparse(base_url)
            if parsed.netloc == "" or parsed.netloc == base_parsed.netloc:
                full_url = urljoin(base_url, href)
                esg_links.append(full_url)
                seen.add(href)

    return esg_links[:3]  # Limit to 3 ESG pages


# ---------------------------------------------------------------------------
# Graph Nodes
# ---------------------------------------------------------------------------
async def collect_corporate(state: CollectorState) -> dict:
    """Node 1: Scrape main corporate information from supplier website."""
    print("\n[1/4] Collecting corporate information...")

    url = state["supplier_url"]
    result = await scrape_page(url)

    if not result["success"]:
        return {
            "corporate_info": {},
            "errors": state.get("errors", [])
            + [f"Failed to scrape {url}: {result.get('error', 'Unknown error')}"],
        }

    # Try to find About page
    about_links = [
        link["href"]
        for link in result.get("links", [])
        if "about" in link.get("text", "").lower()
        or "about" in link.get("href", "").lower()
    ]

    about_content = ""
    if about_links:
        about_result = await scrape_page(about_links[0])
        if about_result["success"]:
            about_content = about_result["content"]

    # Extract company name from title
    title = result.get("title", "")
    company_name = (
        title.split("|")[0].split("-")[0].strip() if title else urlparse(url).netloc
    )

    return {
        "supplier_name": company_name,
        "corporate_info": {
            "name": company_name,
            "website": url,
            "title": title,
            "main_page_content": result["content"][:3000],
            "about_page_content": about_content[:3000] if about_content else None,
            "scraped_at": datetime.now().isoformat(),
        },
    }


async def collect_esg(state: CollectorState) -> dict:
    """Node 2: Find and scrape ESG/sustainability pages."""
    print("[2/4] Collecting ESG information...")

    url = state["supplier_url"]

    # First, get links from homepage
    homepage = await scrape_page(url)
    if not homepage["success"]:
        return {
            "esg_info": {"found": False, "pages": []},
            "errors": state.get("errors", [])
            + ["Could not access homepage for ESG discovery"],
        }

    # Find ESG-related links
    esg_links = find_esg_links(homepage.get("links", []), url)

    if not esg_links:
        return {"esg_info": {"found": False, "pages": [], "note": "No ESG pages found"}}

    # Scrape ESG pages
    esg_pages = []
    for esg_url in esg_links:
        print(f"    Scraping ESG page: {esg_url}")
        result = await scrape_page(esg_url)
        if result["success"]:
            esg_pages.append(
                {
                    "url": esg_url,
                    "title": result["title"],
                    "content": result["content"][:3000],
                }
            )

    return {
        "esg_info": {
            "found": len(esg_pages) > 0,
            "pages_discovered": len(esg_links),
            "pages_scraped": len(esg_pages),
            "pages": esg_pages,
        }
    }


async def process_data(state: CollectorState) -> dict:
    """Node 3: Use LLM to process and summarize findings."""
    print("[3/4] Processing data with LLM...")

    # Check for API key - support OpenRouter or direct Anthropic/OpenAI
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if openrouter_key:
        # Use OpenRouter (OpenAI-compatible API)
        llm = ChatOpenAI(
            model=os.environ.get(
                "OPENROUTER_MODEL", "anthropic/claude-sonnet-4-20250514"
            ),
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
            temperature=0,
            max_tokens=1500,
        )
        print("    Using OpenRouter...")
    elif openai_key:
        # Use OpenAI directly
        llm = ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            api_key=openai_key,
            temperature=0,
            max_tokens=1500,
        )
        print("    Using OpenAI...")
    elif anthropic_key:
        # Use Anthropic via OpenRouter-style (or switch to langchain-anthropic if preferred)
        from langchain_anthropic import ChatAnthropic

        llm = ChatAnthropic(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            api_key=anthropic_key,
            temperature=0,
            max_tokens=1500,
        )
        print("    Using Anthropic...")
    else:
        return {
            "processed_summary": "[LLM processing skipped - No API key set. Set OPENROUTER_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY]",
            "errors": state.get("errors", []) + ["No LLM API key configured"],
        }

    # Build context from collected data
    corporate = state.get("corporate_info", {})
    esg = state.get("esg_info", {})

    context_parts = [f"Company: {corporate.get('name', 'Unknown')}"]

    if corporate.get("main_page_content"):
        context_parts.append(
            f"Main Page Content:\n{corporate['main_page_content'][:2000]}"
        )

    if corporate.get("about_page_content"):
        context_parts.append(
            f"About Page Content:\n{corporate['about_page_content'][:1500]}"
        )

    if esg.get("pages"):
        for page in esg["pages"]:
            context_parts.append(
                f"ESG Page ({page['title']}):\n{page['content'][:1500]}"
            )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""Analyze this supplier's publicly available information and provide a structured summary.

{context}

Provide a concise analysis covering:
1. COMPANY OVERVIEW: Brief description, industry, key business areas
2. ESG INDICATORS: Any sustainability initiatives, certifications, policies mentioned
3. RISK SIGNALS: Any potential red flags or areas requiring further investigation
4. DATA QUALITY: Assessment of how much relevant information was available

Keep the response focused and professional. If information is limited, note that clearly."""

    try:
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        return {"processed_summary": response.content}
    except Exception as e:
        return {
            "processed_summary": f"[LLM processing failed: {e}]",
            "errors": state.get("errors", []) + [f"LLM error: {e}"],
        }


def generate_output(state: CollectorState) -> dict:
    """Node 4: Format and display final report."""
    print("[4/4] Generating output...\n")

    corporate = state.get("corporate_info", {})
    esg = state.get("esg_info", {})
    summary = state.get("processed_summary", "")
    errors = state.get("errors", [])

    # Build report
    report = []
    report.append("=" * 60)
    report.append("       DATA COLLECTION AGENT - DEMO REPORT")
    report.append("=" * 60)
    report.append("")
    report.append(f"Supplier: {corporate.get('name', 'Unknown')}")
    report.append(f"URL: {state.get('supplier_url', 'N/A')}")
    report.append(f"Scraped: {corporate.get('scraped_at', 'N/A')}")
    report.append("")
    report.append("-" * 60)
    report.append("CORPORATE INFORMATION")
    report.append("-" * 60)
    report.append(f"Website Title: {corporate.get('title', 'N/A')}")
    report.append(
        f"About Page: {'Found' if corporate.get('about_page_content') else 'Not found'}"
    )
    report.append("")
    report.append("-" * 60)
    report.append("ESG INFORMATION")
    report.append("-" * 60)
    report.append(f"ESG Pages Found: {esg.get('found', False)}")
    report.append(f"Pages Discovered: {esg.get('pages_discovered', 0)}")
    report.append(f"Pages Scraped: {esg.get('pages_scraped', 0)}")

    if esg.get("pages"):
        report.append("\nESG Pages:")
        for page in esg["pages"]:
            report.append(f"  - {page['title']}: {page['url']}")

    report.append("")
    report.append("-" * 60)
    report.append("LLM ANALYSIS")
    report.append("-" * 60)
    report.append(summary if summary else "[No analysis available]")
    report.append("")

    if errors:
        report.append("-" * 60)
        report.append("ERRORS ENCOUNTERED")
        report.append("-" * 60)
        for error in errors:
            report.append(f"  - {error}")
        report.append("")

    report.append("=" * 60)

    output = "\n".join(report)
    print(output)

    return {}  # No state updates needed


# ---------------------------------------------------------------------------
# Graph Definition
# ---------------------------------------------------------------------------
def build_graph() -> StateGraph:
    """Build the data collection workflow graph."""
    builder = StateGraph(CollectorState)

    # Add nodes
    builder.add_node("collect_corporate", collect_corporate)
    builder.add_node("collect_esg", collect_esg)
    builder.add_node("process_data", process_data)
    builder.add_node("generate_output", generate_output)

    # Define flow: START -> collect_corporate -> collect_esg -> process_data -> generate_output -> END
    builder.add_edge(START, "collect_corporate")
    builder.add_edge("collect_corporate", "collect_esg")
    builder.add_edge("collect_esg", "process_data")
    builder.add_edge("process_data", "generate_output")
    builder.add_edge("generate_output", END)

    return builder.compile()


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
async def run_demo(url: str, output_file: str | None = None):
    """Run the data collection demo."""
    print("\n" + "=" * 60)
    print("     SME SUPPLY CHAIN - DATA COLLECTION AGENT DEMO")
    print("=" * 60)
    print(f"\nTarget URL: {url}")
    print("\nStarting workflow...")

    # Build and run graph
    graph = build_graph()

    initial_state: CollectorState = {
        "supplier_url": url,
        "supplier_name": "",
        "corporate_info": {},
        "esg_info": {},
        "processed_summary": "",
        "errors": [],
    }

    # Run the graph
    final_state = await graph.ainvoke(initial_state)

    # Save to file if requested
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare JSON-serializable output
        output_data = {
            "url": url,
            "supplier_name": final_state.get("supplier_name", ""),
            "corporate_info": final_state.get("corporate_info", {}),
            "esg_info": final_state.get("esg_info", {}),
            "summary": final_state.get("processed_summary", ""),
            "errors": final_state.get("errors", []),
            "generated_at": datetime.now().isoformat(),
        }

        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"\n[Results saved to: {output_path}]")

    return final_state


def main():
    parser = argparse.ArgumentParser(
        description="Data Collection Agent Demo - Scrape supplier info using LangGraph"
    )
    parser.add_argument("url", help="Supplier website URL to analyze")
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file path (optional)",
        default=None,
    )

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        args.url = "https://" + args.url

    # Run the demo
    asyncio.run(run_demo(args.url, args.output))


if __name__ == "__main__":
    main()
