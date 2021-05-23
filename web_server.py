# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVER_HOSTNAME = "localhost"
SERVER_PORT = 8080
contents = ""

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head></head><body>", "utf-8"))
        self.wfile.write(bytes("{}".format(contents), "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

def run():
    web_server = HTTPServer((SERVER_HOSTNAME, SERVER_PORT), WebServer)
    print("Server started http://{}:{}".format(SERVER_HOSTNAME, SERVER_PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")