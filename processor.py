import time
import logging
from store import store, queue, lock

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_INTERVAL = 5  # seconds

def simulate_external_api(id_):
    try:
        time.sleep(1)  # simulate processing delay
        return {"id": id_, "data": "processed"}
    except Exception as e:
        logger.error(f"Error processing ID {id_}: {str(e)}")
        return {"id": id_, "data": "error", "error": str(e)}

async def process_batch(batch, ingestion_id):
    try:
        # Mark batch as triggered
        batch["status"] = "triggered"
        logger.info(f"Processing batch {batch['batch_id']} with IDs {batch['ids']}")

        # Process IDs in the batch
        for id_ in batch["ids"]:
            result = simulate_external_api(id_)
            if result.get("error"):
                logger.error(f"Failed to process ID {id_}: {result['error']}")

        # Mark batch as completed
        batch["status"] = "completed"
        logger.info(f"Completed batch {batch['batch_id']}")

        # Update ingestion status
        with lock:
            ingestion = store[ingestion_id]
            statuses = [b["status"] for b in ingestion["batches"]]
            if all(s == "completed" for s in statuses):
                ingestion["status"] = "completed"
            elif any(s == "triggered" for s in statuses):
                ingestion["status"] = "triggered"
            else:
                ingestion["status"] = "yet_to_start"

            # Process next batch if available
            next_batch = None
            for b in ingestion["batches"]:
                if b["status"] == "yet_to_start":
                    next_batch = b
                    break

            if next_batch:
                # Wait for rate limiting
                time.sleep(BATCH_INTERVAL)
                # Process next batch
                await process_batch(next_batch, ingestion_id)

    except Exception as e:
        logger.error(f"Error processing batch {batch['batch_id']}: {str(e)}")
        batch["status"] = "yet_to_start"  # Reset status on error
