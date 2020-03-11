import urllib.request
import xml.etree.ElementTree as ET
import board
import neopixel
import time

COLOR_VFR = (50,0,0)
COLOR_MVFR = (0,0,50)
COLOR_IFR = (0,50,0)
COLOR_LIFR = (0,50,50)
COLOR_ERROR = (20,20,20)

REFRESH_RATE = 10 #seconds

with open("airports.txt") as f:
	airports = f.readlines()
airports = [x.strip() for x in airports]
print(airports)

# Retrieve METAR from aviationweather.gov data server
# Details about parameters can be found here: https://www.aviationweather.gov/dataserver/example?datatype=metar
url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=5&mostRecentForEachStation=true&stationString=" + ",".join([item for item in airports if item != "NULL"])
print(url)

while (True):

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
		if conditionDict[airportCode] != "No":
			if conditionDict[airportCode] == "VFR":
				color = COLOR_VFR
			elif conditionDict[airportCode] == "MVFR":
				color = COLOR_MVFR
			elif conditionDict[airportCode] == "IFR":
				color = COLOR_IFR
			elif conditionDict[airportCode] == "LIFR":
				color = COLOR_LIFR
			else:
				color = COLOR_ERROR

		pixels[i] = color
		print ("updated")
		print ("" + airportCode + ": " + conditionDict[airportCode] + ", " + flightCategory)

	time.sleep(REFRESH_RATE)






