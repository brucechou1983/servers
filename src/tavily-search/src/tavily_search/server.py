import os
import json
import logging
from datetime import datetime
from typing import Any, Sequence

import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tavily-search")

# API configuration
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY environment variable required")

API_BASE_URL = "https://api.tavily.com"

# Create the server
app = Server("tavily-search")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available search tools."""
    return [
        Tool(
            name="tavily_web_search",
            description="Performs a web search using Tavily Search API. Ideal for general queries, news, articles and online content. "
            "Use this for broad information gathering, recent events, or when you need diverse web sources.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "search_depth": {
                        "type": "string",
                        "description": "Search depth - basic or advanced",
                        "enum": ["basic", "advanced"],
                        "default": "basic"
                    },
                    "include_images": {
                        "type": "boolean",
                        "description": "Include image results",
                        "default": False
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for search."""
    if name != "tavily_web_search":
        raise ValueError(f"Unknown tool: {name}")

    if not isinstance(arguments, dict) or "query" not in arguments:
        raise ValueError("Invalid search arguments")

    query = arguments["query"]
    search_depth = arguments.get("search_depth", "basic")
    include_images = arguments.get("include_images", False)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": search_depth,
                    "include_answer": False,
                    "include_images": include_images,
                    "include_image_descriptions": include_images,
                    "include_raw_content": False,
                    "max_results": 5
                }
            )
            response.raise_for_status()
            data = response.json()

        # Format results with all available fields
        results = []
        for result in data.get("results", []):
            result_data = {
                "title": result.get("title"),
                "content": result.get("content"),
                "url": result.get("url"),
                "score": result.get("score"),
                "published_date": result.get("published_date")
            }

            # Add image data if included
            if include_images and "image" in result:
                result_data["image"] = {
                    "url": result["image"].get("url"),
                    "description": result["image"].get("description")
                }

            results.append(result_data)

        return [
            TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )
        ]
    except httpx.HTTPError as e:
        logger.error(f"Tavily API error: {str(e)}")
        raise RuntimeError(f"Tavily API error: {str(e)}")


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
