import time
import uuid


# In-memory log storage.
FAILURE_LOGS = []


def create_trace_id() -> str:
    # Create unique ID for each workflow run.
    return str(uuid.uuid4())


def log_event(
    trace_id: str,
    step_name: str,
    status: str,
    message: str,
    error: str = "",
):
    # Create one structured log event.
    event = {
        "trace_id": trace_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "step_name": step_name,
        "status": status,
        "message": message,
        "error": error,
    }

    # Store log event.
    FAILURE_LOGS.append(event)


def get_logs():
    # Return all logs.
    return FAILURE_LOGS


def clear_logs():
    # Clear previous logs.
    FAILURE_LOGS.clear()