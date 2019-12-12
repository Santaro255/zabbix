from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
import requests
import json
import socket

zabbix_url = "http://hostname_or_ip/zabbix" #changeme
zabbix_api = zabbix_url + "/api_jsonrpc.php"
zabbix_api_key = "api_key" #changeme
community = "community" #changeme

headers = {
    'content-type': 'application/json',
}

#get device model
def get_model(ip):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.25.3.2.1.3.1')))
    )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for oid,value in varBinds:
            return value

#get device name
def get_name(ip):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')))
    )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for oid,value in varBinds:
            return value

#get hostid from zabbix by hostname
def zabbix_get_host_id(host_name):
    data = {
    "jsonrpc" : "2.0",
    "method" : "host.get",
    "params": {
      'output': [
          'hostid',
          'name'],
      'filter': {
          'host': [ str(host_name) ]
          }
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result'][0]['hostid']

#get host interfaceid from zabbix by hostid
def zabbix_get_host_interface_id(host_id):
    data = {
    "jsonrpc" : "2.0",
    "method" : "hostinterface.get",
    "params": {
        'hostids': host_id,
      'output': [
          'hostid',
          'ip',
          'dns',
          'port'],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result'][0]['interfaceid']

#update interface for host in zabbix and select ip radio button
def zabbix_update_host_interface_use_ip(interface_id, host_name, host_ip):
    data = {
    "jsonrpc" : "2.0",
    "method" : "hostinterface.update",
    "params": {
        "interfaceid": interface_id,
        "dns": host_name,
        "ip": host_ip,
        "main": "1",
        "port": "161",
        "type": "2",
        "useip": "1"
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()

#get hosts from zabbix group
def zabbix_get_hosts_by_group_id(group_id):
    data = {
    "jsonrpc" : "2.0",
    "method" : "host.get",
    "params": {
        'groupids': group_id,
      'output': [
          'hostid',
          'name',
          ],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#add new host in zabbix
def zabbix_add_host(host_name, host_ip, host_dns):
    data = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": host_name,
        "interfaces": [
            {
                "type": 2,
                "main": 1,
                "useip": 1,
                "ip": host_ip,
                "dns": host_dns,
                "port": "161"
            }
        ],
        "groups": [
            {
                "groupid": "5"
            }
        ]
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#create hosts list
host_group = []
for host in zabbix_get_hosts_by_group_id(16):
    host_group.append(host['name'])

#enter your subnet like 10.10.10 or 192.168.0 or 172.1.2 etc 
net = 'REPLACE'

#from like 10.10.10.1 to 10.10.10.254
for second in range(1,255):
    print(str(net)+'.'+str(second))
    dev_model = get_model(str(net)+'.'+str(second))
    dev_ip = str(net)+'.'+str(second)
    dev_name = str(get_name(str(net)+'.'+str(second))).split(".")[0]
    if dev_name in host_group:
        if dev_name != "None":
            host_id = str(zabbix_get_host_id(dev_name))
            interface_id = str(zabbix_get_host_interface_id(host_id))
            print(zabbix_update_host_interface_use_ip(interface_id, dev_name, dev_ip))
    else:
        if (dev_model or dev_name) != "None":
            file = open("hosts_" + str(net) + ".log", "a", newline="")
            file.write(str(dev_model) + ";" + str(dev_ip) + ";" + str(dev_name))
            file.close()
            #uncomment below if you need to auto add new host in zabbix
            #print(zabbix_add_host(dev_name, dev_ip, dev_name))
