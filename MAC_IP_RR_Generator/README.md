# MAC_IP_RR_Generator
Python script to generate MAC address, IP Address and DNS Address(A) Resource Record Generator based on the required number of addresses required in the argument

## Important Notes
- MAC/IP addresses are generated in ascending order
- MAC address starts from 00:00:00:00:00:01, output file: `ipaddress.txt`
- IP address starts from 2.0.0.1, output file: `ipaddress.txt`
- A record starts from a.acme.corp, output file: `arecord.txt`
   
## MAC Generator Examples
   - Generate MAC Address with 100 entries<br />
     `# python3 ./macgenerator.py mac 100`<br />
   - Generate IP Address with 100 entries<br />
     `# python3 ./macgenerator.py ip 100`<br />
   - Generate DNS A Records with 100 entries<br />
     `# python3 ./macgenerator.py a 100`
   > **Note:**<br />
   > Arguments comprises of: TYPE_OF_ADDRRESS COUNT<br />
   >           TYPE_OF_ADDRESS: `ip` / `mac` / `acme` <br />
   >           COUNT: integer greater than 0
   
## Sample IP Address
``` 
2.0.0.1
2.0.0.2
2.0.0.3
2.0.0.4
2.0.0.5
2.0.0.6
2.0.0.7
2.0.0.8
2.0.0.9
2.0.0.10 
```

## Sample MAC Addresses
```
00:00:00:00:00:01
00:00:00:00:00:02
00:00:00:00:00:03
00:00:00:00:00:04
00:00:00:00:00:05
00:00:00:00:00:06
00:00:00:00:00:07
00:00:00:00:00:08
00:00:00:00:00:09
00:00:00:00:00:0a
00:00:00:00:00:0b
00:00:00:00:00:0c
```

## Sample DNS A Records
```
a.acme.corp
b.acme.corp
c.acme.corp
d.acme.corp
e.acme.corp
f.acme.corp
g.acme.corp
h.acme.corp
i.acme.corp
j.acme.corp
```
