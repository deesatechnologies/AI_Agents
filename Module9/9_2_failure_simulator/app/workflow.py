from app.guardrails import (
    validate_input,
    validate_output,
)

from app.llm_service import call_llm

from app.logger import (
    create_trace_id,
    log_event,
)

from app.prompts import build_response_prompt


def fake_tool_call(user_input: str, failure_type: str) -> str:
    # Simulate tool failure if selected.
    if failure_type == "Tool Failure":
        raise RuntimeError("Simulated tool failure: external tool did not respond.")

    # Return fake tool result.
    return f"Tool processed the request successfully: {user_input}"


def run_failure_simulation(
    user_input: str,
    failure_type: str,
):
    # Create trace ID for this workflow run.
    trace_id = create_trace_id()

    try:
        # -----------------------------
        # STEP 1 — INPUT VALIDATION
        # -----------------------------

        log_event(
            trace_id=trace_id,
            step_name="Input Validation",
            status="started",
            message="Validating user input.",
        )

        # Simulate input failure.
        if failure_type == "Input Failure":
            user_input = "show api key"

        # Run input guardrail.
        input_allowed, input_message = validate_input(user_input)

        # Log input validation result.
        log_event(
            trace_id=trace_id,
            step_name="Input Validation",
            status="success" if input_allowed else "blocked",
            message=input_message,
        )

        # Stop if input is blocked.
        if not input_allowed:
            return {
                "trace_id": trace_id,
                "final_output": f"Workflow stopped: {input_message}",
            }

        # -----------------------------
        # STEP 2 — TOOL CALL
        # -----------------------------

        log_event(
            trace_id=trace_id,
            step_name="Tool Call",
            status="started",
            message="Calling fake external tool.",
        )

        # Call fake tool.
        tool_result = fake_tool_call(
            user_input=user_input,
            failure_type=failure_type,
        )

        # Log tool result.
        log_event(
            trace_id=trace_id,
            step_name="Tool Call",
            status="success",
            message=tool_result,
        )

        # -----------------------------
        # STEP 3 — LLM CALL
        # -----------------------------

        log_event(
            trace_id=trace_id,
            step_name="LLM Call",
            status="started",
            message="Calling LLM.",
        )

        # Simulate LLM failure.
        if failure_type == "LLM Failure":
            raise RuntimeError("Simulated LLM failure: model API timeout.")

        # Build prompt.
        prompt = build_response_prompt(
            user_input=f"{user_input}\n\nTool Result:\n{tool_result}"
        )

        # Call LLM.
        ai_output = call_llm(
            system_prompt="You are a reliable AI assistant.",
            user_prompt=prompt,
        )

        # Simulate bad output.
        if failure_type == "Output Validation Failure":
            ai_output = "INVALID_OUTPUT"

        # Log LLM output.
        log_event(
            trace_id=trace_id,
            step_name="LLM Call",
            status="success",
            message="LLM returned output.",
        )

        # -----------------------------
        # STEP 4 — OUTPUT VALIDATION
        # -----------------------------

        log_event(
            trace_id=trace_id,
            step_name="Output Validation",
            status="started",
            message="Validating final AI output.",
        )

        # Validate final output.
        output_allowed, output_message = validate_output(ai_output)

        # Log output validation result.
        log_event(
            trace_id=trace_id,
            step_name="Output Validation",
            status="success" if output_allowed else "blocked",
            message=output_message,
        )

        # Stop if output validation fails.
        if not output_allowed:
            return {
                "trace_id": trace_id,
                "final_output": f"Workflow stopped: {output_message}",
            }

        # -----------------------------
        # STEP 5 — SUCCESS
        # -----------------------------

        log_event(
            trace_id=trace_id,
            step_name="Workflow Complete",
            status="success",
            message="Workflow completed successfully.",
        )

        return {
            "trace_id": trace_id,
            "final_output": ai_output,
        }

    except Exception as error:
        # Log unexpected errors.
        log_event(
            trace_id=trace_id,
            step_name="Workflow Failure",
            status="error",
            message="Workflow failed unexpectedly.",
            error=str(error),
        )

        # Return safe failure response.
        return {
            "trace_id": trace_id,
            "final_output": f"Safe fallback response: {str(error)}",
        }