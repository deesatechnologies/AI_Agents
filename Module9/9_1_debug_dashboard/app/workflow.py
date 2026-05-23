import time

from app.guardrails import validate_user_input

from app.llm_service import call_llm

from app.logger import (
    create_trace_id,
    log_event,
)

from app.prompts import (
    build_analysis_prompt,
    build_summary_prompt,
)


async def run_debuggable_workflow(user_question: str):
    # Create unique trace ID for this workflow execution.
    trace_id = create_trace_id()

    # Track overall workflow start time.
    workflow_start = time.time()

    try:
        # -----------------------------
        # STEP 1 — INPUT VALIDATION
        # -----------------------------

        validation_start = time.time()

        allowed, message = validate_user_input(user_question)

        validation_latency = round(
            time.time() - validation_start,
            3,
        )

        # Log validation step.
        log_event(
            trace_id=trace_id,
            step_name="Input Guardrail Validation",
            status="success" if allowed else "blocked",
            input_data=user_question,
            output_data=message,
            latency=validation_latency,
        )

        # Stop workflow if blocked.
        if not allowed:
            return {
                "trace_id": trace_id,
                "final_output": f"Blocked: {message}",
            }

        # -----------------------------
        # STEP 2 — ANALYSIS STEP
        # -----------------------------

        analysis_prompt = build_analysis_prompt(user_question)

        analysis_start = time.time()

        analysis_output = call_llm(
            system_prompt="You are a business analysis assistant.",
            user_prompt=analysis_prompt,
        )

        analysis_latency = round(
            time.time() - analysis_start,
            3,
        )

        # Log analysis step.
        log_event(
            trace_id=trace_id,
            step_name="Question Analysis",
            status="success",
            input_data=analysis_prompt,
            output_data=analysis_output,
            latency=analysis_latency,
        )

        # -----------------------------
        # STEP 3 — FINAL RESPONSE
        # -----------------------------

        summary_prompt = build_summary_prompt(
            user_question=user_question,
            analysis=analysis_output,
        )

        summary_start = time.time()

        final_response = call_llm(
            system_prompt="You are a helpful business assistant.",
            user_prompt=summary_prompt,
        )

        summary_latency = round(
            time.time() - summary_start,
            3,
        )

        # Log final response generation.
        log_event(
            trace_id=trace_id,
            step_name="Final Response Generation",
            status="success",
            input_data=summary_prompt,
            output_data=final_response,
            latency=summary_latency,
        )

        # -----------------------------
        # STEP 4 — WORKFLOW COMPLETE
        # -----------------------------

        total_workflow_latency = round(
            time.time() - workflow_start,
            3,
        )

        # Log workflow completion.
        log_event(
            trace_id=trace_id,
            step_name="Workflow Complete",
            status="success",
            output_data="Workflow executed successfully.",
            latency=total_workflow_latency,
        )

        return {
            "trace_id": trace_id,
            "final_output": final_response,
        }

    except Exception as error:
        # Log unexpected workflow failure.
        log_event(
            trace_id=trace_id,
            step_name="Workflow Failure",
            status="error",
            error_message=str(error),
        )

        return {
            "trace_id": trace_id,
            "final_output": f"Workflow failed: {str(error)}",
        }