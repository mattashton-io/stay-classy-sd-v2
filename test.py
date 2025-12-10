from fastmcp import FastMCP
import requests
from google.cloud import secretmanager

mcp = FastMCP("test_mcp")

def get_api_key():
    """Fetch the Google Maps API key from Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    # Using the project ID from app.py
    name = "projects/396631018769/secrets/stay-classy-sd-v2-weather/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

@mcp.tool("test_func")
def test_func():
    """Returns my favorite number"""
    return 4

@mcp.tool("get_weather")
def get_weather(location: str):
    """Query the weather for a specific location using Google Maps Weather API (Air Quality)"""
    try:
        api_key = get_api_key()
        
        # 1. Geocode the location to get lat/lng
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        geo_resp = requests.get(geocode_url).json()
        
        if geo_resp['status'] != 'OK':
            return f"Geocoding error: {geo_resp.get('status')}"
            
        if not geo_resp['results']:
            return "Location not found"
            
        lat = geo_resp['results'][0]['geometry']['location']['lat']
        lng = geo_resp['results'][0]['geometry']['location']['lng']
        formatted_address = geo_resp['results'][0]['formatted_address']
        
        # 2. Query Air Quality API as a proxy for 'Weather' in this context
        aq_url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
        payload = {
            "location": {
                "latitude": lat,
                "longitude": lng
            }
        }
        
        headers = {"Content-Type": "application/json"}
        weather_resp = requests.post(aq_url, json=payload, headers=headers).json()
        
        return {
            "location": formatted_address,
            "coordinates": {"lat": lat, "lng": lng},
            "air_quality_data": weather_resp
        }
        
    except Exception as e:
        return f"Error querying weather data: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="http")
