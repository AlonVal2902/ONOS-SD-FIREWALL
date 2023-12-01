import http.client
import json
import base64

# Configuración de conexión a ONOS
onos_ip = '172.17.0.5'
onos_port = 8181
onos_user = 'onos'
onos_password = 'rocks'

# Codificación de credenciales
credentials = '{}:{}'.format(onos_user, onos_password)
encoded_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')
auth_header = 'Basic {}'.format(encoded_credentials)

# Función para enviar regla de flujo
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

# Direcciones MAC de los hosts a bloquear
blocked_macs = ["00:00:00:00:00:01", "00:00:00:00:00:02", "00:00:00:00:00:03"]

# Crear y enviar reglas de flujo para bloquear los hosts
for mac in blocked_macs:
    for i in range(1, 10):  # Para cada switch en la topología
        device_id = "of:000000000000000{}".format(i)
        # Bloquear tráfico desde la MAC
        flow_rule_src = {
            "priority": 50000,
            "timeout": 0,
            "isPermanent": True,
            "deviceId": device_id,
            "treatment": {
                "instructions": [
                    {"type": "NOACTION"}
                ]
            },
            "selector": {
                "criteria": [
                    {"type": "ETH_SRC", "mac": mac}
                ]
            }
        }
        # Bloquear tráfico hacia la MAC
        flow_rule_dst = {
            "priority": 50000,
            "timeout": 0,
            "isPermanent": True,
            "deviceId": device_id,
            "treatment": {
                "instructions": [
                    {"type": "NOACTION"}
                ]
            },
            "selector": {
                "criteria": [
                    {"type": "ETH_DST", "mac": mac}
                ]
            }
        }
        # Enviar las reglas
        send_flow_rule(device_id, flow_rule_src)
        send_flow_rule(device_id, flow_rule_dst)

print("Reglas enviadas para bloquear hosts h1x1, h2x1, y h3x1.")

