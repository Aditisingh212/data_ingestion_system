from enum import IntEnum
import time
import uuid

class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

def get_priority_value(p: str):
    return Priority[p.upper()]

def generate_ingestion_id():
    return str(uuid.uuid4())
