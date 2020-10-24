from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import logging

class DugoutServer():
    sensors = None
    config = None
    def __init__(self, address, port, sensors_, config_):
        DugoutServer.sensors    = sensors_
        DugoutServer.config     = config_
        self.web_server = None
        self.address = address
        self.port = port

    def serve(self):
        self.web_server = HTTPServer((self.address, self.port), DugoutServer.RequestHandler)
        self.web_server.serve_forever()

    def stop(self):
        logging.debug("Stopping Dugout Web Server")
        self.web_server.server_close()

    def process_measurements(measurements):
        return {
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "config": DugoutServer.config,
            "sensors": measurements
            }

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            measurements = DugoutServer.sensors.get() # this is blocking
            data = DugoutServer.process_measurements(measurements)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(data), "utf-8"))