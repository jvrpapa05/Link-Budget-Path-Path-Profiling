from IPython import get_ipython
import numpy
import math
import tkinter as tk
import json
import webbrowser as web
import urllib
import webbrowser
import matplotlib.pyplot as plt
from haversine import haversine

elevationArray = []
latitudeArray = []
longitudeArray = []
mapToAxis = []
distance1 = []
distance2 = []
totalDistance = []
earthCurvature = []
fresnel_fifty_array = []
fresnel_sixty_array = []
curvature_elevation_array = []
fresnel_zone_array = []
fresnel_fifty_above = []
fresnel_fifty_below = []
LOS_array = []

get_ipython().run_line_magic('matplotlib', 'qt')

def Map(x, in_min, in_max, out_min, out_max):
  return abs((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
  
#Earth Curvature
def height(d1, d2, constant, k):
    h = (d1*d2)/(constant*k)
    return h

#Freznel
def fresnel(d1, d2, f):
   calc = 17.31 * math.sqrt((d1*d2/((d1+d2)*f)))
   return calc

    
def find(Lat1, Lon1, Lat2, Lon2, datasets, f_ghz):
    print()
    print('Point A:')
    print('Latitude:', Lat1)
    print('Longitude:', Lon1)
    
    print()
    print('Point B:')
    print('Latitude:', Lat2)
    print('Latitude:', Lon2)
    
    samples = datasets + 1 #THIS IS VERY IMPORTANT, to give offset on "0" value at starting point.
    
    url = ('https://maps.googleapis.com/maps/api/elevation/json?path=' + str(Lat1) + ',' + str(Lon1) + '|' + str(Lat2) + ',' + str(Lon2) + '&samples=' + str(samples) + '&key=' + str(apiKey.get()))
    
    print()
    print(url)
    
    
    #Request Data to Google Cloud
    #web.open_new_tab(url)
    request = urllib.request.urlopen(url)
    results = json.load(request).get('results')
    
    
    #Calculate the distance between Point A and Point B
    distanceBetween = haversine((Lat1 , Lon1) , (Lat2 , Lon2))
    datapointEveryKM = (float(distanceBetween)/len(results))
    print()
    print('Distance between A and B:' , distanceBetween , 'km')
    print('Elevation datapoint at every', datapointEveryKM , 'km')
    
    
    print('\n')
    
    #Create/Calculate Distance 1 based on Mapping Function
    i = 0
    while(i < len(results)):
        data = Map(i, 0, float(1 - len(results)), 0, float(distanceBetween))
        distance1.append(data)
        print()
        print('Distance 1:' , distance1[i])
        i = i + 1

   
    #Create/Calculate Distance 2 based on Mapping Function
    for i in reversed(distance1):
        distance2.append(i)
        
    
    print('\n')
     
    #Print values of Distance 2 and Calculate the Total Distance
    i = 0
    while(i < len(results)):
        totalDistance.append(distance1[i] + distance2[i])
        print()
        print('Distance 2:' , distance2[i])
        i = i + 1
        
    
    
    
    print('\n')
    
    #Calculate Earth Curvature, constants are based on provided lectures
    i = 0
    while(i < len(results)):
        earthCurvature.append(height(distance1[i] , distance2[i] , 12.75 , 4/3))
        print()
        print('Earth Curvature:', earthCurvature[i])
        i = i + 1

 
    print('\n')

    
    #Store and Print datas on the Excel/Monitor
    i = 0
    while(i < len(results)):
        extractElevation = results[i].get('elevation')
        getLoc = results[i].get('location')
        extractLat = getLoc['lat']
        extractLon = getLoc['lng']
        
        elevationArray.append(extractElevation)
        latitudeArray.append(extractLat)
        longitudeArray.append(extractLon)
        
        #Earth Curvature + Elevation
        curvature_elevation = earthCurvature[i] + extractElevation
        curvature_elevation_array.append(curvature_elevation)
        
        #Fresnel Zone
        fresnel_zone = fresnel(distance1[i], distance2[i], f_ghz)
        fresnel_zone_array.append(fresnel_zone)
        
        #Fresnel Zone @ 50 Percent
        fresnel_fiftyPercent = fresnel_zone*0.5
        fresnel_fifty_array.append(fresnel_fiftyPercent)
        
        #Fresnel Zone @ 60 Percent
        fresnel_sixtyPercent = fresnel_zone*0.6
        fresnel_sixty_array.append(fresnel_sixtyPercent)

        
        print()
        print('Data' , i, 'from' , len(results) - 1, ':')
        print('Latitude' , extractLat)
        print('Longitude' , extractLon)
        print('Elevation' , extractElevation)
        i = i + 1
          
        
    # printing the maximum element in fresnel 60 percent
    highest_fresnel = max(fresnel_sixty_array)
    print("Largest element in FRESNEL is:", highest_fresnel) 
    
    #printing the maximum element in Elevation and Curvature
    highest_elevationAndCurvature = max(curvature_elevation_array)
    print("Largest element in Earth Curvature and Elevation is", highest_elevationAndCurvature)
    
    #printing Line of Sight
    LOS = highest_elevationAndCurvature + highest_fresnel
    print("Line of Sight", LOS) 
    
    #printing Antenna RX and TX height
    TX_height = LOS - elevationArray[0]                  #Elevation @ point A
    RX_height = LOS - elevationArray[int(rate.get())]    #Elevation @ point B
    print('TX Antenna Height', TX_height)
    print('RX Antenna Height', RX_height)
    
    #printing Free Space Loss
    frequency_distance = (float(frequencyGet.get())) * (float(distanceBetween))
    freeSpaceLoss = 92.45 + 20 * math.log(frequency_distance,10)
    print('Free Space Loss', freeSpaceLoss)
    
    #printing Received Signal Level
    receivedSignalLevel =  (float(txOutputEntry.get()) + float(txGainEntry.get()) + float(rxGainEntry.get())) - (float(txWaveguideLossEntry.get()) + float(freeSpaceLoss) + float(rxWaveguideLossEntry.get()))
    print('Received Signal Level', receivedSignalLevel)
    
    
    #printing Angular Distance
    angularDistance = float(distanceBetween) / 111.12
    print('Angular Distance', angularDistance)
    
    #printing Azimuth
    azimuth = math.asin(math.sin(180-Lat1)*math.sin(abs(Lon1-Lon2))/math.sin(angularDistance))
    print('Azimuth', azimuth)
    

    #Create a unique filename
    filename = (str(Lat1) + '-' + str(Lat2) + '.csv')
    file = open(filename, "w")
    
    file.write('Powered By:' + ',,,' + 'Google Cloud Platform' + '\n')
    file.write('Project API funded by:' + ',,,' + 'Innotech Philippines - sponsor@innotechphils.com' + '\n')
    file.write('Data are automatically generated and calculated.' + '\n')
    file.write('\n')
    file.write('Point A,,,,,Point B\n')
    file.write('Latitude:' + ',,' + str(Lat1) + ',,,' + 'Latitude:' + ',,' + str(Lat2) + '\n')
    file.write('Longtiude:' + ',,' + str(Lon1) + ',,,' + 'Longitude:' + ',,' + str(Lon2) + '\n')
    file.write('\n')
    file.write('Total Distance (km): ' + ',,,,' +  str(distanceBetween) + '\n')
    file.write('Elevations are available every (km): ' + ',,,,' + str(datapointEveryKM) + ' \n')
    file.write('No. of datapoints: ' + ',,,,' + str(len(results)))
    
    file.write('\n\n')
    
    file.write('\nAntenna Specifications\n')
    file.write('\nTransmitter,,,,,Receiver\n')
    file.write('TX Output (dBm): ' + ',,,' + str(txOutputEntry.get()) + '\n')
    file.write('TX Waveguide Loss (dBm): ' + ',,,' + str(txWaveguideLossEntry.get()) + ',,' + 'RX Waveguide Loss (dBm): ' + ',,,' + str(rxWaveguideLossEntry.get()) + '\n')
    file.write('TX Gain (dBi): ' + ',,,' + str(txGainEntry.get()) + ',,' + 'RX Gain (dBi): ' + ',,,' + str(rxGainEntry.get()) +  '\n')
    
    file.write('\n\n')
    
    file.write('Line of Sight: ' + ',,,' + str(LOS) + '\n')
    file.write('TX Height: ' + ',,,' + str(TX_height) + '\n')
    file.write('RX Height: ' + ',,,' + str(RX_height) + '\n')
    file.write('Free Space Loss: ' + ',,,' + str(freeSpaceLoss) + '\n')
    file.write('Received Signal Level' + ',,,' + str(receivedSignalLevel) + '\n')
    
    file.write('\n\n')
    
    file.write('Angular Distance' + ',,,' + str(angularDistance) + '\n')
    file.write('Azimuth' + ',,,' + str(azimuth) + '\n')
    
    file.write('\n\n')
            
    file.write('LATITUDE,LONGITUDE,DISTANCE 1,DISTANCE 2,TOTAL DISTANCE, EARTH CURVATURE, ELEVATION, ELEVATION AND CURVATURE, Fresnel Zone, 50%FZ (m), 60% FZ (m), Line of Sight (m), LOS+50%Fz (m), LOS-50%FZ  (m)  \n')
    

    #Store and Print datas on the Excel/Monitor
    i = 0
    while(i < len(results)):
        #Fresnel Zone @ 50 Percent Above
        fresnel_fifty_above.append(LOS + fresnel_fifty_array[i])
        
        #Fresnel Zone @ 50 Percent Below
        fresnel_fifty_below.append(LOS - fresnel_fifty_array[i])
        
        #LOS Array
        LOS_array.append(LOS)
        
        file.write(str(latitudeArray[i]) + ','
                   + str(longitudeArray[i]) + ','
                   + str(distance1[i]) + ','
                   + str(distance2[i]) + ',' 
                   + str(totalDistance[i]) + ',' 
                   + str(earthCurvature[i]) + ','
                   + str(elevationArray[i]) + ','
                   + str(curvature_elevation_array[i]) + ','
                   + str(fresnel_zone_array[i]) + ','
                   + str(fresnel_fifty_array[i]) + ','
                   + str(fresnel_sixty_array[i]) + ','
                   + str(LOS) + ','
                   + str(fresnel_fifty_above[i]) + ','
                   + str(fresnel_fifty_above[i]) + ','
                   + '\n')
        
        i = i + 1
        
    file.close()
    
    
    print('\n')

    
    #Calculate each distant depedent to setpoint and replace X-Axis by the value of each distant.
    i = 0
    elevationEveryKM = 0
    while(i < len(results)):
        elevationEveryKM = elevationEveryKM + datapointEveryKM
        mapToAxis.append(elevationEveryKM)
        print()
        print('Data' , i, 'from' , len(results) - 1, ':')
        print('At Distance of' , elevationEveryKM) 
        print('Elevation is', elevationArray[i])
        i = i + 1
    
    print('\n')
    
    #Show data visualization on the Screen
    plt.title("Line of Sight Terrain Elevation", loc="left")
    plt.ylabel("Height in Meters")
    plt.xlabel("Point A to B; Range in Meters")
    
    plt.fill_between(mapToAxis, curvature_elevation_array , color="skyblue", alpha = 0.4)
    plt.plot(mapToAxis, curvature_elevation_array , color="Slateblue", alpha = 0.6)
    
    plt.plot(mapToAxis, LOS_array , color="red", alpha = 0.6)
    plt.plot(mapToAxis, fresnel_fifty_above , color="red", alpha = 0.6)
    plt.plot(mapToAxis, fresnel_fifty_below , color="red", alpha = 0.6)
    
    plt.grid();
    plt.show()
    
    
    print()
    print('Done!')
    root.quit()
    root.destroy()


def calculate():
    print()
    print('Calculating...')
    fLat1 = float(lat1.get())
    fLon1 = float(lon1.get())
    fLat2 = float(lat2.get())
    fLon2 = float(lon2.get())
    iRate = int(rate.get())
    freq_ghz = int(frequencyGet.get())
    find(fLat1, fLon1, fLat2, fLon2, iRate, freq_ghz)

root = tk.Tk()

root.title('Path Profiling and Link Budget')

apiLabel = tk.Label(root, text='<-- API Key')
apiKey = tk.Entry(width = 58, show="*")
apiKey.grid(row=0, column=0, columnspan=3)
apiLabel.grid(row=0,column=3, sticky='w')

pathProfiling = tk.Label(root, text = '\nDATA INPUTS FOR PATH PROFILING\n')
pathProfiling.grid(row=1, column=0, columnspan = 2, sticky='e')

pointA = tk.Label(root, text = "POINT A:")
aLatLabel = tk.Label(root, text = 'TX Latitude')
aLonLabel = tk.Label(root, text = 'TX Longitude')
lat1 = tk.Entry()
lon1 = tk.Entry()
pointA.grid(row=2, column=1)
lat1.grid(row=3, column=1)
lon1.grid(row=4, column=1)
aLatLabel.grid(row=3, column=0, sticky='e')
aLonLabel.grid(row=4, column=0, sticky='e')

pointB = tk.Label(text = "POINT B:")
bLatLabel = tk.Label(root, text = 'RX Latitude')
bLonLabel = tk.Label(root, text = 'RX Longitude')
lat2 = tk.Entry()
lon2 = tk.Entry()
pointB.grid(row=5, column=1)
lat2.grid(row=6, column=1)
lon2.grid(row=7, column=1)
bLatLabel.grid(row=6, column=0, sticky='e')
bLonLabel.grid(row=7, column=0, sticky='e')


sampleRate = tk.Label(root, text = "No. datapoints")
rate = tk.Entry()
sampleRate.grid(row=9, column=0, sticky='e')
rate.grid(row=9, column=1)

frequency = tk.Label(root, text = "Frequency (GHz)")
frequencyGet = tk.Entry()
frequency.grid(row=10, column=0, sticky='e')
frequencyGet.grid(row=10, column=1)

#Inputs for Antenna Specs
antennaSpecifications = tk.Label(root, text = "\nDATA INPUTS FOR LINK BUDGET\n")
antennaSpecifications.grid(row=1, column=2, columnspan = 2, sticky='e')

#Input for Transmitter Output Power in dBm
txOutputLabel = tk.Label(root, text = 'TX Output (dBm)')
txOutputLabel.grid(row=3, column=2, sticky='e')
txOutputEntry = tk.Entry()
txOutputEntry.grid(row=3, column=3)

#Input for Transmitter Waveguide Loss in dBm
txWaveguideLossLabel = tk.Label(root, text = 'TX Waveguide Loss (dBm)')
txWaveguideLossLabel.grid(row=4, column=2, sticky='e')
txWaveguideLossEntry = tk.Entry()
txWaveguideLossEntry.grid(row=4, column=3)

#Input for Transmitter Antenna Gain in dBi
txGainLabel = tk.Label(root, text = 'TX Antenna Gain (dBi)')
txGainLabel.grid(row=5, column=2, sticky='e')
txGainEntry = tk.Entry()
txGainEntry.grid(row=5, column=3)

#Input for Receiver Output power in dBm
rxWaveguideLossLabel = tk.Label(root, text = 'RX Waveguide Loss (dBm)')
rxWaveguideLossLabel.grid(row=7, column=2, sticky='e')
rxWaveguideLossEntry = tk.Entry()
rxWaveguideLossEntry.grid(row=7, column=3)

#Input for Receiver Antenna Gain in dBi
rxGainLabel = tk.Label(root, text = 'RX Antenna Gain (dBi)')
rxGainLabel.grid(row=8, column=2, sticky='e')
rxGainEntry = tk.Entry()
rxGainEntry.grid(row=8, column=3)


button = tk.Button(root,
                  text = "CALCULATE",
                  width = 80,
                  height = 0,
                  bg = "blue",
                  fg = "yellow",
                  command = calculate)
button.grid(row=11, column=0, columnspan=4)

greeting = tk.Label(root, text = '\n Created By: \n John Vince R. Papa \n Rica Joy Serquiña \n Kevin C. Banila')
sponsor = tk.Label(root, text = 'Powered by Google Cloud Platform \n Project API funded by Innotech Philippines \n sponsor@innotechphils.com')
greeting.grid(row=12, column=0, columnspan = 2)
sponsor.grid(row=12, column=2, columnspan = 2)

root.resizable(False,False)
root.mainloop()