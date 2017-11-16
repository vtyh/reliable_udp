Networks Project
================
A project to implement a reliable and quick transport protocol (RQTP) in a local network, used for:
- Point to point file transfer
- Broadcasting

Test and Experiment
-------------------
Mininet is used to simulate our network with packet loss. 

To start mininet, use
```terminal
$ sudo ./run.sh
```

Start the server application on h1, and the client(s) on h2-h5. Set up the server to send approximately 1.5 Mbps of traffic to the client(s). No packets loss should be observed.

However, packet loss should be observed when the rate of file transfer is increased (e.g 1.6 Mbps). 

Flow Control
------------
To test UDP in the case of congestion causing data loss. 

Reliability 
Files: reliableClientTest.py, reliableServerTest.py

Testing reliability using lab3 files by adjusting rates of data transfer. 

Flow Control
Files: FlowControlClientTest.py, FlowControlServerTest.py

Testing congestion adjustment by varying size of files in accordance to data loss. 
