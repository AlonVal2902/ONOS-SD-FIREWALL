import http.client
import json
import base64

onos_ip = '172.17.0.5'
onos_port = 8181
onos_user = 'onos'
onos_password = 'rocks'


credentials = '{}:{}'.format(onos_user, onos_password)
encoded_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')
auth_header = 'Basic {}'.format(encoded_credentials)


def send_flow_rule(device_id, flow_rule):
    conn = http.client.HTTPConnection(onos_ip, onos_port)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
    }
    conn.request("POST", '/onos/v1/flows/{}'.format(device_id), json.dumps(flow_rule), headers)
    response = conn.getresponse()
    data = response.read().decode()
    conn.close()
    return data


flow_rule = {
    "priority": 40000,
    "timeout": 0,
    "isPermanent": True,
    "deviceId": "of:0000000000000001",
    "treatment": {
        "instructions": [
            {"type": "NOACTION"}
        ]
    },
    "selector": {
        "criteria": [
            {"type": "ETH_SRC", "mac": "00:00:00:00:00:01"},  
            {"type": "ETH_DST", "mac": "00:00:00:00:00:03"}   
        ]
    }
}


response = send_flow_rule("of:0000000000000001", flow_rule)
print("Respuesta de ONOS:", response)
