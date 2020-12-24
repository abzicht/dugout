from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import time
import json
import logging

class DugoutServer():
    sensors = None
    config = None
    ongoing_request = False
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
            if DugoutServer.ongoing_request:
                logging.debug("New request is delayed! An ongoing request was detected.")
                while(DugoutServer.ongoing_request):
                    time.sleep(0.05)
                logging.debug("New request is now being processed.")
            DugoutServer.ongoing_request = True
            try:
                measurements = DugoutServer.sensors.get() # this is blocking
                data = DugoutServer.process_measurements(measurements)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(data), "utf-8"))
            except Exception as msg:
                logging.error(msg)
            finally:
                DugoutServer.ongoing_request = False
        def do_POST(self):
            if DugoutServer.ongoing_request:
                logging.debug("New request is delayed! An ongoing request was detected.")
                while(DugoutServer.ongoing_request):
                    time.sleep(0.05)
                logging.debug("New request is now being processed.")
            DugoutServer.ongoing_request = True
            success = True
            try:
                logging.info(self.headers)
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    postvars = cgi.parse_multipart(self.rfile, pdict)
                elif ctype == 'application/x-www-form-urlencoded':
                    length = int(self.headers['content-length'])
                    postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                else:
                    postvars = {}
                logging.info(ctype)
                logging.info(postvars)
                payload = json.loads(bytes.decode(list(postvars.keys())[0],'utf-8'))
                logging.info(payload)
                success = DugoutServer.sensors.set(payload) # this is blocking
            except Exception as msg:
                logging.error(msg)
                success = False
            finally:
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps({"success":success}), "utf-8"))
                except Exception as msg:
                    pass
                DugoutServer.ongoing_request = False
