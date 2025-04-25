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

rabbit.onConsume(
    queue    = queue,
    callback = callback,
)

print(' [*] Waiting for build job....')
rabbit.startConsuming()