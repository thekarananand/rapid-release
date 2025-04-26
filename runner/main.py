from rabbit import Rabbit
from callback import callback

rabbit = Rabbit(
    host   = "rabbitmq",
    port   = 5672,
    user   = "user",
    passwd = "password"
)

queue = "main_build_job"

rabbit.declareQueues([
    queue
])

rabbit.consume(
    queue    = queue,
    callback = callback,
)