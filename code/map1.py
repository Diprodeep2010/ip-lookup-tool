#http://hci574.blogspot.in/2010/04/using-google-maps-static-images.html
#author Avik Pal
import urllib
import cStringIO 
import Image

from Tkinter import *  # order seems to matter: import Tkinter first
import Image, ImageTk  # then import ImageTk

import pygeoip
rawdata = pygeoip.GeoIP('f:/GeoLiteCity.dat')
def ipquery(ip):
    data = rawdata.record_by_name(ip)
    country = data['country_name']
    city = data['city']
    longi = data['longitude']
    lat = data['latitude']
    print '[x] '+str(city)+',' +str(country)
    print '[x] Latitude: '+str(lat)+ ', Longitude: '+ str(longi)
    location=str(lat)+","+str(longi)
    print location
    return location

class MyFrame(Frame):
    def __init__(self, master, im):
        Frame.__init__(self, master)
        self.caption = Label(self, text="Location of given URL")
        self.caption.grid()
        self.image = ImageTk.PhotoImage(im) # <--- results of PhotoImage() must be stored
        self.image_label = Label(self, image=self.image, bd=0) # <--- will not work if 'image = ImageTk.PhotoImage(im)'
        self.image_label.grid()
        self.grid()




def get_static_google_map(center=None, zoom=None, imgsize=None, 
                          maptype="roadmap", markers=None ):  
    """retrieve a map (image) from the static google maps server 
    
     See: http://code.google.com/apis/maps/documentation/staticmaps/
        
        Creates a request string with a URL like this:
        http://maps.google.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=14&size=512x512&maptype=roadmap
&markers=color:blue|label:S|40.702147,-74.015794&sensor=false"""
   
    
    # assemble the URL
    request =  "http://maps.google.com/maps/api/staticmap?" # base URL, append query params, separated by &
   
    # if center and zoom  are not given, the map will show all marker locations
    if center != None:
        request += "center=%s&" % center
        #request += "center=%s&" % "40.714728, -73.998672"   # latitude and longitude (up to 6-digits)
        #request += "center=%s&" % "50011" # could also be a zipcode,
        #request += "center=%s&" % "Brooklyn+Bridge,New+York,NY"  # or a search term 
    if center != None:
        request += "zoom=%i&" % zoom  # zoom 0 (all of the world scale ) to 22 (single buildings scale)


    request += "size=%ix%i&" % (imgsize)  # tuple of ints, up to 640 by 640
    request += "format=png&" 
    request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain


    # add markers (location and style)
    if markers != None:
       request += "markers=%s&" % markers


    #request += "mobile=false&"  # optional: mobile=true will assume the image is shown on a small screen (mobile device)
    request += "sensor=false&"   # must be given, deals with getting loction from mobile device 
    print request
    
    # read into PIL 
    web_sock = urllib.urlopen(request)
    imgdata = cStringIO.StringIO(web_sock.read()) # constructs a StringIO holding the image
    try:
        PIL_img = Image.open(imgdata)
    
    # if this cannot be read as image that, it's probably an error from the server,
    except IOError:
        print "IOError:", imgdata.read() # print error (or it may return a image showing the error"
     
    # show image 
    else:
        PIL_img.save("f:/gmap.png", "PNG") # save as png image in disk
        im=PIL_img
        mainw = Tk()
        mainw.frame = MyFrame(mainw, im)
        mainw.mainloop()


if __name__ == '__main__':
    ipaddress=input("Enter Ip address")

    centerlocation=ipquery(ipaddress)

    # make a map around a center
    get_static_google_map(center=centerlocation, zoom=12, imgsize=(500,500),
                           maptype="terrain", markers="size:mid|label:B|color:red|"+centerlocation+"|")


   
