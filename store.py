from collections import defaultdict
from threading import Lock

store = {}
queue = []  # (priority, timestamp, ingestion_id)
lock = Lock()
