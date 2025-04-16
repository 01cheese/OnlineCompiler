import logging
import redis.asyncio as aioredis
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from celery_worker import execute_task
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://onlinecompiler-895n.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.post("/execute")
async def execute_code(request: dict, background_tasks: BackgroundTasks):
    """Accepts code, sends to Celery"""
    logging.info(f"Request receivd: {request}")

    print(request)

    task = execute_task.delay(request)
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == "PENDING":
        return {"status": "processing"}

    if task_result.state == "FAILURE":
        return JSONResponse(
            status_code=500,
            content={"status": "error", "output": str(task_result.result)}
        )

    if task_result.state == "SUCCESS":
        return task_result.result

    return {"status": task_result.state.lower()}


@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """WebSocket for Redis Pub/Sub"""
    await websocket.accept()

    redis = await aioredis.create_redis("redis://redis:6379/1")
    res = await redis.subscribe(f"task:{task_id}")
    ch = res[0]

    try:
        while await ch.wait_message():
            msg = await ch.get_json()
            await websocket.send_json(msg)
            break
    except Exception as e:
        await websocket.send_json({"status": "error", "output": f"WebSocket error: {str(e)}"})
    finally:
        await redis.unsubscribe(f"task:{task_id}")
        redis.close()
        await redis.wait_closed()
        await websocket.close()

