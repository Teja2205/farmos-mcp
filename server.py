from fastmcp import FastMCP
import httpx

mcp = FastMCP("FarmOS")

@mcp.tool()
def get_weather(lat: float, lon: float, days: int) -> dict:
    response = httpx.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&forecast_days={days}")
    return response.json()

if __name__ == "__main__":
    mcp.run()