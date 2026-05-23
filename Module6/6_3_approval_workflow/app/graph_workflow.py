from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm_service import call_llm

from app.prompts import build_risk_analysis_prompt

#State to be carried forward using ApprovalState class
class ApprovalState(TypedDict):
    # Original business request from the user.
    request_text: str

    # Risk level detected by AI.
    risk_level: str

    # Reason for the risk level.
    risk_reason: str

    # AI recommended action.
    recommended_action: str

    # Human decision entered from UI.
    human_decision: str

    # Final workflow result.
    final_result: str


def parse_risk_output(ai_text: str) -> dict:
    # Default values protect workflow if AI output is imperfect.
    parsed = {
        "risk_level": "Medium",
        "risk_reason": "Could not confidently determine risk.",
        "recommended_action": "Human Review",
    }

    # Split AI response into lines.
    lines = ai_text.splitlines()

    # Extract values from each line.
    for line in lines:
        if line.lower().startswith("risk level:"):
            parsed["risk_level"] = line.split(":", 1)[1].strip()

        elif line.lower().startswith("reason:"):
            parsed["risk_reason"] = line.split(":", 1)[1].strip()

        elif line.lower().startswith("recommended action:"):
            parsed["recommended_action"] = line.split(":", 1)[1].strip()

    return parsed


def risk_analysis_node(state: ApprovalState) -> dict:
    # Build prompt for AI risk analysis.
    prompt = build_risk_analysis_prompt(
        request_text=state["request_text"]
    )

    # System prompt controls AI behavior.
    system_prompt = "You are an enterprise risk analysis assistant."

    # Call LLM to analyze request risk.
    ai_output = call_llm(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    # Parse AI output into structured fields.
    parsed = parse_risk_output(ai_output)

    # Return partial state update.
    return {
        "risk_level": parsed["risk_level"],
        "risk_reason": parsed["risk_reason"],
        "recommended_action": parsed["recommended_action"],
    }


def auto_approve_node(state: ApprovalState) -> dict:
    # Create final result for low-risk auto-approved requests.
    final_result = f"""
# Approval Workflow Result

## Request
{state["request_text"]}

## Risk Level
{state["risk_level"]}

## Risk Reason
{state["risk_reason"]}

## Recommended Action
{state["recommended_action"]}

## Final Decision
Auto Approved

## Explanation
This request was classified as low risk, so the workflow approved it automatically.
"""

    return {
        "final_result": final_result
    }


def human_review_node(state: ApprovalState) -> dict:
    # This node marks that human approval is required.
    final_result = f"""
# Human Approval Required

## Request
{state["request_text"]}

## Risk Level
{state["risk_level"]}

## Risk Reason
{state["risk_reason"]}

## Recommended Action
{state["recommended_action"]}

## Status
Waiting for human approval.

Please choose Approve or Reject from the UI.
"""

    return {
        "final_result": final_result
    }


def final_decision_node(state: ApprovalState) -> dict:
    # Read human decision from state.
    decision = state["human_decision"]

    # Create final result after human decision.
    final_result = f"""
# Final Approval Decision

## Request
{state["request_text"]}

## Risk Level
{state["risk_level"]}

## Risk Reason
{state["risk_reason"]}

## Human Decision
{decision}

## Final Result
The request has been {decision.lower()} by the human reviewer.
"""

    return {
        "final_result": final_result
    }


def route_after_risk_analysis(state: ApprovalState) -> str:
    # Conditional routing based on AI risk level.

    risk = state["risk_level"].lower()

    # Low-risk requests can be auto-approved.
    if risk == "low":
        return "auto_approve"

    # Medium and high-risk requests require human review.
    return "human_review"


def build_initial_approval_graph():
    # Create graph for first phase:
    # risk analysis → auto approve OR human review.
    workflow = StateGraph(ApprovalState)

    # Add nodes.
    workflow.add_node("risk_analysis", risk_analysis_node)
    workflow.add_node("auto_approve", auto_approve_node)
    workflow.add_node("human_review", human_review_node)

    # Start with risk analysis.
    workflow.add_edge(START, "risk_analysis")

    # Route based on risk.
    workflow.add_conditional_edges(
        "risk_analysis",
        route_after_risk_analysis,
        {
            "auto_approve": "auto_approve",
            "human_review": "human_review",
        },
    )

    # End after either auto approval or human review request.
    workflow.add_edge("auto_approve", END)
    workflow.add_edge("human_review", END)

    return workflow.compile()


def build_final_decision_graph():
    # Create graph for second phase:
    # human decision → final result.
    workflow = StateGraph(ApprovalState)

    # Add final decision node.
    workflow.add_node("final_decision", final_decision_node)

    # Start directly with final decision node.
    workflow.add_edge(START, "final_decision")

    # End workflow.
    workflow.add_edge("final_decision", END)

    return workflow.compile()