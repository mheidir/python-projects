# BINDZoneExporter
Written in Python3 to facilitate the extraction and conversion of BIND Zone Statistics for Prometheus to scrape the information and allow Grafana to present the data in a visually appealing UI.
Script was prepared for EfficientIP SOLIDserver with all required modules intact within the virtualenv, in cshell as a background process. As a Python script, the code is portable without having to add external dependencies to achieve the required purpose.

## Important Notes
- Script should be compatible with standard ISC-BIND
- Zone Statistics must be set
- Statistics Channel must be set
- ISC-BIND must be compiled with json-c for the Zone Statistics to be in JSON format (Reference: [https://kb.isc.org/docs/monitoring-recommendations-for-bind-9](https://kb.isc.org/docs/monitoring-recommendations-for-bind-9) 

## Tested SOLIDserver Versions
- SOLIDserver v8.2.0

## Configuration on EfficientIP SOLIDserver
1. Download the tar.gz file from the releases directory and upload to `/data1/users/admin`<br /><br />
2. Extract the file: `# tar -zxvf bind_zone_exporter_0.1_8.2.tar.gz`<br /><br />
3. Enter the directory: `# cd bind_zone_exporter`<br /><br />
4. Execute the full command: `# ./bin/python3 ./bind_zone_exporter.py &`
   Script executes with default values comprising of the following:
   - **BIND-URI:** http://localhost:8080/json
   - **POLL:** 5 seconds
   - **EXPOSED PORT:** 9100<br /><br />
5. Configure built-in firewall with a new rule to allow inbound TCP on port 9100
   Hardened the firewall rule by allowing only specific source IP and destination IP on an expected network interface<br /><br />
6. Verify BIND Zone Statistics are compiled and exposed: <br />
   `curl http://localhost:9100/metrics`<br />
7. Configure Prometheus to scrape data via the specified interface IP address and port. Edit `prometheus.yml` and add the following target:
   ```
   - job_name: "sds-ns1-zone"
    static_configs:
      - targets: ['10.10.10.1:9100']
        labels:
          alias: "sds-ns1-zone"
   ```
8. Restart Prometheus to apply changes to the target<br /><br />
9. Configure Grafana with additional Data Source, directing towards the Prometheus server<br /><br />
10. Add dashboard on Grafana and start compiling the data into a visual presentation
   
## BIND Zone Exporter Examples
   - Run with specific BIND-URI<br />
     `# ./bin/python3 ./bind_zone_exporter.py http://10.10.10.1:8053 &`<br />
   - Run with specified BIND-URI and Poll period of 10 seconds<br />
     `# ./bin/python3 ./bind_zone_exporter.py http://10.10.10.1:8053 10 &`<br />
   - Run with specified BIND-URI, Poll Period of 10 seconds on specified Port<br />
     `# ./bin/python3 ./bind_zone_exporter.py http://10.10.10.1:8053 10 9101 &`
   > **Note:** Argument sequence is fixed.<br />
   >           BIND-URI POLL EXPOSED_PORT
   
## Sample BIND Zone Statistics in JSON format
``` 
{
  "json-stats-version":"1.5",
  "boot-time":"2023-04-13T08:16:48.309Z",
  "config-time":"2023-04-13T08:16:49.381Z",
  "current-time":"2023-04-16T02:52:00.373Z",
  "version":"9.16.33",
  "views":{
    "_default":{
        "zones":[ 
            {
              "name":"0.0.10.in-addr.arpa",
              "class":"IN",
              "serial":5,
              "type":"master",
              "loaded":"2023-02-03T14:32:26Z",
              "rcodes":{
                "QrySuccess":198,
                "QryAuthAns":219,
                "QryNXDOMAIN":21,
                "QryUDP":153,
                "QryTCP":66
              },
              "qtypes":{
                "SOA":194,
                "PTR":25
              }
            },
            {
              "name":"10.10.10.in-addr.arpa",
              "class":"IN",
              "serial":2023010421,
              "type":"master",
              "loaded":"2023-02-09T03:37:26Z",
              "rcodes":{
                "QrySuccess":206,
                "QryAuthAns":227,
                "QryNxrrset":10,
                "QryNXDOMAIN":11,
                "QryUDP":161,
                "QryTCP":66
              },
              "qtypes":{
                "SOA":208,
                "PTR":19
              }
            },
            {
              "name":"11.10.10.in-addr.arpa",
              "class":"IN",
              "serial":4,
              "type":"master",
              "loaded":"2023-01-06T10:38:47Z",
              "rcodes":{
                "QrySuccess":195,
                "QryAuthAns":261,
                "QryNXDOMAIN":66,
                "QryUDP":195,
                "QryTCP":66
              },
              "qtypes":{
                "SOA":195,
                "PTR":66
              }
            },
            {
              "name":"efficientip.lab",
              "class":"IN",
              "serial":2023013038,
              "type":"master",
              "loaded":"2023-04-13T07:54:30Z",
              "rcodes":{
                "QrySuccess":1085,
                "QryAuthAns":1836,
                "QryNxrrset":567,
                "QryNXDOMAIN":184,
                "XfrReqDone":137,
                "UpdateDone":75,
                "QryUDP":1702,
                "QryTCP":134
              },
              "qtypes":{
                "A":618,
                "NS":48,
                "SOA":891,
                "AAAA":234,
                "SRV":28
              }
            },
            {
              "name":"obfuscate.lab",
              "class":"IN",
              "serial":2023022731,
              "type":"master",
              "loaded":"2023-04-11T18:44:07Z",
              "rcodes":{
                "QrySuccess":294,
                "QryAuthAns":294,
                "QryUDP":228,
                "QryTCP":66
              },
              "qtypes":{
                "SOA":294
              }
            }
        ]
    }
  }
}   
```

## Sample Prometheus Scrape Data
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 8.596522e+06
python_gc_objects_collected_total{generation="1"} 781633.0
python_gc_objects_collected_total{generation="2"} 25284.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 499843.0
python_gc_collections_total{generation="1"} 45440.0
python_gc_collections_total{generation="2"} 1468.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="8",patchlevel="15",version="3.8.15"} 1.0
# HELP bind_view_zone_rcode Response Code Count by View, Zone
# TYPE bind_view_zone_rcode gauge
bind_view_zone_rcode{rcode="QrySuccess",view="_default",zone="0.0.10.in-addr.arpa"} 982.0
bind_view_zone_rcode{rcode="QryAuthAns",view="_default",zone="0.0.10.in-addr.arpa"} 1099.0
bind_view_zone_rcode{rcode="QryNXDOMAIN",view="_default",zone="0.0.10.in-addr.arpa"} 117.0
bind_view_zone_rcode{rcode="QryUDP",view="_default",zone="0.0.10.in-addr.arpa"} 784.0
bind_view_zone_rcode{rcode="QryTCP",view="_default",zone="0.0.10.in-addr.arpa"} 315.0
bind_view_zone_rcode{rcode="QrySuccess",view="_default",zone="10.10.10.in-addr.arpa"} 995.0
bind_view_zone_rcode{rcode="QryAuthAns",view="_default",zone="10.10.10.in-addr.arpa"} 1113.0
bind_view_zone_rcode{rcode="QryNxrrset",view="_default",zone="10.10.10.in-addr.arpa"} 39.0
bind_view_zone_rcode{rcode="QryNXDOMAIN",view="_default",zone="10.10.10.in-addr.arpa"} 79.0
bind_view_zone_rcode{rcode="QryUDP",view="_default",zone="10.10.10.in-addr.arpa"} 798.0
bind_view_zone_rcode{rcode="QryTCP",view="_default",zone="10.10.10.in-addr.arpa"} 315.0
bind_view_zone_rcode{rcode="QrySuccess",view="_default",zone="11.10.10.in-addr.arpa"} 964.0
bind_view_zone_rcode{rcode="QryAuthAns",view="_default",zone="11.10.10.in-addr.arpa"} 1280.0
bind_view_zone_rcode{rcode="QryNXDOMAIN",view="_default",zone="11.10.10.in-addr.arpa"} 316.0
# HELP bind_view_zone_qtypes Query Types Count by View, Zone
# TYPE bind_view_zone_qtypes gauge
bind_view_zone_qtypes{qtypes="SOA",view="_default",zone="0.0.10.in-addr.arpa"} 957.0
bind_view_zone_qtypes{qtypes="PTR",view="_default",zone="0.0.10.in-addr.arpa"} 142.0
bind_view_zone_qtypes{qtypes="SOA",view="_default",zone="10.10.10.in-addr.arpa"} 982.0
bind_view_zone_qtypes{qtypes="PTR",view="_default",zone="10.10.10.in-addr.arpa"} 131.0
bind_view_zone_qtypes{qtypes="SOA",view="_default",zone="11.10.10.in-addr.arpa"} 964.0
bind_view_zone_qtypes{qtypes="PTR",view="_default",zone="11.10.10.in-addr.arpa"} 316.0
```


