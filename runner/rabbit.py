import pika
import json
import time

class Rabbit:
    def __init__(self, host, port, user, passwd):
        self.host   = host
        self.port   = port
        self.user   = user
        self.passwd = passwd
        
        self.credentials = pika.PlainCredentials(
            username=self.user, 
            password=self.passwd
        )
        self.connection = self.connect()
        self.channel = self.connection.channel()
        
    def connect(self):
        attempt = 0
        while attempt < 10:
            try:
                print(f"🔌 Trying to connect to RabbitMQ ({self.host}:{self.port})... attempt {attempt + 1}")
                return pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.host,
                        port=self.port,
                        credentials=self.credentials
                    )
                )
            except pika.exceptions.AMQPConnectionError as e:
                print(f"❌ Connection failed: {e}")
                attempt += 1
                time.sleep(3)  # ⏱️ Add delay before retrying
        raise Exception("💥 Could not connect to RabbitMQ after multiple attempts.")
        
    def declareQueues(self, queues):
        for queue in queues:
            self.channel.queue_declare(queue=queue)
    
    def publish(self, queue, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message)
        )
    
    def onConsume(self, queue, callback):
        self.channel.basic_consume(
            queue=queue,
            on_message_callback=callback,
            auto_ack=True
        )
    
    def startConsuming(self):
        self.channel.start_consuming()
