import json


def parse_evaluation_response(response: str):
    # Try converting evaluator response into JSON.
    try:
        parsed = json.loads(response)

        return {
            "success": True,
            "evaluation": parsed,
        }

    except Exception as error:
        # Return parsing failure safely.
        return {
            "success": False,
            "evaluation": {
                "relevance": 0,
                "clarity": 0,
                "completeness": 0,
                "professionalism": 0,
                "hallucination_risk": 0,
                "overall_score": 0,
                "feedback": f"Evaluation parsing failed: {str(error)}",
            },
        }


def calculate_average_score(evaluation: dict):
    # Collect numeric evaluation scores.
    scores = [
        evaluation.get("relevance", 0),
        evaluation.get("clarity", 0),
        evaluation.get("completeness", 0),
        evaluation.get("professionalism", 0),
        evaluation.get("hallucination_risk", 0),
    ]

    # Return average score.
    return round(sum(scores) / len(scores), 2)