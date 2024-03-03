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
url = "https://geo.weather.gc.ca/geomet?service=WFS&version=1.1.0&request=GetFeature&typename=CURRENT_CONDITIONS&filter=<Filter><PropertyIsEqualTo><PropertyName>name</PropertyName><Literal>Ottawa%20%28Richmond%20-%20Metcalfe%29</Literal></PropertyIsEqualTo></Filter>"
# Call the function to scrape weather data
scrape_weather_data(url)
