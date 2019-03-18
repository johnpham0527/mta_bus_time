#!/usr/bin/env python

#MTA Bus Time API
# This code accesses the MTA's Bus Time API to output a list of upcoming bus times, given a bus stop code

#Access (from http://bustime.mta.info/wiki/Developers/OneBusAwayRESTfulAPI)
#The root of the OBA API in the MTA Bus Time deployment is http://bustime.mta.info/api/where/ .  So, for example:
#    To get the list of and metadata for the agencies covered by MTA Bus Time, use: http://bustime.mta.info/api/where/agencies-with-coverage.xml?key=9a865f19-cb53-43b2-9452-78ae26403a1e
#    To get the list of and metadata for the MTA NYCT and MTABC routes covered by MTA Bus Time, use: http://bustime.mta.info/api/where/routes-for-agency/MTA%20NYCT.xml?key=9a865f19-cb53-43b2-9452-78ae26403a1e
#    For information on one specific stop served by MTA Bus Time, use: http://bustime.mta.info/api/where/stop/MTA_STOP-ID.xml?key=9a865f19-cb53-43b2-9452-78ae26403a1e
#    For information on the stops that serve a route, use http://bustime.mta.info/api/where/stops-for-route/MTA%20NYCT_M1.json?key=9a865f19-cb53-43b2-9452-78ae26403a1e&includePolylines=false&version=2
#    For information on stops near a location, use http://bustime.mta.info/api/where/stops-for-location.json?lat=40.748433&lon=-73.985656&latSpan=0.005&lonSpan=0.005&key=9a865f19-cb53-43b2-9452-78ae26403a1e

#Monitored Vehicle Journey Documentation: http://bustime.mta.info/wiki/Developers/SIRIMonitoredVehicleJourney
#   Predicted arrival and departure times are presented in ISO8601 format


#Bus Stop Monitoring
#http://bustime.mta.info/wiki/Developers/SIRIStopMonitoring

#Example links to JSON
#http://bustime.mta.info/api/siri/stop-monitoring.json?key=9a865f19-cb53-43b2-9452-78ae26403a1e&OperatorRef=MTA&MonitoringRef=308209&LineRef=MTA%20NYCT_B63
#http://bustime.mta.info/api/siri/stop-monitoring.json?key=9a865f19-cb53-43b2-9452-78ae26403a1e&OperatorRef=MTA&MonitoringRef=403367&LineRef=MTA%20NYCT_M86%2B

#TO-DO
# * implement a function to select the bus stop closest to where you are



#Before running, be sure to install python-dateutil:
#pip install python-dateutil
import requests
import json
import dateutil.parser as dateTimeParser

myLatitude = 40.778322
myLongitude = -73.945143
myBusStopCode = 403367 #This is the bus stop called "E 91 ST/YORK AV"
myAPIKey = "9a865f19-cb53-43b2-9452-78ae26403a1e" #This is my (John Pham's) API key

#build the URL string, given the parameters
getUrlBusStopMonitoring = "http://bustime.mta.info/api/siri/stop-monitoring.json"
parameters = {"key":myAPIKey, "OperatorRef":"MTA", "MonitoringRef":myBusStopCode} #parameters for the URL
requestResult = requests.get(getUrlBusStopMonitoring,params=parameters) #submit the GET request
resultText = requestResult.text #obtain the requested text
jsonText = json.loads(resultText) #convert the requested text to JSON format

print("Bus Stop: " + jsonText["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"][0]["MonitoredVehicleJourney"]["MonitoredCall"]["StopPointName"])

busesToMonitor = 3 #number of buses to monitor at the bus stop

for i in range (0, busesToMonitor): 
    arrivalTime = dateTimeParser.parse(jsonText["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"][i]["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"])
    stringArrivalTime = str(arrivalTime.time())

    #The MTA Bus Time API returns time in ISO 8601 format. I want to output the time in a more readable 12-hour format. 
    #This code strips out last 7 characters of the arrival time and saves only first 5 characters (HH:MM). It also assigns AM or PM to the time.
    formattedArrivalTime24Hr = ""
    AMorPM = "AM"
    for i in range(0, 5): 
        formattedArrivalTime24Hr += stringArrivalTime[i]
        if i == 1:
            integerTime = int(formattedArrivalTime24Hr)
            if integerTime > 12:
                AMorPM = "PM"
                integerTime -= 12
                formattedArrivalTime24Hr = str(integerTime)
    formattedArrivalTime24Hr += " " + AMorPM
    print("\tBus " + jsonText["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"][i]["MonitoredVehicleJourney"]["PublishedLineName"] + " will arrive at " + formattedArrivalTime24Hr)