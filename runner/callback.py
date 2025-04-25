import json

def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received { message }")