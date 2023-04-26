#!/data1/users/admin/bind_zone_exporter/bin/python3

##########################################################################
# Reference:   https://trstringer.com/quick-and-easy-prometheus-exporter/
# Title:       BIND Zone Exporter
# Description: Exporter for Prometheus Extracting Zone Statistics 
# Author:      Muhammad Heidir (md.heidir@efficientip.com)
# Date:        20 April 2023
# Version:     0.2
# License:     CC-BYSA (https://creativecommons.org/licenses/by-sa/4.0/)
# Changelog:
#              0.1 - Initial release, tested on SOLIDserver v8.2
#                  - Runs in virtualenv (extract and execute)
#              0.2 - Added support for Slave zones
#              
##########################################################################


import os
import sys
sys.path.append("/data1/users/admin/bind_zone_exporter/lib/python3.9/site-packages")
import time
from prometheus_client import start_http_server, Gauge
import requests
import json


class BindZoneMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    BIND Zone metrics into Prometheus metrics.
    """

    def __init__(self, host_port="localhost:8080", polling_interval_seconds=5, listener_port=9100):
        self.host_port = host_port
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.view_zone_rcode = Gauge("bind_view_zone_rcode", "Response Code Count by View, Zone", ['view', 'zone', 'rcode'])
        self.view_zone_qtype = Gauge("bind_view_zone_qtypes", "Query Types Count by View, Zone", ['view', 'zone', 'qtypes'])
    
    def _check_json(self, p, attr):
        # Reference: https://stackoverflow.com/questions/5508509/how-do-i-check-if-a-string-is-valid-json-in-python#:~:text=If%20the%20object%20contains%20valid,calling%20a%20non%20JSON%20object.
        doc = json.loads(json.dumps(p))
        try:
            doc.get(attr) # we don't care if the value exists. Only that 'get()' is accessible
            return True
        except AttributeError:
            return False
    
                            
    def createRcodeGauge(self, dnsview, dnszone, dnsrcode, dnsvalue):
        self.view_zone_rcode.labels(dnsview,dnszone,dnsrcode).set(dnsvalue)
    
    def createQtypesGauge(self, dnsview, dnszone, dnsqtypes, dnsvalue):
        self.view_zone_qtype.labels(dnsview,dnszone,dnsqtypes).set(dnsvalue)

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            try:
                self.fetch()
                time.sleep(self.polling_interval_seconds)
                 
            except Exception as err:
                print(err) 

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """
        # Fetch raw status data from the application
        resp = requests.get(self.host_port+"/json")
        status_data = resp.json()

        #data = json.loads(status_data)
        views = status_data["views"]
        
        # Find DNS Views
        for view in views:
            # Find Zones Definitions within the views
            # Skip if view name = '_bind', process the rest
            if (view != "_bind"):
                for zones in views[view]:
                    # List the Zones
                    for zone in views[view][zones]:
                        # Check if zone is valid and contains type as "master", ignore the rest
                        if (self._check_json(zone, 'name') and (zone['type'] == "master" or zone['type'] == "slave")):
                        
                            # Update Prometheus metrics with Response Code Count, Per View, Per Zone
                            for rcode in zone['rcodes']:
                                self.createRcodeGauge(view, zone['name'], rcode, zone['rcodes'][rcode])
                            
                            # Update Prometheus metrics with Query Type Count, Per View, Per Zone
                            for qtype in zone['qtypes']:
                                self.createQtypesGauge(view, zone['name'], qtype, zone['qtypes'][qtype])

    
def main(_binduri="http://localhost:8080",_bindpoll=5,_listenport=9100):
    """Main entry point"""

    bindzone_metrics = BindZoneMetrics(
        host_port=_binduri,
        polling_interval_seconds=_bindpoll
    )
    
    print(f"Starting server listener on port: {_listenport}")
    start_http_server(_listenport)
   
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"[{current_time}] Getting BIND Zone Statistics from: {_binduri}")
    bindzone_metrics.run_metrics_loop()

def help():
    _version = "0.1"
    _arguments = """
Arguments:
    help                    Show help commands
    BIND-URI                HTTP JSON API address of BIND server (Default: http://localhost:8080)
    POLL                    Poll interval for getting stats from BIND server in seconds (Default: 5)
    LISTEN-PORT             Listener port for Prometheus to scrape data from (Default: 9100)
"""
    print(f"BIND Zone Exporter {_version}\n")
    print(f"Usage: {sys.argv[0]} BIND-URI [BIND-TIMEOUT] [LISTEN-PORT]")
    print(f"{_arguments}")

#########################################################################
#status_data = ""

if __name__ == "__main__":
    if (len(sys.argv) == 2 and sys.argv[1] == "help"):
        help()
        
    elif (len(sys.argv) == 1):
        # Start default listener and poll metrics
        main()
    
    elif (len(sys.argv) == 2):
        _binduri = sys.argv[1]
        
        # Start listener and poll metrics
        main(_binduri)
        
    elif (len(sys.argv) == 3):       
        _binduri = sys.argv[1]
        _bindpoll = int(sys.argv[2])
        
        # Start listener and poll metrics
        main(_binduri,_bindpoll)
            
    elif (len(sys.argv) == 4):   
        _binduri = sys.argv[1]
        _bindpoll = int(sys.argv[2])
        _listenport = int(sys.argv[3])
        
        # Start listener and poll metrics
        main(_binduri,_bindpoll,_listenport)
        
    else:
        help()
    
    sys.exit(0)
    