# BoojCodeTest
data developer test code

-Flexible enough to run on any XML file with the same format/structure

-The 'listings.xml' file is re-downloaded each time the script is ran rather than reading it directly from the webpage

-I'm not sure if I'm filling the 'Rooms' column with what's wanted. Let me know and I can make a change.

-Since the Bathroom field was empty for all of the listings, I made a new 'Total Bathrooms' column calculated from the 'FullBathrooms' and 'HalfBathrooms' columns
-You can specify which year of listings you want to look at with an argument in my cleanData() method for added modularity

-Checks for 'and' in description field after shortening to 200 characters

-CSV saved with timestamp in file name
