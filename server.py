from fastmcp import FastMCP
import httpx

mcp = FastMCP("FarmOS")

@mcp.tool()
def get_weather(lat: float, lon: float, days: int) -> dict:
    """Get weather forecast for a location using Open-Meteo free API."""
    response = httpx.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&forecast_days={days}")
    return response.json()
@mcp.tool()
def get_pest_alerts(crop: str, state: str) -> dict:
    """Get common pest alerts for a crop in a US state."""
    pest_data = {
        "tomato": ["Tomato hornworm", "Whiteflies", "Spider mites", "Aphids", "Early blight"],
        "apple": ["Apple scab", "Codling moth", "Fire blight", "Aphids"],
        "blueberry": ["Spotted wing drosophila", "Mummyberry", "Blueberry maggot"],
        "strawberry": ["Botrytis gray mold", "Spider mites", "Aphids", "Root weevils"],
        "corn": ["Corn earworm", "European corn borer", "Rootworm", "Gray leaf spot"]
    }
    
    alerts = pest_data.get(crop.lower(), ["No specific pest data available for this crop"])
    
    return {
        "crop": crop,
        "state": state,
        "common_pests": alerts,
        "recommendation": f"Monitor your {crop} plants in {state} for these common pests"
    }
if __name__ == "__main__":
    mcp.run()