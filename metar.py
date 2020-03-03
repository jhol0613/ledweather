import urllib.request
import xml.etree.ElementTree as ET
from colors import Colors
import board
import neopixel

with open("airports.txt") as f:
	airports = f.readlines()
airports = [x.strip() for x in airports]
print(airports)

# Retrieve METAR from aviationweather.gov data server
# Details about parameters can be found here: https://www.aviationweather.gov/dataserver/example?datatype=metar
url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=5&mostRecentForEachStation=true&stationString=" + ",".join([item for item in airports if item != "NULL"])
print(url)

content = urllib.request.urlopen(url).read()

# Retrieve flying conditions from the service response and store in a dictionary for each airport
root = ET.fromstring(content)
conditionDict = { "":"" }
for metar in root.iter('METAR'):
	stationId = metar.find('station_id').text
	if metar.find('flight_category') is None:
		print("Missing flight condition, skipping.")
		conditionDict[stationId] = "Error"
		#print("Missing flight condition for " + stationId)
		continue
	flightCategory = metar.find('flight_category').text
	conditionDict[stationId] = flightCategory
	#print("" + stationId + ": " + flightCategory)

pixels = neopixel.NeoPixel(board.D18, len(conditionDict))

for i, airportCode in enumerate(airports):
	if flightCategory != "No":
		if flightCategory == "VFR":
			color = Colors.VFR
		elif flightCategory == "MVFR":
			color = Colors.MVFR
		elif flightCategory == "IFR":
			color = Colors.IFR
		elif flightCategory == "LIFR":
			color = Colors.LIFR
		else:
			color = colors.ERROR

	pixels[i] = color
	print ("" + airportCode + ": " + conditionDict[airportCode])






