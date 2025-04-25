from rabbit import Rabbit
import time

rabbit = Rabbit(
    host   = "rabbitmq",
    port   = 5672,
    user   = "user",
    passwd = "password"
)

rabbit.declareQueues([
    "main_build_job",
    "priority_build_job"
])

for count in range(10):
    
    message = {
        "id": count,
        "message": "Hello from publisher!",
        "timestamp": time.time()
    }
    
    rabbit.publish(
        queue="main_build_job",
        message=message
    )
    
    print(f" [x] Sent { message }")
    count += 1
    time.sleep(2)