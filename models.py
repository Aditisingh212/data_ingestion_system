from pydantic import BaseModel, Field, validator
from typing import List, Literal
from uuid import UUID

class IngestRequest(BaseModel):
    ids: List[int] = Field(..., min_items=1)
    priority: Literal['HIGH', 'MEDIUM', 'LOW']

    @validator('ids')
    def validate_ids(cls, v):
        for id_ in v:
            if not 1 <= id_ <= 10**9 + 7:
                raise ValueError(f"ID {id_} must be between 1 and 10^9+7")
        return v

class BatchStatus(BaseModel):
    batch_id: UUID
    ids: List[int]
    status: Literal['yet_to_start', 'triggered', 'completed']

class StatusResponse(BaseModel):
    ingestion_id: str
    status: Literal['yet_to_start', 'triggered', 'completed']
    batches: List[BatchStatus]

