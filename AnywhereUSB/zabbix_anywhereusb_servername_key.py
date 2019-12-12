#!/usr/bin/python
# encoding: utf-8
from pysnmp.hlapi import nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
import sys

community = "community" #changeme
#AnywhereUSB IP
device_ip = sys.argv[1]
#Server with key IP
connected_ip = "hostip_with_key" #changeme

#dictionary of all connections
connections = {}
#default result (no connections)
result = 0

#snmp walk for take all connections to keys and add in dictionary
for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in nextCmd(SnmpEngine(),
                          CommunityData(community, mpModel=1),
                          UdpTransportTarget((device_ip, 161)),
                          ContextData(),
                          ObjectType(ObjectIdentity("1.3.6.1.2.1.6.13.1.1")),
                          lexicographicMode=False):

    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        break
    else:
        for oid,value in varBinds:
            connections[str(oid)]=str(value)

#search for server ip in connections
for connect in connections:
    if connected_ip in connect:
        #if connection established return 5
        if connections[connect] == "5":
            result = 5
        #else return other value
        else:
            result = connections[connect]

print(result)

## 0 - no connections
##closed (1)
##listen (2)
##synSent (3)
##synReceived (4)
##established (5)
##finWait1 (6)
##finWait2 (7)
##closeWait (8)
##lastAck (9)
##closing (10)
##timeWait (11)
##deleteTCB (12)
