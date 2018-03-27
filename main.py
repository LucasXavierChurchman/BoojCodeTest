"""
Lucas Churchman

3.27.18
"""

import xml.etree.ElementTree as ET
import urllib2

def downloadXML():
    '''
    Downloads contents from the url and saves them in a local XML file
    '''

    #Read the file from the url
    url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    file = urllib2.urlopen(url)

    #Create an object of the file's contents and save it
    contents = file.read()
    with open('listings.xml', 'wb') as f:
        f.write(contents)
        f.close()

def parseTree(xmlfile):

    #Create tree from XML. Get root of element.
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    #create empty list for our listings
    MyListings = []

    #Pulls all relevant data from ListingDetails branch
    for ListingDetails in root.findall('./Listing/ListingDetails'):

        details = {}

        for child in ListingDetails:
            if child.tag == 'MlsId':
                details['MlsId'] = child.text
            if child.tag == 'MlsName':
                details['MlsName'] = child.text
        print(details)
        MyListings.append(details)

    print(MyListings)

if __name__ == "__main__":
    # downloadXML()
    parseTree('listings.xml')


