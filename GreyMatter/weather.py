from GreyMatter.SenseCells.tts_engine import tts

def weather():
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
            temperature = member.fine('.//{urn:x-msc-smc:md:weather-meteo}temp').text
            pressure = member.find('.//{urn:x-msc-smc:md:weather-meteo}pres_en').text
            pressure_tendency = member.find('.//{urn:x-msc-smc:md:weather-meteo}prestnd_en').text

            #Determine if pressure is rising, falling or steady
            pressure_tendency_str = "steady"
            if pressure_tendency == "falling":
                pressure_tendency_str = "falling"
            elif pressure_tendency == "rising":
                pressure_tendency = "rising"

            # create the weather_resulst string

            weather_result = f"Weather in Ottawa today: Condition is {condition_en}. Temperature is {temperature} degrees Celsius. Atmospheric pressure is {pressure} kilopascals and {pressure_tendency_str}."
            return weather_result
    else:
        tts("Failed to retrieve weather data.")
        return("Failed to retrieve weather data.")

    tts(weather_result)

if __name__ == "__main__":
    weather()
