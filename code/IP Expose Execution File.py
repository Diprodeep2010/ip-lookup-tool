#http://hci574.blogspot.in/2010/04/using-google-maps-static-images.html
#author Avik Pal
import sys
import urllib
import socket
import easygui

import cStringIO 
from PIL import Image

import pygeoip

show_image="images1.jpg"
rawdata = pygeoip.GeoIP('GeoLiteCity.dat')
DOMAIN_NAME=None
def ipquery(ip):
    try:
        data = rawdata.record_by_name(ip)
        country = data['country_name']
        city = data['city']
        longi = data['longitude']
        lat = data['latitude']
        centerlocation=str(lat)+","+str(longi)
        #print location
        # make a map around a center
        image_name=get_static_google_map(center=centerlocation, zoom=11, imgsize=(320,240),
                               maptype="terrain", markers="size:mid|label:B|color:red|"+centerlocation+"|" )
        
        
        if DOMAIN_NAME != None :
            easygui.msgbox("IP Adress:="+ip+"\nDomain Name:= "+DOMAIN_NAME+"\nCountry:="+str(country)+"\nCity:="+str(city)+"\nlatitude:="+str(lat)+"\nlongitude:="+str(longi),
                       "Location Details",image=image_name)
        else:
            easygui.msgbox("IP Adress:="+ip+"\nCountry:="+str(country)+"\nCity:="+str(city)+"\nlatitude:="+str(lat)+"\nlongitude:="+str(longi),
                       "Location Details",image=image_name)
    except:
        easygui.msgbox("Location can not be processed. \nCheck the network connection \n or the server is not available. \n \n Try again after sometime","ERROR")
        sys.exit(0)

    
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
    #print request
    
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
        PIL_img.save("gmap.png", "PNG") # save as png image in disk
        image_name="gmap.png"
        return image_name
        
        

if __name__ == '__main__':
    is_url_given=False 
    url=""
    title="IP Expose"
    easygui.msgbox("Welcome to IP Expose", title, image=show_image)
    msg = "Are you ready to begin Decrepifying?"
    
    if easygui.ccbox(msg, title,image=show_image):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:  # user chose Cancel
        sys.exit(0)

    msg = "Choose between Look Up and Reverse Look Up"
    
    if easygui.buttonbox(msg, title, choices=('Look Up', 'Reverse Look Up'),image=show_image) == 'Look Up' :     # show a Continue/Cancel dialog
        while is_url_given != True :
            url=easygui.enterbox("Enter URL , Press OK and Wait...", title, default='', strip=True, image=show_image, root=None)
            if url==None:
                sys.exit(0)
            if url !="" :
                is_url_given=True
                try:
                    ipaddress=socket.gethostbyname(url)
                except:
                    easygui.msgbox("Entered url can not be processed \nCheck the network connection."+
                                   "\n Or the url is either not correct or not available."+"\n \n Try again after sometime","ERROR")
                    sys.exit(0)
                ipquery(ipaddress)
            else:
                easygui.msgbox("Enter the url,field is empty","ERROR")  
    else:  # user chose Reverse Look Up 
        while is_url_given != True :
            ip=easygui.enterbox("Enter IP Address , Press OK and Wait...", title, default='', strip=True, image=show_image, root=None)
            if ip == None:
                sys.exit(0)
            if ip !="" :
                is_url_given=True
                try:
                    ipaddress=ip
                    name,alias,ip=socket.gethostbyaddr(ip)
                    DOMAIN_NAME=name
                except:
                    easygui.msgbox("Entered IP Address can not be processed \nCheck the network connection."+
                                   "\n Or the IP Address is either not correct or not available."+"\n \n Try again after sometime","ERROR")
                    sys.exit(0)
                ipquery(ipaddress)
            else:
                easygui.msgbox("Enter the IP Address,field is empty","ERROR")      
     
     


   
