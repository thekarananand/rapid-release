import json
import subprocess
import threading
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://elasticsearch:9200",
    headers={
        "Content-Type": "application/json",
        "Accept":       "application/json"
    }
)

def logHandeler(stream, label):

    for line in stream:
        log_line = line.strip()
        print(f"[{label}] {log_line}")

        es.index(
            index="logs",
            document={
                "service": "runner",
                "stream": label,
                "message": log_line,
                "timestamp": datetime.utcnow()
            }
        )

def callback(channel, method, properties, body):
    try:
        message = json.loads(body.decode())
        print(f" [x] Received {message}")

        cwd = "/app/backend"
        command = ["docker", "build", "."]

        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        stdout_thread = threading.Thread(target=logHandeler, args=(process.stdout, "STDOUT"))
        stderr_thread = threading.Thread(target=logHandeler, args=(process.stderr, "STDERR"))

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        process.stdout.close()
        process.stderr.close()
        process.wait()

        # Ack AFTER everything succeeds
        channel.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error during processing: {e}")

    finally:
        try:
            channel.stop_consuming()
        except Exception as e:
            print(f"Error while stopping consumption cleanly: {e}")