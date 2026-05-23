import time
import uuid


# Store workflow traces in memory.
WORKFLOW_LOGS = []


def create_trace_id() -> str:
    # Generate unique workflow execution ID.
    return str(uuid.uuid4())


def log_event(
    trace_id: str,
    step_name: str,
    status: str,
    input_data=None,
    output_data=None,
    error_message=None,
    latency=None,
):
    # Create structured workflow event log.
    event = {
        "trace_id": trace_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "step_name": step_name,
        "status": status,
        "input_data": input_data,
        "output_data": output_data,
        "error_message": error_message,
        "latency_seconds": latency,
    }

    # Save event into workflow logs.
    WORKFLOW_LOGS.append(event)


def get_all_logs():
    # Return all workflow logs.
    return WORKFLOW_LOGS


def clear_logs():
    # Remove old logs.
    WORKFLOW_LOGS.clear()