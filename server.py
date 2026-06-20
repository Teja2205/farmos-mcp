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
    
@mcp.tool()
def get_soil_data(lat: float, lon: float)-> dict:
    """ Get common soil data for the crop in us state """
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}&property=phh2o&property=soc&depth=0-5cm&value=mean"
    soil_data =  httpx.get(url , timeout=60.0)
    return soil_data.json()

@mcp.tool()
@mcp.tool()
def get_field_context(lat: float, lon: float, crop: str, state: str) -> dict:
    """Bundle weather, pest alerts, and soil data into one field context."""
    weather_data = get_weather(lat, lon, days=7)
    pests_data = get_pest_alerts(crop, state)
    
    try:
        soildata = get_soil_data(lat, lon)
    except Exception:
        soildata = {"soil_status": "unavailable"}
    
    return weather_data | pests_data | soildata
if __name__ == "__main__":
    mcp.run()