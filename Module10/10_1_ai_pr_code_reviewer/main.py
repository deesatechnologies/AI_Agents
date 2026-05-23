from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Request,
)

from app.config import get_github_webhook_secret

from app.github_service import (
    build_reviewable_diff,
    fetch_pull_request_files,
    post_pr_comment,
)

from app.guardrails import validate_combined_diff

from app.llm_service import call_llm

from app.prompts import build_code_review_prompt

from app.schemas import LocalReviewRequest

from app.webhook_security import verify_github_signature


# Create FastAPI app.
app = FastAPI(
    title="AI Pull Request Code Reviewer",
    description="AI tool that reviews GitHub Pull Requests and posts comments.",
    version="1.0.0",
)


#When someone opens the root URL using an HTTP GET request, run the function below it.
@app.get("/")
def home():
    # Simple health endpoint.
    return {
        "message": "AI PR Code Reviewer API is running."
    }


@app.get("/health")
def health():
    # Deployment health check.
    return {
        "status": "healthy"
    }


def review_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
    pr_title: str = "",
    pr_body: str = "",
    post_comment: bool = True,
):
    # Fetch changed files from GitHub PR.
    files = fetch_pull_request_files(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
    )

    # Build sanitized reviewable diff.
    diff_text = build_reviewable_diff(files)

    # Validate diff before sending to AI.
    allowed, message = validate_combined_diff(diff_text)

    # Stop if guardrail blocks diff.
    if not allowed:
        review_comment = f"""
# AI Code Review Skipped

Reason:
{message}
"""
        if post_comment:
            post_pr_comment(
                owner=owner,
                repo=repo,
                pull_number=pull_number,
                comment_body=review_comment,
            )

        return {
            "success": False,
            "message": message,
            "comment": review_comment,
        }

    # Build AI review prompt.
    user_prompt = build_code_review_prompt(
        repo_name=f"{owner}/{repo}",
        pr_title=pr_title,
        pr_body=pr_body,
        diff_text=diff_text,
    )

    # System prompt controls AI role.
    system_prompt = (
        "You are a careful senior software engineer performing code review."
    )

    # Call LLM to generate review.
    ai_review = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    # Add header so users know this is AI generated.
    comment_body = f"""
🤖 **AI Pull Request Review**

{ai_review}
"""

    # Post comment to GitHub PR if enabled.
    if post_comment:
        post_pr_comment(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
            comment_body=comment_body,
        )

    # Return result for debugging/testing.
    return {
        "success": True,
        "message": "AI review completed.",
        "comment": comment_body,
    }


#When someone sends an HTTP POST request to /local/test-review, run the function below it.
@app.post("/local/test-review")
def local_test_review(request: LocalReviewRequest):
    # This endpoint lets us test locally without GitHub webhook.
    return review_pull_request(
        owner=request.owner,
        repo=request.repo,
        pull_number=request.pull_number,
        pr_title="Local test PR",
        pr_body="Testing AI PR reviewer locally.",
        post_comment=request.post_comment,
    )


#When GitHub sends an HTTP POST webhook request to /github/webhook, run the function below it.
@app.post("/github/webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(default=""),
    x_hub_signature_256: str = Header(default=""),
):
    # Read raw request body.
    payload_body = await request.body()

    # Verify GitHub webhook signature.
    is_valid = verify_github_signature(
        payload_body=payload_body,
        signature_header=x_hub_signature_256,
        webhook_secret=get_github_webhook_secret(),
    )

    # Reject invalid webhook calls.
    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid GitHub webhook signature.",
        )

    # Parse JSON payload.
    payload = await request.json()

    # Only process pull_request events.
    if x_github_event != "pull_request":
        return {
            "message": f"Ignored event: {x_github_event}"
        }

    # Only review when PR is opened, reopened, synchronized, or ready for review.
    action = payload.get("action", "")

    allowed_actions = [
        "opened",
        "reopened",
        "synchronize",
        "ready_for_review",
    ]

    if action not in allowed_actions:
        return {
            "message": f"Ignored pull_request action: {action}"
        }

    # Extract PR details from webhook payload.
    repository = payload["repository"]
    pull_request = payload["pull_request"]

    owner = repository["owner"]["login"]
    repo = repository["name"]
    pull_number = pull_request["number"]
    pr_title = pull_request.get("title", "")
    pr_body = pull_request.get("body", "") or ""

    # Run AI review and post comment.
    result = review_pull_request(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
        pr_title=pr_title,
        pr_body=pr_body,
        post_comment=True,
    )

    # Return webhook response.
    return result