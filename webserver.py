from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urlparse
import cgi
import os.path



def fileRead(fname,textFile=False):
    f=open(fname)
    raw=f.read()
    f.close()
    if textFile==True and ".txt" in fname:
        raw=raw.replace("\n","\n<br>")
        raw="<code>"+raw+"</code>"
        raw=tableIt(raw)
    return raw

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



        if self.path=="/green":
            if form==None:
                print 'NO STUFF?!?'
            elif "GREEN" in formDict["action"]:
                print 'Color changed to Green!'
            msg=fileRead("close.html",True)
            if "frameset" in msg: edge=False

        elif '.' in self.path and os.path.exists(fname):
            msg=fileRead(fname,True)
            if "frameset" in msg: edge=False
        
        self.wfile.write(msg)

    
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

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

	
## Edit the section below for your computer IP and port settings
if __name__ == '__main__':
    myIP='localhost'
    myIP='127.0.0.1'
    myPort=80
    server = ThreadedHTTPServer((myIP, myPort), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    print 'http://%s:%d'%(myIP,myPort)
    server.serve_forever()
