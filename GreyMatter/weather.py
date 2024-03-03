import requests
import xml.etree.ElementTree as ET

def scrape_weather_data(url):
    # Send a GET request to the provided URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the XML content
        root = ET.fromstring(response.content)
        
        # Find the relevant weather data elements
        for member in root.findall('.//{urn:x-msc-smc:md:weather-meteo}CURRENT_CONDITIONS'):
            location = member.find('{urn:x-msc-smc:md:weather-meteo}name').text
            station_en = member.find('{urn:x-msc-smc:md:weather-meteo}station_en').text
            icon_url = member.find('{urn:x-msc-smc:md:weather-meteo}icon').text
            condition_en = member.find('{urn:x-msc-smc:md:weather-meteo}cond_en').text
            temperature = member.find('{urn:x-msc-smc:md:weather-meteo}temp').text
            dewpoint = member.find('{urn:x-msc-smc:md:weather-meteo}dewpoint').text
            windchill = member.find('{urn:x-msc-smc:md:weather-meteo}windchill').text
            pressure = member.find('{urn:x-msc-smc:md:weather-meteo}pres_en').text
            pressure_tendency = member.find('{urn:x-msc-smc:md:weather-meteo}prestnd_en').text
            humidity = member.find('{urn:x-msc-smc:md:weather-meteo}rel_hum').text
            wind_speed = member.find('{urn:x-msc-smc:md:weather-meteo}speed').text
            wind_direction = member.find('{urn:x-msc-smc:md:weather-meteo}direction').text
            timestamp = member.find('{urn:x-msc-smc:md:weather-meteo}timestamp').text
            url_en = member.find('{urn:x-msc-smc:md:weather-meteo}url_en').text
            
            # Print the extracted weather data
            print(f"Location: {location}")
            print(f"Weather Station: {station_en}")
            print(f"Icon URL: {icon_url}")
            print(f"Condition: {condition_en}")
            print(f"Temperature: {temperature} °C")
            print(f"Dewpoint: {dewpoint} °C")
            print(f"Wind Chill: {windchill} °C")
            print(f"Pressure: {pressure} kPa")
            print(f"Pressure Tendency: {pressure_tendency}")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} km/h")
            print(f"Wind Direction: {wind_direction}")
            print(f"Timestamp: {timestamp}")
            print(f"URL (English): {url_en}")
            print("-" * 50)
    else:
        print("Failed to retrieve weather data.")

# URL provided by ECCC for Ottawa weather data
url = "https://geo.weather.gc.ca/geomet?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=CURRENT_CONDITIONS&FILTER=%3CFilter%20xmlns=%22http://www.opengis.net/ogc%22%20xmlns:gml=%22http://www.opengis.net/gml%22%20xmlns:ogc=%22http://www.opengis.net/ogc%22%3E%3CPropertyIsEqualTo%3E%3CPropertyName%3ElocationName_en%3C/PropertyName%3E%3CLiteral%3EOttawa%3C/Literal%3E%3C/PropertyIsEqualTo%3E%3C/Filter%3E"

# Call the function to scrape weather data
scrape_weather_data(url)
