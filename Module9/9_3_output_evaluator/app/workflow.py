from app.evaluator import (
    calculate_average_score,
    parse_evaluation_response,
)

from app.llm_service import call_llm

from app.logger import log_evaluation

from app.prompts import (
    build_evaluation_prompt,
    build_generation_prompt,
)


def run_output_evaluation(user_prompt: str):
    # -----------------------------
    # STEP 1 — GENERATE AI OUTPUT
    # -----------------------------

    generation_prompt = build_generation_prompt(user_prompt)

    # Generate AI response.
    ai_output = call_llm(
        system_prompt="You are a professional AI assistant.",
        user_prompt=generation_prompt,
    )

    # -----------------------------
    # STEP 2 — EVALUATE OUTPUT
    # -----------------------------

    evaluation_prompt = build_evaluation_prompt(
        user_prompt=user_prompt,
        ai_output=ai_output,
    )

    # Ask evaluator LLM to score output.
    evaluation_response = call_llm(
        system_prompt="You are an expert AI evaluator.",
        user_prompt=evaluation_prompt,
    )

    # Parse evaluation JSON safely.
    parsed_result = parse_evaluation_response(
        evaluation_response
    )

   #get the value stored inside the "evaluation" key from the dictionary parsed_result
    evaluation = parsed_result["evaluation"]

    # -----------------------------
    # STEP 3 — CALCULATE FINAL SCORE
    # -----------------------------

    average_score = calculate_average_score(
        evaluation
    )

    # Add computed score.
    evaluation["calculated_average_score"] = average_score

    # -----------------------------
    # STEP 4 — STORE EVALUATION LOG
    # -----------------------------

    log_evaluation(
        user_prompt=user_prompt,
        ai_output=ai_output,
        evaluation_result=evaluation,
    )

    return {
        "ai_output": ai_output,
        "evaluation": evaluation,
    }