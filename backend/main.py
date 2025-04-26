from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from rabbit import Rabbit

# FastAPI Config
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RabbitMQ Config 
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

# Message Payload
class MessagePayload(BaseModel):
    project: str
    service: str
    env: str
    priory: bool = False

# FastAPI Routes
@app.get("/healthcheck")
def ping():
    return {"ping": "pong"}

@app.post("/")
def enqueue_message(payload: MessagePayload):
    message = {
        "project" : payload.project,
        "service" : payload.service,
        "env"     : payload.env
    }
    queue = f"{ 'priority' if payload.priory else 'main' }_build_job"
    
    try:
        rabbit.publish(
            queue   = queue,
            message = message
        )
        return {"status": "success", "queue": queue}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))