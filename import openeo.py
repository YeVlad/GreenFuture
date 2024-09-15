import openeo
import ee

startTime = "2020-01-01"
endTime =  "2020-05-14"

arabia_spatial_extent={"west": 10, "south": 10, "east": 80, "north": 40}
world_spatial_extent={"west": -170, "south": -70, "east": 170, "north": 70}
berlin_spatial_extent={"west": 13.2, "south": 52.4, "east": 13.7, "north": 52.7}
london_spatial_extent={"west": 0.9, "south": 51.75, "east":  1.1, "north": 51.83}
globalCoord = london_spatial_extent
x=True

def getDataMeanTime(mapid,filename,connection_s,band_t,coords):
    connection = openeo.connect(connection_s).authenticate_oidc()
    # Load data cube from TERRASCOPE_S2_NDVI_V2 collection.
    cube = connection.load_collection(
        mapid,
        coords,
        temporal_extent=[startTime, endTime],
        bands=[band_t],
    )
    # Rescale digital number to physical values and take temporal maximum.
    #cube = cube.mean_time()

    cube.download(filename)
    return cube

def getDataMaxTime(mapid,filename,connection_s,band_t,coords):
    connection = openeo.connect(connection_s).authenticate_oidc()
    # Load data cube from TERRASCOPE_S2_NDVI_V2 collection.
    cube = connection.load_collection(
        mapid,
        coords,
        temporal_extent=[startTime, endTime],
        bands=[band_t],
    )
    # Rescale digital number to physical values and take temporal maximum.
    cube = cube.apply(lambda x: 0.004*x-0.08).max_time()

    cube.download(filename)
    return cube
#getData("SENTINEL2_L2A","7.png","openeo.dataspace.copernicus.eu/openeo/1.2","WVP",berlin_spatial_extent)

def createNewPrefab():
    print("Input the coodinates:")
    print("The most western point:")
    west = input()
    print("The most northern point:")
    north = input()
    print("The most eastern point:")
    east = input()
    print("The most southern point:")
    south = input()
    coords = {"west": west, "south": south, "east": east, "north": north}
    return coords

def seletPrefCoords():
    print("Enter a number to select region to monitor:\n 1 - Berlin \n 2 - Arabia")
    key = input()
    match key:
        case "1":
            return {"west": 13.2, "south": 52.4, "east": 13.7, "north": 52.7}
        case "2":
            return {"west": 10, "south": 10, "east": 80, "north": 40}
        case _:
            print("invalid input")
            return seletPrefCoords()



def selectStartTime():
    print("Enter the starting date in this format: YYYY-MM-DD ")
    startTime = input()
    return startTime

def selectEndTime():
    print("Enter the end date in this format: YYYY-MM-DD ")
    endTime = input()
    return endTime


while x==True :
    print("Enter a number to :\n 1 - Select a region; \n 2 - Set the timeframe;\n 3 - Compile the results; \n 4 - exit")
    key = input()
    match key:
        case "1":
            globalCoord = seletPrefCoords()
        case "2":
            startTime = selectStartTime() 
            endTime = selectEndTime()
        case "3":
            mask = getDataMaxTime("VEGETATION_PHENOLOGY_AND_PRODUCTIVITY_PARAMETERS_SEASON_1","london.tiff","https://openeo.sentinel-hub.com/production","EOSD",globalCoord)
            #map = getDataMaxTime("TERRASCOPE_S2_NDVI_V2","map.tiff","https://openeocloud.vito.be","NDVI_10M",globalCoord)
        case "4":
            x=False
