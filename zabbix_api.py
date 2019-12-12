import requests
import json

zabbix_user = "username" #changeme
zabbix_pass = "password" #changeme
zabbix_url = "http://hostname_or_ip/zabbix" #changeme
zabbix_api = zabbix_url + "/api_jsonrpc.php"
zabbix_api_key = "api_key" #changeme

headers = {
    'content-type': 'application/json',
}

#Get api version
def zabbix_get_api_version():
    data = {
    "jsonrpc": "2.0",
    "method": "apiinfo.version",
    "params": [],
    "id": 1
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    api_version = response.json()['result']
    return api_version

#Get api key (USERNAME, PASSWORD)
def zabbix_auth(zabbix_user, zabbix_pass):
    data = {
    "jsonrpc" : "2.0",
    "method" : "user.login",
    "params": {
      "user": zabbix_user,
      "password": zabbix_pass,
    },
    "auth" : None,
    "id" : 0,
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#Hosts
#Get all hosts
def zabbix_get_hosts():
    data = {
    "jsonrpc" : "2.0",
    "method" : "host.get",
    "params": {
        "output": [
            "hostid",
            "name"],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#Get hostid by hostname from Zabbix
def zabbix_get_host_id(host_name):
    data = {
    "jsonrpc" : "2.0",
    "method" : "host.get",
    "params": {
        "output": [
            "hostid",
            "name"],
        "filter": {
            "host": [ str(host_name) ]
          }
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result'][0]['hostid']

#Get hosts from group by groupid
def zabbix_get_hosts_by_group_id(group_id):
    data = {
    "jsonrpc" : "2.0",
    "method" : "host.get",
    "params": {
        "groupids": group_id,
        "output": [
            "hostid",
            "name"],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#Add new host (HOSTNAME for Zabbix, HOST IP, HOSTNAME)
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

#Host interfaces
#Get interfaces for host by hostid
def zabbix_get_host_interfaces(host_id):
    data = {
    "jsonrpc" : "2.0",
    "method" : "hostinterface.get",
    "params": {
        "hostids": host_id,
        "output": [
            "hostid",
            "ip",
            "dns",
            "port"],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#Get host interface id by hostid
def zabbix_get_host_interface_id(host_id):
    data = {
    "jsonrpc" : "2.0",
    "method" : "hostinterface.get",
    "params": {
        "hostids": host_id,
        "output": [
            "hostid",
            "ip",
            "dns",
            "port"],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result'][0]['interfaceid']

#Get interfaces for hosts in group by groupid
def zabbix_get_host_interfaces_by_group_id(group_id):
    data = {
    "jsonrpc" : "2.0",
    "method" : "hostinterface.get",
    "params": {
        "output": [
            "hostid",
            "ip"],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#Update host interface by (interfaceID, HOSTNAME, hostIP) for IP requests
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

#Update host interface by (interfaceEID, HOSTNAME, hostIP) for DNS requests
def zabbix_update_host_interface_use_dns(interface_id, host_name, host_ip):
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
        "useip": "0"
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()

#Maps
#Get maps
def zabbix_get_maps():
    data = {
    "jsonrpc" : "2.0",
    "method" : "map.get",
    "params": {
        "output": [
            "sysmapid",
            "name"],
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#Get map elements by map id
def zabbix_get_map_elements_by_id(map_id):
    data = {
    "jsonrpc" : "2.0",
    "method" : "map.get",
    "params": {
        "output": "extend",
        "selectSelements": "extend",
        "selectLinks": "extend",
        "selectUsers": "extend",
        "selectUserGroups": "extend",
        "selectShapes": "extend",
        "selectLines": "extend",
        "sysmapids": map_id
    },
    "auth" : zabbix_api_key,
    "id" : 2,
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']


#Update map by JSON DATA
"""
sample:

elements = []
for host in zabbix_get_hosts_by_group_id(18):
    name = host.get('name')
    host_id = host.get('hostid')
    element = {
        "label": name,
        "elementtype": 0,
        "iconid_off": 154,
        "iconid_on": 155,
        "iconid_disabled": 153,
        "elements": [
            {"hostid": host_id}]
        }
    elements.append(element)

data = {
    "jsonrpc": "2.0",
    "method": "map.update",
    "params": {
        "sysmapid": 2,
        "selements": [
            *elements,
      ],
    },
    "auth": zbx_api_key,
    "id": 2
    }
"""
def zabbix_map_update(data):
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()

#Graphs
#Get graphs
def zabbix_get_graphs():
    data = {
    "jsonrpc": "2.0",
    "method": "graph.get",
    "params": {
        "output": [
        "graphids",
        "name"],
    },
    "auth": zabbix_api_key,
    "id": 1
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#Images
#Get images
def zabbix_get_images():
    data = {
    "jsonrpc": "2.0",
    "method": "image.get",
    "params": {
        "output": [
        "imageids",
        "name"],
    },
    "auth": zabbix_api_key,
    "id": 1
    }
    response  = requests.post(zabbix_api, data=json.dumps(data), headers=headers)
    return response.json()['result']

#For print formated result
def format_result(func):
    return print(json.dumps(func, indent=4, sort_keys=True))
