# Tavily Search MCP Server

An MCP server implementation that integrates the Tavily Search API, providing AI-optimized search results with high relevance and rich content.

## Features

- **AI-Powered Search**: Get highly relevant results optimized by Tavily's AI algorithms
- **Flexible Search Depth**: Choose between basic and advanced search modes
- **Rich Content**: Support for images with descriptions
- **Customizable Results**: Control result count and content types
- **Smart Filtering**: Include or exclude specific domains

## Tools

- **tavily_web_search**
  - Execute web searches with customizable depth and options
  - Inputs:
    - `query` (string): Search terms (max 400 chars, 50 words)
    - `search_depth` (string, optional): "basic" or "advanced" (default: "basic")
    - `include_images` (boolean, optional): Include image results with descriptions (default: false)

## Configuration

### Getting an API Key
1. Sign up at [app.tavily.com](https://app.tavily.com)
2. Generate your API key from the dashboard
3. Test your API in the [Playground](https://app.tavily.com/playground)

### Usage with Claude Desktop
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tavily-search": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/your/project",
        "run",
        "tavily-search"
      ],
      "env": {
        "TAVILY_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}