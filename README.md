# Link-Budget-and-Path-Profiling

We highly suggest to run the code on Spyder, Python version 3.7.
In order for the code to function properly, the lists of libraries must fully installed correctly:
## Library Dependencies
1. IPython
2. numpy
3. math
4. tkinter
5. json
6. webbrowser
7. urllib
8. webbrowser
9. matplotlib
10. haversine

Aside from these 10 library dependencies, the user must PROVIDE a Google Cloud Platform's Elevation API.
Learn more on @: [Google Elevation API](https://developers.google.com/maps/documentation/elevation/start)

![Interface](https://github.com/papa1560868/Link-Budget-and-Path-Profiling/blob/main/image/Interface.PNG)

## How to use the python script:
### Path Profiling
1. **API KEY** - This is where the user needed to place the generated API Elevation from GCP.
2. **TX Latitude** - Transmitters Latitude, must be in Decimal Degrees (DD) and *not* in Degrees Minutes and Seconds (DMS).
3. **TX Longitude** - Transmitters Longitude, must be in Decimal Degrees (DD) and *not* in Degrees Minutes and Seconds (DMS).
4. **RX Latitude** - Receivers Latitude, must be in Decimal Degrees (DD) and *not* in Degrees Minutes and Seconds (DMS).
5. **RX Longitude** - Receivers Longitude, must be in Decimal Degrees (DD) and *not* in Degrees Minutes and Seconds (DMS).
6. **No. of datapoints** - This sets how many samples the system is going to get, rule of thumb the higher the sample rate the better the resolution is.
7. **Frequency (GHz)** - Operational frequency of the transmitting and receiving signal.
#### Link Budget
8. **TX Output (dBm)** - Transmitters maximum output power.
9. **TX Waveguide Loss (dBm)** - Transmitters physical wire waveguide loss.
10. **TX Antenna Gain (dBi)** - Transmitters rated gain.
11. **RX Waveguide Loss (dBm)** - Receivers physical wire waveguide loss.
12. **TX Antenna Gain (dBi)** - Receivers rated gain.

*Note: These data are provided by the user, for link budget we highly suggest tinkering with Andrews Catalog*


# Example
Here's the example of valid input datas.

![Interface](https://github.com/papa1560868/Link-Budget-and-Path-Profiling/blob/main/image/Example.PNG)


The Python code has the capability of creating the *Elevation and Earth Curvature*, including the *Freznel Zone* and *Line of Sight graph*.


## Example of generated graph
![Interface](https://github.com/papa1560868/Link-Budget-and-Path-Profiling/blob/main/image/ExampleGraph.PNG)
The user can save the photo as well at .png format.


# Generated Excel File
The system will then save the data on the same file location folder where the python script is executed, the filename of the excel file is in this format:
**TX_Latitude-TX_Longitude.csv**
![ExcelFilename](https://github.com/papa1560868/Link-Budget-and-Path-Profiling/blob/main/image/ExcelFilename.PNG)


## Excel File Preview
Please take note that the generated excel type is "Microsoft Excel Comma Separated Values File(.csv)" and we highly suggest to change it to "Microsoft Excel Worksheet(.xlxs)" to save any equation you might want to add to the file. 
![ExcelPreview](https://github.com/papa1560868/Link-Budget-and-Path-Profiling/blob/main/image/ExcelPreview.PNG)



# Disclaimer
The developer is not liable to any false information you might encounter by using the python script.


# Acknowlodgement 
The developer, John Vince Papa wants to acknowledge **Innotech Engineering Services PH** for sponsoring the API for this project.
Learn more @ [Innotech Philippines!](http://www.innotechphils.com/)
