import time


# Store evaluation history.
EVALUATION_LOGS = []


def log_evaluation(
    user_prompt: str,
    ai_output: str,
    evaluation_result: dict,
):
    # Store one evaluation entry.
    EVALUATION_LOGS.append(
        {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_prompt": user_prompt,
            "ai_output": ai_output,
            "overall_score": evaluation_result.get(
                "overall_score",
                0,
            ),
            "feedback": evaluation_result.get(
                "feedback",
                "",
            ),
        }
    )


def get_logs():
    # Return evaluation logs.
    return EVALUATION_LOGS


def clear_logs():
    # Clear previous logs.
    EVALUATION_LOGS.clear()