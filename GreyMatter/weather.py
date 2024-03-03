import requests
import xml.etree.ElementTree as ET

# URL of the XML data with filter included
url = "https://geo.weather.gc.ca/geomet?service=WFS&version=1.1.0&request=GetFeature&typename=CURRENT_CONDITIONS&filter=<Filter><PropertyIsEqualTo><PropertyName>name</PropertyName><Literal>Ottawa%20%28Richmond%20-%20Metcalfe%29</Literal></PropertyIsEqualTo></Filter>"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML content
    root = ET.fromstring(response.content)

    # Find and print weather condition for Ottawa
    for member in root.findall('.//{http://www.opengis.net/gml}featureMember'):
        condition_en = member.find('.//{urn:x-msc-smc:md:weather-meteo}cond_en').text

        # Print weather condition
        print("Weather Condition (English):", condition_en)
        break  # Only print the first condition found
else:
    print("Failed to retrieve weather data.")
