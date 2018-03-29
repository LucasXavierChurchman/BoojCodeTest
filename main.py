"""
Lucas Churchman

Booj Data Code Test

3.27.18
"""

import xml.etree.ElementTree as ET
import urllib2
import time
import os
import glob

#These should be the only ones needed to be installed via pip
import pandas as pd
import numpy as np

def downloadXML(url):
    '''
    Downloads contents from the url and saves them in a local XML file
    '''

    #Read the file from the url
    file = urllib2.urlopen(url)

    #Create an object of the file's contents and save it
    contents = file.read()
    with open('listings.xml', 'wb') as f:
        f.write(contents)
        f.close()


def parseTree(xmlfile):
    '''
    Parse the tree and create the table from the XML file
    '''

    #Create tree object
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    data = []
    datacolumns = ['MlsId', 'MlsName', 'DateListed', 'Price', 'StreetAddress', 'Bedrooms', 'FullBathrooms', 'HalfBathrooms', 'Appliances', 'Rooms', 'Description']

    #Iterate through each listing
    for listing in root.findall('Listing'):

        #Initialize an object to hold the info for each listing
        info = []

        #Each of the following for loops are written so it's apparent how new columns can be added

        #this for loop gathers MlsId, MlsName, DateListed, and Price info needed from ListingDetails
        for listingDetails in listing.findall('ListingDetails'):
            MlsId = listingDetails.find('MlsId').text
            info.append(MlsId)
            MlsName = listingDetails.find('MlsName').text
            info.append(MlsName)
            DateListed = listingDetails.find('DateListed').text
            info.append(DateListed)
            Price = listingDetails.find('Price').text
            info.append(Price)

        #Gets street address info from Location
        for location in listing.findall('Location'):
            StreetAddress = location.find('StreetAddress').text
            info.append(StreetAddress)

        #Gets bathroom, bedroom, and description info from BasicDetails
        for basicDetails in listing.findall('BasicDetails'):
            Bedrooms = basicDetails.find('Bedrooms').text
            info.append(Bedrooms)
            FullBathrooms = basicDetails.find('FullBathrooms').text
            info.append(FullBathrooms)
            HalfBathrooms = basicDetails.find('HalfBathrooms').text
            info.append(HalfBathrooms)
            Description = basicDetails.find('Description').text
            Description = Description[0:199]

        #Generates a list of appliances for each listing
        for richDetails in listing.findall('RichDetails'):
            applianceList = []
            for child in richDetails.findall('Appliances'):
                for appliance in child.findall('Appliance'):
                    applianceList.append(appliance.text)
            applianceString = ', '.join(applianceList)
            info.append(applianceString)

        # Generates a list of rooms for each listing
        for richDetails in listing.findall('RichDetails'):
            roomList = []
            for child in richDetails.findall('Rooms'):
                for room in child.findall('Room'):
                    roomList.append(room.text)
            roomString = ', '.join(roomList)
            info.append(roomString)

        info.append(Description) #appending Description last to keep columns in better order

        #Append the row into the data list
        data.append(info)

    #Turn our data list into a pandas dataframe
    df = pd.DataFrame(data, columns = datacolumns)
    return(df)

def cleanData(df, query_year):
    '''Cleans the dataframe according to specifications'''

    #Contains only properties listed from *query_year* [DateListed]
    df['DateListed'] = df['DateListed'].astype('datetime64[ns]')     # Convert DateListed into a datetime type
    df = df[(df['DateListed'].dt.year == query_year)]

    #Contains only properties that contain the word "and" in the Description field
    df = df[df['Description'].str.contains('and')]

    #CSV ordered by DateListed
    df.sort_values(by = 'DateListed', ascending = False)

    #Convert the FullBathroom and HalfBathroom columns to floats and calculate the total number of bathrooms from them
    #Any 'Nones' in the field get converted to 0
    df['FullBathrooms'] = np.array(df['FullBathrooms'], dtype = np.float)
    df['HalfBathrooms'] = np.array(df['HalfBathrooms'], dtype=np.float)
    df['FullBathrooms'].fillna(0, inplace = True)
    df['HalfBathrooms'].fillna(0, inplace = True)
    df['TotalBathrooms'] = df['FullBathrooms'] + 0.5*df['HalfBathrooms']

    #Reorder the columns to match better with the list on the assignment description
    cols = ['MlsId','MlsName','DateListed','StreetAddress','Price','Bedrooms','TotalBathrooms','FullBathrooms','HalfBathrooms',
                'Appliances','Rooms','Description']
    df = df[cols]

    print(df.head())
    return(df)

def saveCSV(df):
    '''Deletes old CSV files and saves new one'''

    #Delete old CSV(s)
    filelist = glob.glob(os.path.join('*.csv'))
    for f in filelist:
        os.remove(f)

    # Generate a timestamp to be used in CSV file name to indicate when it was last updated
    now = time.strftime("%Y-%m-%d %H_%M_%S")

    #Save the csv
    filename = 'listings_{}.csv'.format(now)
    df.to_csv(filename)

if __name__ == "__main__":
    downloadXML(url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
    df = parseTree(xmlfile = 'listings.xml')
    df = cleanData(df = df, query_year = 2016)
    saveCSV(df = df)


