from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import urllib.parse
import cgi
import os.path
import time
import neopixel
import board
 
 
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
 
# The number of NeoPixels
num_pixels = 50
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)


def fileRead(fname,textFile=False):
    f=open(fname)
    raw=f.read()
    f.close()
    if textFile==True and ".txt" in fname:
        raw=raw.replace("\n","\n<br>")
        raw="<code>"+raw+"</code>"
        raw=tableIt(raw)
    return raw

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
 
 

def rainbow_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)

class Handler(BaseHTTPRequestHandler):

    def do_PAGE(self,form=None,msg="",edge=True):
        if self.path=="/": self.path="/index.html"
        fname= './'+ self.path
        page=""

        if not form==None:
            formDict={}
            for key in form.keys():
                formDict[key]=form[key].value
                if key=='call':
                    formDict[key]=formDict[key].upper()

        if self.path=="/neo":
            if form==None:
                print ("NO STUFF?!?")
            elif "GREEN" in formDict["action"]:
                pixels.fill((0, 0, 255))
                print ('Color changed to Green!')
            elif "RED" in formDict["action"]:
                pixels.fill((255, 0, 0))
                print ('Color changed to Red!')
            elif "PURPLE" in formDict["action"]:
                pixels.fill((255, 255, 0))
                print ('Color changed to Purple!')
            elif "BLUE" in formDict["action"]:
                pixels.fill((0, 255, 0))
                print ('Color changed to Blue!')
            elif "YELLOW" in formDict["action"]:
                pixels.fill((255, 0, 255))
                print ('Color changed to Yellow!')
            elif "RAINBOW" in formDict["action"]:
                rainbow_cycle()
                print ('Color changed to Rainbow!')
            pixels.show()
            msg=fileRead("close.html",True)
            if "frameset" in msg: edge=False

        elif '.' in self.path and os.path.exists(fname):
            msg=fileRead(fname,True)
            if "frameset" in msg: edge=False
        
        self.wfile.write(bytes(msg, "utf-8"))

    
    def do_GET(self):
        ##if 'favicon' in self.path:
        ##    self.send_error(404, "File not found")
        ##    return    
        self.send_response(200)
        self.end_headers()
        self.do_PAGE()
        return

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                            environ={'REQUEST_METHOD':'POST',
                            'CONTENT_TYPE':self.headers['Content-Type'],})
        self.send_response(200)
        self.end_headers()
        self.do_PAGE(form)
        return

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

	
## Edit the section below for your computer IP and port settings
if __name__ == '__main__':
    myIP='localhost'
    myIP='127.0.0.1'
    myPort=90
    server = ThreadedHTTPServer((myIP, myPort), Handler)
    print ('Starting server, use <Ctrl-C> to stop')
    print ('http://%s:%d'%(myIP,myPort))
    server.serve_forever()
