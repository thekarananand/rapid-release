import json
import subprocess
import threading

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

        def stream_output(stream, label):
            for line in stream:
                print(f"[{label}] {line.strip()}")

        stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, "STDOUT"))
        stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, "STDERR"))

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
        # Stop consuming ONLY after work is done
        try:
            channel.stop_consuming()
        except Exception as e:
            print(f"Error while stopping consumption cleanly: {e}")