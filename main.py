from fastapi import FastAPI, HTTPException, BackgroundTasks
from models import IngestRequest, StatusResponse, BatchStatus
from utils import generate_ingestion_id
from store import store, queue, lock
from processor import process_batch
from uuid import uuid4
import time
from contextlib import asynccontextmanager

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Ingestion API"}

@app.post("/ingest")
async def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    ingestion_id = generate_ingestion_id()
    ids = request.ids
    priority = request.priority

    batches = []
    for i in range(0, len(ids), 3):
        batch = {
            "batch_id": str(uuid4()),
            "ids": ids[i:i+3],
            "status": "yet_to_start"
        }
        batches.append(batch)

    with lock:
        store[ingestion_id] = {
            "ingestion_id": ingestion_id,
            "status": "yet_to_start",
            "batches": batches,
            "created_time": time.time()
        }
        queue.append((priority, time.time(), ingestion_id))
        
        # Start processing the first batch
        if batches:
            background_tasks.add_task(process_batch, batches[0], ingestion_id)

    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}", response_model=StatusResponse)
def get_status(ingestion_id: str):
    with lock:
        if ingestion_id not in store:
            raise HTTPException(status_code=404, detail="Not found")

        record = store[ingestion_id]
        return {
            "ingestion_id": ingestion_id,
            "status": record["status"],
            "batches": record["batches"]
        }
