import urllib.request
import xml.etree.ElementTree as ET
import board
import neopixel

COLOR_VFR = (50,0,0)
COLOR_MVFR = (0,0,50)
COLOR_IFR = (0,50,0)
COLOR_LIFR = (0,25,25)
COLOR_ERROR = (20,20,20)

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
			color = COLOR_VFR
		elif flightCategory == "MVFR":
			color = COLOR_MVFR
		elif flightCategory == "IFR":
			color = COLOR_IFR
		elif flightCategory == "LIFR":
			color = COLOR_LIFR
		else:
			color = COLOR_ERROR

	pixels[i] = color
	print ("" + airportCode + ": " + conditionDict[airportCode])






