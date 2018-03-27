"""
Lucas Churchman

3.27.18
"""

import xml.etree.ElementTree as ET
import urllib2
import datetime
from lxml import etree


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

    tree = etree.XML(contents)

def parseTree(xmlfile):

    tree = etree.parse(xmlfile)

    MlsId = tree.xpath('//MlsId/text()')
    MlsName = tree.xpath('//MlsName/text()')
    DateListed = tree.xpath('//DateListed/text()')
    StreeAddresse = tree.xpath('//StreetAddress/text()')
    Price = tree.xpath('//Price/text()')
    Bedrooms = tree.xpath('//Bedrooms/text()')
    Bathrooms = tree.xpath('//Bathrooms/text()')



if __name__ == "__main__":
    downloadXML()
    parseTree('listings.xml')


#
# def parseTree(xmlfile):
#
#     #Create tree from XML. Get root of element.
#     tree = ET.parse(xmlfile)
#     root = tree.getroot()
#
#     #create empty list for our listings
#     MyListings = []
#
#     for listing in root.findall('Listing'):
#
#         details = {}
#         for infoCategory in listing:
#             print infoCategory.tag
#
#
#
#     MyListings.append(details)
#
#     print(MyListings)
#
# if __name__ == "__main__":
#     downloadXML()
#     parseTree('listings.xml')
#
#
