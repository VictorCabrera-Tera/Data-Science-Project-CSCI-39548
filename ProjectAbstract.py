#Name: Victor Cabrera
#Email: victor.cabrera@stu.bmcc.cuny.ed
#Resources: https://en.wikipedia.org/wiki/Hurricane_Sandy for learning about one of the worst hurricanes that has hit NYC
#https://www1.nyc.gov/assets/em/html/know-your-zone/knowyourzone.html this is where I got my information about safe zones and high risk zones of storm surge
#https://data.cityofnewyork.us/Public-Safety/Hurricane-Evacuation-Centers/ayer-cga7 Hurricane shelter dataset
#https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49 subway station dataset for seeing which stations are close to shelters
#https://www.weather.gov/phi/FlashFloodingDefinition where I got some definitions
#https://www.youtube.com/watch?v=YxpjW-Mq96Q&t=68s tutorial for creating a website
#https://datatofish.com/bar-chart-python-matplotlib/ for creating a bar graph
#used program 45 collision maps from my 127 csci class
#also used programs from homework such as #14 and #24
#Title: Hurricane Shelters For NYC
#URL: https://victorcabrera9704.wixsite.com/website-1

import pandas as pd
import pandasql as psql #didn't really need it 
import re
import matplotlib.pyplot as plt
import matplotlib.style as style #didn't use it
import seaborn as sns
import folium

#Helper function for getting a boroughs name in the "CITY" column depending
#on the value passed from Borocode
#paramater:colname which will be a int object from column "BOROCODE"
#returns:the name of the borough as a string
def helper(Borocode):
    if Borocode == 1:
        return 'Manhattan'
    elif Borocode == 2:
        return 'Bronx'
    elif Borocode == 3:
        return 'Brooklyn'
    elif Borocode == 4:
        return 'Queens'
    else:
        return 'Staten Island'
    return 'Bronx' #default return value
   

#function for returning a df with the "CITY" columns filled 
#with only string values of the 5 boroughs
#paramater:df which is the original dataframe from dataset Hurricane_Evacuation_Centers.csv 
#returns:a dataframe with only borough names in "CITY" and columns "BIN" AND "BBL" dropped    
def CleaningDF(df):
    df["CITY"] = df["BOROCODE"].apply(helper)
    df = df.drop(["BIN","BBL"], axis = 1)  
    return df


#function for getting the count of shelters in each borough in order to use it for the barGraph() function
#parameter: colname to hold a panda series assuming to be column "CITY"
#return: a panda series of length 5 containing all 5 boroughs
def getCount(colname):
    #get a list of unique values from column "CITY" to get all 5 boroughs 
    unique_boroughs = colname.unique()

    #empty list for adding the counts of each borough
    count_b = []

    #traverse through the list of boroughs
    for i in unique_boroughs:
        #add elements to the original empty 
        count_b.append(colname.str.count(i).sum())
        
    return pd.Series(data = count_b)

#function for creating a bar graph from a dataframe of my dataset with hurricane sheters 
#parameter: df which is a dataframe assumed to have 2 columns of length of 5 called
#"COUNTS" and "Boroughs" respectively
#return: none since this is only a mutator function    
def barGraph(df):
    shelter_count = df["COUNTS"].head().astype(int) #head() is for getting the first 5 values since thats all we need 
    Boroughs = df["BOROUGHS"].head().astype(str)
    city_colors = ['blue','red','purple','yellow','green']
    plt.bar(Boroughs, shelter_count, color = city_colors)
    plt.title('Number of shelters vs boroughs')
    plt.xlabel('borough')
    plt.ylabel('number of shelters')
    plt.grid(True)
    plt.savefig('1bar.jpg')
    plt.show()

#function for extracting the latitude and longitude in string format
#from geo coordinates in the format of (lon,lat)
#parameter: colName in which we will pass the column "the_geom" which is a string obj
#return: a single float value of the latitude
def get_LatLon(colName):
    #using str.extract with a regex expression to find POINT(-lat,lon) and turn it into (lat lon)
    #then using str.replace() to format it into (lat, lon)
    colName = colName.str.extract('(-?[\d(.)]+[\d]+[\s]+[\d(.)]+\d)',expand= False).str.replace(' ',', ')

    return colName

#function for getting the latitude from geo coordinates in string format of (lon,lat) used in conjuction
#with Pd.series.apply()
#parameter: row in which we will pass the column returned from function get_LatLon()
#return: a single float value of the latitude  
def extractlat(row):
    #create list where values are split when ',' is found
    list_ = row.split(",")
    
    #change the list second element to float 
    lat = float(list_[1])

    return lat

#function for getting the longitude from geo coordinates in string format of (lon,lat) used in conjuction
#with Pd.series.apply()
#parameter: row in which we will pass the column returned from function get_LatLon()
#return: a single float value of the longitude  
def extractlon(row):
    list_ = row.split(",")
    
    lon = float(list_[0])
    #lat = float(list_[1])

    return lon
    

#function for showing a map of NYC with markers of where all the shelters are located 
#and to ouput said map as a html interactive map 
#parameter: a dataframe assuming it has columns named "LATITUDE","LONGITUDE" and "BLDG_NAME"
#return: no return statement but it does save a map in html format to your working directory
def ShelterMap(df):
    #load a folium map with geo coordinates of NYC
    mapShelter = folium.Map(location=[40.5405508, -74.1931974])

    #2d traversal of the dataframe for accessing the latitude and longitude
    for i,row in df.iterrows():
        lat = row["LATITUDE"]
        lon = row["LONGITUDE"]
        name = row["BLDG_NAME"]
        newMarker = folium.Marker([lat, lon], popup= name)
        newMarker.add_to(mapShelter)

    mapShelter.save('1ShelterMap.html')
    
#main driver function where I do some cleaning of my dataset and testing
#This is also where I call the functions for creating the bar graph and folium map visulizations
def main():
    
    User_Input = 'Hurricane_Evacuation_Centers.csv'
    User_Output = '1' + User_Input  
    File_Name = pd.read_csv(User_Input)


    CITY_expr = """
    SELECT CITY AS QUEENS
    FROM File_Name
    WHERE CITY != 'New York'
        AND CITY != 'Bronx'
        AND CITY != 'Brooklyn'
        AND CITY != 'Staten Island'    
    """
    #CITY = psql.sqldf(CITY_expr)
    #CITY.to_csv(User_Output,index= False)
    #print(CITY)
    df = CleaningDF(File_Name)
    df["COUNTS"] = getCount(df["CITY"])
    unique = df["CITY"].unique() #list of unique values (returns list with the 5 boroughs)
    df["BOROUGHS"] = pd.Series(data = unique) #create column called BOROUGHS with the list of boroughs

    df["LOCATION"] = df["the_geom"].str.extract('(-?[\d(.)]+[\d]+[\s]+[\d(.)]+\d)',expand= False).str.replace(' ',', ')
    df["LATITUDE"] = df["LOCATION"].apply(extractlat)
    df["LONGITUDE"] = df["LOCATION"].apply(extractlon)

    barGraph(df)
    ShelterMap(df)

    df.to_csv(User_Output,index= False)
    print(df)
    print(df.info())

if __name__ == "__main__":
    main()




