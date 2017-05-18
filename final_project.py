#!/usr/bin/python
# Shebang line to avoid internal server error

# CS 108 Final Project 
# CS 108 Spring 2017 (Professor Stevens) 
# File: final_project.py
# Date: 4/24/2017 - 5/3/2017

# Description: The final project is a mini iTunes application with authentication functionality
# similar to that of miniFacebook, and the order confirmation similar to shipping.py but with an
# additional serialization feature of purchase code (confirmation code) and email receipt. The application
# will also enable to pre-fill values for the user and have a username / password authentication
# upon login. Finally, the user is able to manipulate, add, update, and also be able to order
# songs from the selection provided (first 5 by default), similar to that of a real iTunes website / application. 

# My SQL:
# instrument.db (instrid,instrument,type)
# songs.db(songid,year,name,artist,genre)
# vendor.db(songid,song,date,purchase,website)

# Helper function(s):
# debugFormData(form) from Assignment 23: miniFacebook4.py
# defPrintShippingForm() from Assignment 18 and 19: shipping.py and shipping2.py 

"""
This final project will take input of song attributes (song, year, name, artist, type, instrument) with HTML forms,
from the user, connect to the songs, instruments, and vendor databases, and then based on the input of the user,
give the user a final purchase total of the songs, an order confirmation form to finalize the purchase, plus an
email address to show that the user has purchased the songs with a serialized confirmation code. It will then
finally use cookies to maintain the session state. 

It is essentially a mini iTunes web application. 
"""

# import statements
# time import 
import time
# datetime import
import datetime
# CGI (Common Gateway Interface) import, for HTML forms 
import cgi
# importing cgi libraries 
import cgitb; cgitb.enable()
# importing for email address verification 
import smtplib
# MySQL database imports 
import MySQLdb as db

# additional cookie imports as well
import os
import Cookie

# printing the HTTP headers
print "Content-Type: text/html"
print # blank line 

#################################################################################
## Function 1 ## 
"Function 1: HTML header file"
"This function will display to the user the header of the website"

def htmlHead(title):

    print("""
    <html>
    <head>
    <title>%s</title>
    <body>
    <h1>%s</h1>

    <p>
    
    """ % (title, title))

################################################################################
## Function 2 ## 
"Function 2: HTML tail file"
"This function will show what time the webpage was generated."

def htmlTail():
    print("""
    <p>
    <hr>
    This webpage was generated at %s.<br>
    <a href="./final_project.py"> Return to home page.</a> 
    </body>
    </html>

    """ % time.ctime())

#################################################################################
## Function 3 ## 
"Function 3: Connection to the Database File"
"""This function will connect to the database, and return connection and cursor objects."""

def getConnAndCursor():

    # need to have the following to connect to DB:
    # username, password (first 4 numbers of BU ID),localhost,and database

    # databases: songs.db, instruments.db, vendors.db 

    conn = db.connect(host="localhost", user="jasonlu6", passwd="8285", db="cs108_jasonlu6_project")

    cursor = conn.cursor()
    return conn, cursor

###################################################################################
## Function 4 ## 
"Function 4: Debugging form data function"
"This function will show all data that was sent to the server in HTTP form."

def debugFormData(form):

    print """
    <h2>Debugging Information:</h2>
    <p>
    HTTP form fields:

    <table border=1>
        <tr>
            <th>Key</th>
            <th>Value</th>
        </tr>
    """
    
    # get key names for the form
    keyNames = form.keys()

    # for loop to iterate all keys and values
    for k in keyNames:

        # if we have a list / single MiniFieldStorage element
        if type(form[k]) == list:

            # print out list of values
            values = form.getlist(k)
            print """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (k, str(values))

        # else the list / single MiniFieldStorage element not found
        else:
            # print the MiniFieldStorage object's value
            value = form[k].value
            print """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
        """ % (k,value)

        # print statement to show end of HTTP form data
        print """
        </table>
        <h3>End of HTTP form data</h3>
        <hr>
        """
    
###################################################################################
## Songs Table Functions ##

## Attributes: ##
## Song ID: the identification number of the song
## Year: the year that the song was produced
## Name: the formal (canon) name of the song
## Artist(s): the artists / main musicians of the song (may be multiple)
## Genre(s): What the song would generally classified based on the rating of the actual iTunes website 
## Function 5a ##
        
"Function 5a: Get all songs data"
"""
This middleware function will get all songs from the songs table
It will return a list of tuples of (songid,year,name,artist,genre)
"""

def getAllSongs():

    # connect to the database
    conn, cursor = getConnAndCursor()

    # SQL statement to query all of the fields in the songs.db table
    sqlSongs = """
    SELECT songid, year, name, artist, genre, description
    FROM songs
    """

    # execute the query
    cursor.execute(sqlSongs)

    # get data from the database
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    # return the data as a tuple
    return data

###################################################################################
## Function 5b ## 
"Function 5b: Show all of the songs for user"
def showAllSongs(data):
    """
    Presentation layer function to display a table showing all available songs for
    the user to select. 
    """

    ## creating HTML table for output
    print("""
    <h2>Song List</h2>
    <p>

    <table border=1>
        <tr>
            <td><font size+=1"><b>songid</font></td>
            <td><font size+=1"><b>year</font></td>
            <td><font size+=1"><b>name</font></td>
            <td><font size+=1"><b>artist</font></td>
            <td><font size+=1"><b>genre</font></td>
            <td><font size+=1"><b>description</font></td>
        </tr>
    """)

    # process the songs in the database
    for row in data:

        # each iteration of the loop creates row of output:
        (songid, year, name, artist, genre, description) = row

        print("""
      <tr>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          
      </tr>
        """ % (songid, songid, songid, year, songid, name, songid, artist, songid, genre, songid, description ))

        # print out how many songs there are total
    print("""
    </table>
    """)

    print("Found %d songs.<br>" % len(data))
###################################################################################
## Function 5c ## 
"Function 5c: get one song from the data"
def getOneSong(songid):
    """
    Middleware function to get one song record from the songs table.
    Returns a list containing one tuple
    """

    # connect to the DB
    conn, cursor = getConnAndCursor()

    # SQL statement to query one song from the songs.db database
    sqlOneSong = """
    SELECT *
    FROM songs
    WHERE songid=%s
    """

    # execute the query
    # using the parameterized queries to avoid the SQL injection vulnerability
    parameters = (songid, )
    cursor.execute(sqlOneSong, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    # return the data
    return data

###################################################################################                  
## Function 5d ## 
"""Function 5d: Form to allow the user to add a new song"""

def addNewSong():

    # General addition of a new song for the user form:
    print("""
    <form>
    <h1 style="background-color:orange">
    New Song
    </h1>
    <p>
    <table>
        <tr>
            <th>Song ID:</th>
            <td><input type="text" name="songid", value='0'></td>
        </tr>

        <tr>
            <th>Year Produced:</th>
            <td><input type="text" name="prodyear", value='0000'></td>
        </tr>
        
        <tr>
            <th>Song Title:</th>
            <td><input type="text" name="songtitle", value='Anonymous'></td>
        </tr>

        <tr>
            <th>Artist(s):</th>
            <td><input type="text" name="songartist", value='No One'></td>
        </tr>

        <tr>
            <th>Genre(s):</th>
            <td><input type="text" name="songgenre", value='N/A'></td>
        </tr>

        <tr>
            <td><input type="submit" name="addsongs"></td>
        </tr>
        
    </table>
    </form>
    """)

###################################################################################
#### Function 5e ##### 
"""Function 5e: SQL to add a song to the song table """
def addSongSQL(songid,year,name,artist,genre):

    # connect to the database
    conn, cursor = getConnAndCursor()

    # SQL insert statement to make the new profile
    sqlInsert = '''
    INSERT INTO songs(songid, year, name, artist, genre)
    VALUES(%s, %s, %s, %s, %s)
    '''

    # execute the query
    # avoid SQL injection with parameterized querying
    parameters = (songid,year,name,artist,genre)
    cursor.execute(sqlInsert,parameters)

    # print statement to show insert works
    print '%d songs were inserted.' % cursor.rowcount

    # getting the data
    data = cursor.fetchall()

    # clean up
    conn.commit() # commit changes to add a new song for user
    cursor.close()
    conn.close()

###################################################################################
#### Function 5f ######
""" Function 5f: SQL to update (change the parameters) in the table"""
def updateSongSQL(songid,year,name,artist,genre,description):

    # connect to the database
    conn, cursor = getConnAndCursor()

    # sql statement to update the songs
    sqlUpdate = '''
    UPDATE songs
    SET year=%s, name=%s, artist=%s, genre=%s, description=%s
    WHERE songid=%s
    '''

    # get the parameters for SQL 
    parameters = (year,name,artist,genre,description,songid)

    # run the SQL
    cursor.execute(sqlUpdate, parameters)

    # return the row count of records affected
    print '%d songs were updated.' % cursor.rowcount

    # clean up
    conn.commit() # commit the changes
    cursor.close()
    conn.close()

###################################################################################
## Function 6 ###
""" Function 6: Form to allow the user to update song data"""
def updateSongForm(songdata):

    ## show the song information
    (songid,year,name,artist,genre,description) = songdata[0]
    record = getOneSong(songid)
    
    print("""
    <html>
    <h1 style="background-color:cyan">
    Update Song
    </h1>
    
    <form>
    <table>
        <tr>
            <th>Song ID:</th>
            <td><input type="text" name="songid", value='%s'></td>
        </tr>

        <tr>
            <th>Year:</th>
            <td><input type="text" name="year", value='%s'></td>
        </tr>

        <tr>
            <th>Name:</th>
            <td><input type="text" name="songname", value='%s'></td>
        </tr>

        <tr>
            <th>Artist:</th>
            <td><input type="text" name="songartist", value='%s'></td>
        </tr>

        <tr>
            <th>Genre:</th>
            <td><input type="text" name="songgenre", value='%s'></td>
        </tr>

        <tr>
            <th>Description:</th>
            <td><input type="text" name="description", value='%s'></td>
        </tr>

        <input type="submit" name='submitUpdateForm'>
        
    </table>
    </form>
    """ % (songid,year,name,artist,genre,description))

###################################################################################
## Function 7 ###
    """
    Function 7: 
    Presentation layer function to display the song page for the user. 
    """
    
def showSongPage(data):

    (songid,year,name,artist,genre,description) = data[0]

    print("""
    <h2 style="background-color:green">
    %s
    </h2>
    <p>
    <table>
        <tr>
            <td>songid</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Song Production Year:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Song Name:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Song Artist(s)</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Song Genre(s)</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Description(s)</td>
            <td>%s</td>
        </tr>
    </table>
    """) % (name,songid,year,name,artist,genre,description)

    vendordata = getVendors(songid)
    showAllVendors(vendordata) 
    
    print("""
    <h3 style="background-color:orange">
    Update Song Data
    </h3>
    <form>
    <table>
        <tr>
             <th>Update Song Data:</th>
            <td><input type="submit" name="submitUpdate"></td>
        </tr>
    </table>

    <input type='hidden' name='songid' value='%s'>
    </form>
    """ % (songid))
###################################################################################
## Function 8 ## 
""" Function 8:
    Form for the user to input what type of song they would like to purchase
    similar to the approach using in shipping.py and shipping2.py in Assignments 18 and 19
"""

def songUserForm():
    print """
    <html>
    <body>

    <h1 style="background-color:cyan">
    Customer Song Purchase Information
    </h1> 
    <form action="http://cs-webapps.bu.edu/cgi-bin/util/formmailer.py">
    <table>
        <tr>
            <th><label>Name:</label></th>
            <td><input type="text" name="name" value=" " width=500></td>
        </tr>

        <tr>
            <th><label>ID:</label></th>
            <td><input type="text" name="id" value=" " width=100></td>
        </tr>

        <tr>
            <th><label>Address:</label></th>
            <td><input type="text" name="address" value=" " width=1000></td>
        </tr>

        <tr>
            <th><label>City:</label</th>
            <td><input type="text" name="city" value=" " width=200></td>
        </tr>

        <tr>
            <td>State (Select one:)</td>
            <td><select name="state">
                    <option value="AL">Alabama</option>
                    <option value="AK">Alaska</option>
                    <option value="AZ">Arizona</option>
                    <option value="AR">Arkansas</option>
                    <option value="CA">California</option>
                    <option value="CO">Colorado</option>
                    <option value="CT">Connecticut</option>
                    <option value="DE">Delaware</option>
                    <option value="DC">District Of Columbia</option>
                    <option value="FL">Florida</option>
                    <option value="GA">Georgia</option>
                    <option value="HI">Hawaii</option>
                    <option value="ID">Idaho</option>
                    <option value="IL">Illinois</option>
                    <option value="IN">Indiana</option>
                    <option value="IA">Iowa</option>
                    <option value="KS">Kansas</option>
                    <option value="KY">Kentucky</option>
                    <option value="LA">Louisiana</option>
                    <option value="ME">Maine</option>
                    <option value="MD">Maryland</option>
                    <option value="MA">Massachusetts</option>
                    <option value="MI">Michigan</option>
                    <option value="MN">Minnesota</option>
                    <option value="MS">Mississippi</option>
                    <option value="MO">Missouri</option>
                    <option value="MT">Montana</option>
                    <option value="NE">Nebraska</option>
                    <option value="NV">Nevada</option>
                    <option value="NH">New Hampshire</option>
                    <option value="NJ">New Jersey</option>
                    <option value="NM">New Mexico</option>
                    <option value="NY">New York</option>
                    <option value="NC">North Carolina</option>
                    <option value="ND">North Dakota</option>
                    <option value="OH">Ohio</option>
                    <option value="OK">Oklahoma</option>
                    <option value="OR">Oregon</option>
                    <option value="PA">Pennsylvania</option>
                    <option value="RI">Rhode Island</option>
                    <option value="SC">South Carolina</option>
                    <option value="SD">South Dakota</option>
                    <option value="TN">Tennessee</option>
                    <option value="TX">Texas</option>
                    <option value="UT">Utah</option>
                    <option value="VT">Vermont</option>
                    <option value="VA">Virginia</option>
                    <option value="WA">Washington</option>
                    <option value="WV">West Virginia</option>
                    <option value="WI">Wisconsin</option>
                    <option value="WY">Wyoming</option>
            </select></td>
              <br>
            </tr>

        <tr>
            <th><label>Zip Code:</label></th>
            <td><input type="text" name="zipcode" value=" " width=100"></td>
        </tr>

        <tr>
            <td>Genre (Select one:)</td>
            <td><select name="genre">
                <option value="POP">Pop</option>
                <option value="DANCE">Dance</option>
                <option value="POP MOVIE">Pop/Movie</option>
                <option value="ALTERNATIVE">Alternative</option>
                <option value="CLASSIC">Classic</option>
                <option value="HIP HOP">Hip Hop</option>
                <option value="RAP">Rap</option>
                <option value="INDIE">Indie</option>
            </select></td>
                <br>
            </tr>

       <tr>
         <td><input type="radio" name="songchoice" value="Shape Of You"><label>Ed Sheeran</label></td>
       </tr>

       <tr>
         <td><input type="radio" name="songchoice" value="Chained To The Rhythm"><label>Katy Perry</label></td>
       </tr>

        <tr>
            <td><input type="radio" name="songchoice" value="Paris"><label>Chainsmoker</label></td>
        </tr>
        
        <tr>
            <td><input type="radio" name="songchoice" value="How Far I'll Go (Moana)"><label>Auli'l Cravalho</label></td>
        </tr>

        <tr>
            <td><input type="radio" name="songchoice" value="Believer (Single)"><label>Imagine Dragons</label></td>
        </tr>

        <input type="hidden" name="mailto" value="jasonlu968@gmail.com">
    </table>

    <!-- submit the form for confirmation -->
    <input type="submit" value="Submit My Order">

    <hr>
    This form was generated at %s.

    </form>
    </body>
    </html>
    """ % time.ctime()

## Vendor Table Functions 
## Attributes:
    
# songid - the identification number of the song(s)
# song - the title of the song
# date - the date of purchase / browsing (within cookie)
# purchase - the amount of times purchased
# website - the official website of the vendor(s)

## Function 9a ## 
"Function 9a: Get all vendors data"
"""
This middleware function will get all vendors from the vendors table
It will return a list of tuples of (songid,year,name,artist,genre)

Initialized to all 0 to show that no user has chosen a song to purchase
until the first payment.
"""

def getAllVendors():

    # connect to the database
    conn, cursor = getConnAndCursor()

    # SQL statement to query all of the fields in the songs.db table
    sqlVendors = """
    SELECT songid, song, date, purchase, website
    FROM vendors
    """

    # execute the query
    cursor.execute(sqlVendors)

    # get data from the database
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    # return the data as a tuple
    return data

###################################################################################
## Function 9b ## 
""" Function 9b:
    Presentation layer function to display a table showing all available vendors for
    the user to select, and what type of song they purchased, the number of times for
    purchase, and the date of purchase (as a history record) 
"""
def showAllVendors(data):

    ## creating HTML table for output
    print("""
    <h2 style="background-color:yellow">
    Vendors Selection
    </h2>
    <p>

    <table border=1>
        <tr>
            <td><font size+=1"><b>songid</font></td>
            <td><font size+=1"><b>song</font></td>
            <td><font size+=1"><b>date</font></td>
            <td><font size+=1"><b>purchase</font></td>
            <td><font size+=1"><b>website</font></td>
        </tr>
    """)

    # process the songs in the database
    for row in data:

        # each iteration of the loop creates row of output:
        (songid, song, date, purchase, website) = row

        print("""
      <tr>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
          <td><a href="?songid=%s">%s</a></td>
     </tr>
        """ % (songid, songid, songid, song, songid, date, songid, purchase, songid, website, ))

        # print out how many vendors there are total
    print("""
    </table>
    """)

    print("Found %d total available vendors.<br>" % len(data))

###################################################################################
## Function 9c ## 
def getOneVendor(songid):
    """
    Function 9c: 
    Middleware function to get one song record from vendors table.
    Returns a list containing one tuple
    """

    # connect to the DB
    conn, cursor = getConnAndCursor()

    # SQL statement to query one song from the songs.db database
    sqlOneSong = """
    SELECT *
    FROM vendors
    WHERE songid=%s
    """

    # execute the query
    # using the parameterized queries to avoid the SQL injection vulnerability
    parameters = (songid, )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    # return the data
    return data

# <input type="hidden" name="songid", value='%s'>
###################################################################################
## Function 9d ##

"""
    Function 9d: SQL function to allow the user to add a new vendor to the mini iTunes website
"""

def addVendorSQL(songid,song,date,purchase,website):

    # connect to the database
    conn, cursor = getConnAndCursor()

    # SQL insert statement to make the new vendor page
    sqlVendor = '''
    INSERT INTO vendors(songid,song,date,purchase,website)
    VALUES(%s,%s,%s,%s,%s)
    '''

    # execute the query
    # avoid SQL injection
    parameters = (songid,song,date,purchase,website)
    cursor.execute(sqlVendor, parameters)

    # getting the data
    data = cursor.fetchall()

    # clean up
    cursor.commit()
    cursor.close()
    conn.close()

###################################################################################
## Function 9e ##
"""
    Function 9e: SQL function to allow the user to update a vendor in the mini iTunes website 
"""

def updateVendorSQL(songid,song,date,purchase,website):

    # connect to the database
    conn, cursor = getConnAndCursor()

    # SQL update statement to update a vendor page
    vendUpdate = '''
    UPDATE vendors
    SET song=%s, date=%s, purchase=%s, website=%s
    WHERE songid=%s
    '''

    # get the parameters in SQL
    parameters = (song,date,purchase,website,songid)

    # run the SQL
    cursor.execute(vendUpdate, parameters)

    # return the row count of updated vendors
    print '%d vendors were updated.' % cursor.rowcount

    # clean up
    conn.commit()
    cursor.close()
    conn.close()
###################################################################################
## Function 9f ## 
""" Function 9f: a function to allow the user to update vendor data """
def updateVendorForm(vendordata):

    # show the vendor information
    (songid,song,date,purchase,website) = vendordata[0]
    record = getOneVendor(songid)

    # print the page
    print("""
    <html>
    <h1 style="background-color:yellow">
    Update Vendor(s)
    </h1>

    <form>
    <table>
        <tr>
            <th>Song ID:</th>
            <td><input type="text" name="songid", value='%s'></td>
        </tr>

        <tr>
            <th>New Song Name:</th>
            <td><input type="text" name="songname", value='%s'></td>
        </tr>

        <tr>
            <th>New Date of Purchase:</th>
            <td><input type="text" name="dop", value='%s'></td>
        </tr>

        <tr>
            <th>Amount of Purchases:</th>
            <td><input type="text" name="purchases", value='%s'></td>
        </tr>

        <tr>
            <th>New Vendor Website:</th>
            <td><input type="text" name="website", value='%s'></td>
        </tr>

        <input type="submit" name="vendorUpdate", value="Submit Vendor Information">
    </table>
    </form> 
    """ % (songid,song,date,purchase,website))
###################################################################################
## Function 10 ## 
""" Function 10: Presentation layer function to display new information about the vendor """
def showVendorPage(data):

    (songid,song,date,purchase,website) = data[0]
    # print the vendor page for the user
    print("""
    <h2 style="background-color:cyan">
    Vendor Information Page
    </h2>
    <p>
    <table>
        <tr>
            <td>Song ID:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Song Name:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Date of Purchase:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Number of Purchases For Song:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Website of Vendor:</td>
            <td>%s</td>
        </tr>
        
    </table>
    """ % (songid,song,date,purchase,website))

    
    print("""
    <h3 style="background-color:red">
    Update Vendor Data
    </h3>
    <form>
    <table>
        <tr>
            <th>Update Vendor Data:</th>
            <td><input type="submit" name="submitVendor"></td>
        </tr>
    </table>

    <input type="hidden" name='songid', value='%s'>
    </form>
    """ % (songid))
    
###################################################################################
## Function 10b ## 
""" Function 10b: A page to add a completely new vendor """

def addNewVendor():

    # General addition of a new vendor for the user form:
    print("""
    <form>
    <h1 style="background-color:cyan">
    New Vendor
    </h1>
    <p>
    <table>
        <tr>
            <th>Song ID:</th>
            <td><input type="text" name="songid" size="20"></td>
        </tr>

        <tr>
            <th>Song Name:</th>
            <td><input type="text" name="songname" size="50"></td>
        </tr>

        <tr>
            <th>Date of Purchase:</th>
            <td><input type="text" name="date" size="60"></td>
        </tr>

        <tr>
            <th>Number of Purchases:</th>
            <td><input type="text" name="purchase" size="10"></td>
        </tr>

        <tr>
            <th>New Website For Vendor:</th>
            <td><input type="text" name="website" size="100"></td>
        </tr>

        <tr>
            <td><input type="submit" name="addvendor"></td>
        </tr>
    </table>
    </form>
    """)
    
###################################################################################
## Function 11 ##
"""Function 11: A middleware function that will select
all of the descriptions for the user (by songid) and return the most recent
description for a particular song."""

def getDescriptionForUser(songid):

    ## connecting to the database
    conn, cursor = getConnAndCursor()
    # sql query
    sql = '''
    SELECT name, description FROM songs WHERE songid=%s
    '''

    # execute the query
    parameters = (int(songid), )
    cursor.execute(sql,parameters)

    # get data from the DB
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    return data

###################################################################################
### Function 12 ####
"""Function 12: Middleware function to allow user to
post a description of the song by songid (form)"""

def postDescription(songid):

    print("""
    <html>
    <h1>New Description For The Song:</h1>
    <form>
    <table>
        <tr>
            <th>Description:</th>
            <td><input type="text" name="description"></td>
        </tr>
    </table>

    <table>
        <tr>
            <th>Submit The Description:</th>
            <td><input type="submit" name="submitDescription"></td>
        </tr>
    <table>

    <input type="hidden" name ="songid" value="%s">
    </form>
    """ % (songid))
    
###################################################################################
## Function 13 ##

"""Function 13b: This function will allow the user to add a new description for a song
selected in the song page query."""

def addDescription(songid, description):
# connect to the DB
    conn, cursor = getConnAndCursor()

    # sql statement to insert (add record to the friends table containing the values)
    sql = '''
    UPDATE songs SET description = %s
    WHERE songid = %s
    '''

    # execute the query
    parameters = (description, songid)
    cursor.execute(sql,parameters)

    # print statement to show that insert was successful
    print 'Description was added.'

    # clean up
    conn.commit() # commit the changes to add friends for user
    cursor.close()
    conn.close()

## Function 14 ##
"""Function 14: SQL join-combinated function that will allow the user to see, upon selection of a song,
   what type of available vendors are visible for the song. The user then can right-click to get to the
   vendor website for that particular song. The two tables being joined are songs and vendors, with primary
   keys songs.songid and vendors.songid 
"""
def getVendors(songid):

    # connect the cursor to the database
    conn, cursor = getConnAndCursor()

    # sql join statement to query both page and vendors table

    # table 1: vendors
    # table 2: songs

    sqlJoin = '''
    SELECT vendors.songid, vendors.song, vendors.date, vendors.purchase, vendors.website
    FROM vendors
    INNER JOIN songs ON vendors.songid = songs.songid
    WHERE songs.songid = %s
    '''

    # execute the query
    parameters = (songid, )
    cursor.execute(sqlJoin, parameters)

    # getting the data
    data = cursor.fetchall()

    # clean up
    cursor.close()
    conn.close()

    # return the data
    return data

###################################################################################
## Instrument Functions ##

## No data change required for this table ##

## Attributes: ##
# instrid: identification number of the song with relation to the instrument
# instrument: what general instruments the song is accompanied / played with
# type: is the song a single or album? 


## Function 15 ## 
"""Function 15: This function will be able to show the user all available instruments
   and types of musical accompianments (duet, piano, ...) for the song as well. It will return
   the total number of instruments found, linked to the songid. The type for the instrument can either
   be in a single form or album form. 
"""

def showAllInstruments(data):

    # HTML table for the output
    print("""
    <h2 style="background-color:green">
    Instruments Selection
    </h2>
    <p>

    <table border=1>
        <tr>
            <td><font size+=1"><b>instrid</font></td>
            <td><font size+=1"><b>instrument</font></td>
            <td><font size+=1"><b>type</font></td>
        </tr>
    """)

    # process the instruments in the database
    for row in data:

        # each iteration of the loop creates a row of output:
        (instrid, instrument, type) = row

        # click on the instrument to view the song site
        print("""
    <tr>
        <td><a href="?instrid=%s">%s</a></td>
        <td><a href="?instrid=%s">%s</a></td>
        <td><a href="?instrid=%s">%s</a></td>
    </tr>
        """ % (instrid, instrid, instrid, instrument, instrid, type, ))

        # print how many types of instruments are there total

    print("""
    </table>
    """)

    print("Found %d total instruments.<br>" % len(data))


###################################################################################
## Function 16 ##
    
"""Function 16: This middleware function displays all instruments
from the instruments table. It will return a list of tuples of
(instrid, instrument, type)"""

def getAllInstruments():

    # connect to the database
    conn, cursor = getConnAndCursor()

    # SQL statement to query all fields in the instruments table
    sqlInstr = """
    SELECT instrid, instrument, type
    FROM instruments 
    """

    # execute the query
    cursor.execute(sqlInstr)

    # get data from the database
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    # return the data as a tuple
    return data 

###################################################################################
## Function 17 ## 
"""
Function 17:
Middleware function to get one instrument from the instruments table.
Returns a list containing the tuple (instrid, instrument, type)

Note: Upon request of the user, we can select exactly one instrument being used.
This function will be sparingly used, only if the user has no other instrument choice.
"""

def getOneInstrument(instrid):
    
    # connect to the DB
    conn, cursor = getConnAndCursor()

    # SQL statement to query one song from the instruments table
    sqlOneInst = """
    SELECT *
    FROM instruments
    WHERE instrid=%s
    """

    # execute the query
    parameters = (instrid, )
    cursor.execute(sql, parameters)

    # get the data from the database
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    # return the data
    return data 

###################################################################################
## Function 18 ##

"""
    Function 18: This function (given a set of data from the table), will be able to display the
    instrument page for the song. Not used unless the user specifically requests to have a particular
    instrument accompanied by the main lyrics of the song. 
"""

def showInstrumentPage(data):

    # print(data)

    (instrid,instrument,type) = data[0]

    print("""
    <h2 style="background-color:yellow">
    Instrument Page 
    </h2>
    <p>
    <table>
        <tr>
            <td>Instrument ID:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Instruments Used:</td>
            <td>%s</td>
        </tr>

        <tr>
            <td>Type of the Instrument:</td>
            <td>%s</td>
        </tr>
    </table>
    """) % (instrid,instrument,type)
    
###################################################################################    
## Function 19 ##

""" Function 19: Upon the successful ordering of a song from mini ITunes, the user
will then be greeted by a confirmation page. """

def confirmation():
    print """
    <html>
    <head>
    <title>Song Order Confirmation Page</title>
    </head>

    <body>

    <h1>Order Information</h1>

    <table>
        <tr>
            <th><label>Name:</label></th>
            <td>%s</td><b>
        </tr>

        <tr><label>ID Number:</label></th>
            <td>%s</td><b>
        </tr>

        <tr><label>Address:</label></th>
            <td>%s</td><b>
        </tr>

        <tr><label>State:</label></th>
            <td>%s</td><b>
        </tr>

        <tr><label>Zip Code:</label></th>
            <td>%s</td><b>
        </tr>

        <tr><label>Genre:</label></th>
            <td>%s</td><b>
        </tr>

        <tr><label>Songs Selected:</label></th>
            <td>%s</td><b>
        </tr>
    </table>
    </body>
    </html> """ % (name,address,city,state,zipcode,genre,songs)

###################################################################################
## Function 20 ##

""" Function 20: If necessary (in the demonstration, I will use my own personal gmail account), the user
can specify the email required to directly send data via a certain handle: (username@mailname.com/.org/.edu) """

def sendMail(sender, recipient, msg, number):
    """Connect up to the SMTP server and send the message (and confirmation number)
    to from sendor (the miniITunes server) to the recipient (user).
    """
    
    # mailer object
    mailer = smtplib.STMP()

    # connect to the outgoing mail server
    mailer.connect("acs-smtp.bu.edu",25)
    # recipient 
    rec = smtp.helo("USERNAME")
    print("Connected to the SMTP server.")

    # send the message and confirmation number to the user
    rec = smtp.sendmail(sender, recipient, msg)
    print("Email was sent to %s" % recipient)

    print("Your confirmation number is: %s" % number)

    # goodbye to the user
    smtp.quit()
    print "Disconnected from the SMTP server."

###################################################################################
## Authentication Functions ##
    
## Function 21a ##

""" Function 21a: The user will be required to have a login name, password, and confirmation number
in order to gain full access of the mini iTunes website."""

def doWelcomeIdentForm():

    print """
    <h2>Welcome!</h2>
    You must identify yourself before using the mini iTunes website. Please enter your:
    <p>
    <form method="post">
    <table>
        <tr>
            <td>
                <h3>Email Address:</h3>
            </td>
            <td>
                <input type="text" name="email" value="johnsmith@bu.edu" size="50"><br>
            </td>
        </tr>

        <tr>
            <td>
                <h3>Password:</h3>
            </td>
            <td>
                <input type="password" name="password" value="******" size="50"><br>
            </td>
        </tr>

        <tr>
            <td>
                <h3>User Confirmation Code:</h3>
            </td>
            <td>
                <input type="text" name="user_cookie" value="0000000" size="50"><br>
            </td>
        </tr>

        <tr>
            <td>
                <input type="submit" name="Login" value="Authenticate">
            </td>
            <td>
            </td>
        </tr>
    </table>
    </form>
    """
    
###################################################################################
### Function 21b ##
""" Function 21b: This function is a session-state maintenance function, in that
upon successful login of the user, the server will give the user the cookie that
maintains the session state"""

def cookieMaintenance(form):

    # get the email, password, and cookie
    email = form["email"].value
    password = form["password"].value
    cookieType = form["user_cookie"].value

    # create the cookie instance
    cookie1 = Cookie.SimpleCookie()
    cookie1["remember_user"] = email

    # print out the cookie
    print cookie1

    # create the second cookie instance
    cookie2 = Cookie.SimpleCookie()
    # default 
    cookie2["confirmation_code"] = cookieType

    # print the cookie
    print cookie2

    htmlHead("User Confirmed")

    # print that the user is authenticated, and can access the mini ITunes website
    print """
    Authentication complete, %s. You have been identified by our servers.
    """ % email 

###################################################################################
## function 21c ##
""" Function 21c: Upon successful login, print a welcome screen for the user """

def printWelcomeScreen(email,cookieType):

    # greet the user
    print """
    Hi %s. Good to see you. Welcome back.
    """ % email

    # print the user's confirmation number as the cookie
    print """
    Your confirmation number is %s.
    """ % cookieType

    # ask the user to submit the confirmation number:
    # make sure the user submits the correct confirmation number


"""Main function""" 
if __name__ == "__main__":

    # read the cookie from the HTTP request
    # environment OS variable
    cs = os.environ["HTTP_COOKIE"]

    # create a cookie object from the string, and load to the cs
    cookie = Cookie.SimpleCookie()
    cookie.load(cs)

    # get the form data
    form = cgi.FieldStorage()
    # debugging statement of the form
    # debugFormData(form)
    
    # call the HTML head (mini iTunes)
    htmlHead("miniITunes")

    # making the images of the songs
    
    # Ed Sheeran's Shape Of You 
    print("""
<html>
<head>
<title>Ed Sheeran's Shape Of You</title>
</head>

<img src ="https://i.ytimg.com/vi/JGwWNGJdvx8/hqdefault.jpg" height="200" width="300">
</html>
        """)

    # Chainsmoker Paris
    print("""
<html>
<head>
<title>Chainsmoker's Paris</title>
</head>

<img src="https://i.ytimg.com/vi/RhU9MZ98jxo/maxresdefault.jpg" height="200" width="300">
</html>
        """)

    # Moana
    print("""
<html>
<head>
<title>Disney's Moana</title>
</head>
<img src="https://vignette4.wikia.nocookie.net/disney/images/9/96/Moana_Trailer_Moana.jpg/revision/latest?cb=20160613192044" height="200" width="300">
</html>
    """)

    # Lady Gaga Million Reasons
    print("""
<html>
<head>
<title>Lady Gaga (Million Reasons)</title>
</head>

<img src="https://i.ytimg.com/vi/OqOapRo0nWk/maxresdefault.jpg" height="200" width="300">
</html>
    """)

    # Yiruma Kiss the Rain
    print("""
<html>
<head>
<title>Lady Gaga (Million Reasons)</title>
</head>

<img src="https://s2.manifo.com/usr/a/Ad323/63/manager/yiruma4ever1144704112.jpg" height="200" width="300">
</html>
    """)
    
    # first thing to show to the user:
    # song selection form (form submission format)
    # allows the user to select (by default) the first five song choices
    # (optional): may have the picture displayed in front of the user
    # upon the song selection 

    if "name" in form and "id" in form and "address" in form and "city" in form and "state" in form and "zipcode" in form and "genre" in form:
        name = form["name"].value
        ident = form["id"].value
        address = form["address"].value
        city = form["city"].value
        state = form["state"].value
        zipcode = form["zipcode"].value
        genre = form["genre"].value
        # choice of song for the user 
        songchoice = form["songchoice"].value

        # the user selections, after authentication login 
        if songchoice == "Ed Sheeran":

            # add the picture

            print("""
            <html>
            <img src ="https://i.ytimg.com/vi/JGwWNGJdvx8/hqdefault.jpg" height="500" width="500">
            </html>
            """)
            
            print("You have selected Shape Of You.")
            

        if songchoice == "Katy Perry":
            print("You have selected Chained To The Rhythm")

            # add the picture 

            print("""
            <html>
            <img src ="https://i.ytimg.com/vi/Um7pMggPnug/hqdefault.jpg " height="500" width="500">
            </html>
            """)
            print("You have selected Shape Of You.")

           
        if songchoice == "Chainsmoker":
            print("You have selected Paris")

            # add the picture

            print("""
            <html>
            <img src="https://i.ytimg.com/vi/RhU9MZ98jxo/maxresdefault.jpg" height="500" width="500">
            </html>
            """)

            
        if songchoice == "Auli'l Cravalho":

            print("""
            <html>
            <img src="https://vignette4.wikia.nocookie.net/disney/images/9/96/Moana_Trailer_Moana.jpg/revision/latest?cb=20160613192044" height="500" width="500">
            </html>
            """)
            
            print("You have selected How Far I'll Go (Moana)")

        if songchoice == "Imagine Dragons":

            ## no picture available yet ##
            
            print("You have selected Believer (Single)")

    # adding a song within the form
    # pre-filled values by default:
    # Song ID: 0
    # Year Produced: 0000
    # Song Title: Anonymous
    # Artists: No One
    # Genre(s): N/A 
    elif 'addsongs' in form:
        songid = form['songid'].value
        production = form['prodyear'].value
        title = form['songtitle'].value
        artist = form['songartist'].value
        genre = form['songgenre'].value
        addNewSong()
        addSongSQL(songid,production,title,artist,genre)

    # updating the song within the form 
    elif 'submitUpdate' in form:
        songid = form['songid'].value
        songdata = getOneSong(songid)
        updateSongForm(songdata) 
        
    # submit the updated song form on the SQL database
    elif 'submitUpdateForm' in form:
        songid = form['songid'].value
        songyear = form['year'].value
        songtitle = form['songname'].value
        songartist = form['songartist'].value
        songgenre = form['songgenre'].value
        description = form['description'].value
        updateSongSQL(songid, songyear, songtitle, songartist, songgenre,description)

    # adding vendors to the table
    elif 'addvendor' in form:
        songid = form['songid'].value
        songname = form['songname'].value
        datepurchase = form['date'].value
        purchase = form['purchase'].value
        website = form['website'].value
        addNewVendor()
        addVendorSQL(songid,songname,datepurchase,purchase,website)

    # submitting a vendor to the table 
    elif 'submitVendor' in form:
        songid = form['songid'].value
        vendordata = getOneVendor(songid)
        updateVendorForm(vendordata)

    # updating the vendors in the form
    elif 'vendorUpdate' in form:
        songid = form['songid'].value
        songname = form['songname'].value
        datepurchase = form['dop'].value
        purchase = form['purchases'].value
        website = form['website'].value
        updateVendorSQL(songid,songname,datepurchase,purchase,website)

    # show a description for the user to post
    elif 'songid' in form:
       # unpack the python variable
       songid = form['songid'].value
       data = getOneSong(songid)
       showSongPage(data)

    elif 'submitDescription' in form:
        # unpack the description
        description = form['description'].value
        songid = form['songid'].value
        addDescription(songid,description)

    # begin with user confirmation page on the top 
    else:
        htmlHead("User Confirmation")
        doWelcomeIdentForm()
        
        # authenticate the user first via username and password
        if "remember_user" in cookie and "confirmation_code" in cookie:
            email = cookie["remember_user"].value
            confirmNum = cookie["confirmation_code"].value
            printWelcomeScreen(email,confirmNum)

        # elif "name" in form and "email" in form and "password" in form and "user_cookie" in form and
        elif "Login" in form:
            cookieMaintenance(form)

        else:
            # give the user the form
            # allow the users to see the full database of
            # songs, vendors, instruments

            # Finally, give the user an ability to add a new song 
            songUserForm()
            data = getAllSongs()
            showAllSongs(data)

            data2 = getAllVendors()
            showAllVendors(data2)

            data3 = getAllInstruments()
            showAllInstruments(data3)

            addNewSong()

    # call the HTML tail, and the website is complete 
    htmlTail()

