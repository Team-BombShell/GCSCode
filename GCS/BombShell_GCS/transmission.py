from serial.serialutil import SerialException

from xbee import XBee               #Xbee module

def read_data(data):
    '''
    The Xbee module calls this method whenever it receives
    data. It then sends the data as a single argument to
    this method.
    '''

    #Data-in (measured) variables
    global missionTime, softwareState,tiltX,tiltY,tiltZ,altitude,pressure,temp,voltage,teamID,packetCount,\
           GPSTime,GPSLat,GPSLong,GPSSats,GPSAlt

    #Derived Variables
    global packetsDropped,packetReceivedRate

    #lol. keeping track of packetsDropped is futile because the XBee will just throw it away if the data
    #   is wrong.

    try:
        #If I read the Docs correctly, this should append all of the data to their respective variables
        #Otherwise, this will break horribly
        teamID.append(data["dio-0"])
        missionTime.append(data["dio-1"])
        packetCount.append(data["dio-2"])
        altitude.append(data["dio-3"])
        pressure.append(data["dio-4"])
        temp.append(data["dio-5"])
        voltage.append(data["dio-6"])
        GPSTime.append(data["dio-7"])
        GPSLat.append(data["dio-8"])
        GPSLong.append(data["dio-9"])
        GPSAlt.append(data["dio-10"])
        GPSSats.append(data["dio-11"])
        tiltX.append(data["dio-12"])
        tiltY.append(data["dio-13"])
        tiltZ.append(data["dio-14"])
        softwareState.append(data["dio-15"])
        app.update()
        packetsDropped.append(packetsDropped[-1])
    except KeyError:
        #If one of the keys is missing, this probably means something is very wrong on the probe side
        warnings.warn("Data Frame improperly received this tick.")
        packetsDropped.append(1+packetsDropped[-1]) #cumulative packets dropped
    
