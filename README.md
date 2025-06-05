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
![Screenshot 2025-06-05 114828](https://github.com/user-attachments/assets/553af256-5e19-4f4f-bb02-7af2eccfc41d)

  ![Screenshot 2025-06![Screenshot 2025-06-05 114922](https://github.com/user-attachments/assets/a4e68de1-b8dd-4378-81c8-142b2eddb58b)
-05 114907](https://github.com/user-attachments/assets/4354f283-24b9-4ae5-ad28-8902c0676413)


![Screenshot 2025-06-05 114849](https://github.com/user-attachments/assets/46abc271-6089-4d49-8ad3-4b93019fb24d)
![Screenshot 2025-06-05 114828](https://github.com/user-attachments/assets/b1b1080b-b41f-4604-8e26-038c2315d85b)
