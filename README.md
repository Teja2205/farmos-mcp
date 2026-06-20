# FarmOS MCP 🌾

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.4-green)](https://gofastmcp.com)
[![MCP](https://img.shields.io/badge/MCP-compatible-orange)](https://modelcontextprotocol.io)

Machine-readable agriculture intelligence server. Exposes weather forecasts, pest alerts, and soil data as MCP tools — callable by any AI agent that speaks the Model Context Protocol.

---

## What it does

FarmOS MCP gives AI agents structured access to real-world farm data through 4 tools:

| Tool | Inputs | Returns |
|---|---|---|
| `get_weather` | lat, lon, days | 7-day temperature and precipitation forecast |
| `get_pest_alerts` | crop, state | Common pests and management recommendations |
| `get_soil_data` | lat, lon | Soil pH and organic carbon at 0-5cm depth |
| `get_field_context` | lat, lon, crop, state | All three bundled into one structured context |

---

## Architecture

```
AI Agent (Claude, LangChain, AgriMind)
      ↓ MCP protocol
FarmOS MCP Server
      ├── get_weather → Open-Meteo API (free, no key)
      ├── get_pest_alerts → Static crop pest database
      ├── get_soil_data → SoilGrids REST API (free)
      └── get_field_context → Bundles all three
```

---

## Setup

**1. Clone and install**
```bash
git clone https://github.com/Teja2205/farmos-mcp.git
cd farmos-mcp
uv venv && source .venv/bin/activate
uv pip install fastmcp httpx pydantic python-dotenv
```

**2. Run the server**
```bash
python server.py
```

---

## Connect to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "farmos": {
      "command": "/path/to/farmos-mcp/.venv/bin/python",
      "args": ["/path/to/farmos-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. Then ask:

```
Use farmos get_field_context for lat 41.8, lon -93.6, crop tomato, state Iowa
```

---

## Example Response

```json
{
  "daily": {
    "temperature_2m_max": [25.5, 24.1, 20.4],
    "precipitation_sum": [0.0, 3.5, 0.0]
  },
  "crop": "tomato",
  "state": "Iowa",
  "common_pests": ["Tomato hornworm", "Whiteflies", "Spider mites"],
  "recommendation": "Monitor your tomato plants in Iowa for these common pests",
  "properties": {
    "phh2o": {"mean": 6.4},
    "soc": {"mean": 21.5}
  }
}
```

---

## Data Sources

| Source | API | Cost |
|---|---|---|
| Weather | Open-Meteo | Free, no key |
| Soil | SoilGrids (ISRIC) | Free, no key |
| Pests | Built-in database | Free |

---

## Used By

- [AgriMind](https://github.com/Teja2205/AgriMind) — AI crop disease diagnosis service that calls `get_field_context` before every diagnosis

---

## Author

Built by Teja Guduguntla as part of an AI engineering portfolio targeting FAANG roles in 2026.