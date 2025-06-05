# Data Ingestion API

A RESTful API system for handling data ingestion requests with priority-based processing and rate limiting.

## Features

- Asynchronous batch processing
- Priority-based queue (HIGH, MEDIUM, LOW)
- Rate limiting (3 IDs per 5 seconds)
- Status tracking for ingestion requests
- Simulated external API calls

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Ingest Data
- **Endpoint**: POST /ingest
- **Input**:
```json
{
    "ids": [1, 2, 3, 4, 5],
    "priority": "HIGH"
}
```
- **Output**:
```json
{
    "ingestion_id": "abc123"
}
```

### 2. Check Status
- **Endpoint**: GET /status/{ingestion_id}
- **Output**:
```json
{
    "ingestion_id": "abc123",
    "status": "triggered",
    "batches": [
        {
            "batch_id": "uuid",
            "ids": [1, 2, 3],
            "status": "completed"
        }
    ]
}
```

## Running Tests

```bash
pytest test_app.py -v
```

## Design Choices

1. **Priority Queue**: Implemented using a list sorted by priority and timestamp
2. **Rate Limiting**: Enforced using sleep intervals between batch processing
3. **Status Tracking**: In-memory storage with thread-safe operations
4. **Batch Processing**: Asynchronous processing using background threads

## Status Codes

- **yet_to_start**: Initial state
- **triggered**: Processing has begun
- **completed**: All batches processed

## Priority Levels

- HIGH: Highest priority
- MEDIUM: Medium priority
- LOW: Lowest priority 