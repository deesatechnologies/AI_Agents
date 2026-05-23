import requests

from app.config import get_github_token

from app.guardrails import (
    is_allowed_file,
    sanitize_patch,
)


GITHUB_API_BASE_URL = "https://api.github.com"


#Creates the authentication and API headers required to securely communicate with GitHub APIs.
def get_github_headers() -> dict:
    
    return {
        "Authorization": f"Bearer {get_github_token()}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


#Fetches all changed files and code diffs from a GitHub Pull Request using GitHub APIs.
def fetch_pull_request_files(
    owner: str,
    repo: str,
    pull_number: int,
) -> list:
    # GitHub endpoint to list changed files in a PR.
    url = (
        f"{GITHUB_API_BASE_URL}/repos/"
        f"{owner}/{repo}/pulls/{pull_number}/files"
    )

    # Call GitHub API.
    response = requests.get(
        url,
        headers=get_github_headers(),
        timeout=30,
    )

    # Raise error if GitHub returns failure.
    response.raise_for_status()

    # Return list of changed files.
    return response.json()


#Builds one clean, sanitized combined code diff from all PR files to send to the AI reviewer.
def build_reviewable_diff(files: list) -> str:
    # Store formatted diff for AI review.
    diff_sections = []

    # Loop through changed files.
    for file in files:
        filename = file.get("filename", "")

        # GitHub may not include patch for binary/large files. patch: code difference. No code diff --> NO review
        patch = file.get("patch", "")

        # Skip files without patch.
        if not patch:
            continue

        # Skip blocked or unsupported files.
        if not is_allowed_file(filename):
            continue

        # Sanitize patch before sending to AI.
        safe_patch = sanitize_patch(patch)

        # Add formatted diff section.
        diff_sections.append(
            f"""
FILE: {filename}

PATCH:
{safe_patch}
"""
        )

    # Combine all file diffs.
    return "\n\n---\n\n".join(diff_sections)

#Posts the AI-generated review comment back to the GitHub Pull Request.
def post_pr_comment(
    owner: str,
    repo: str,
    pull_number: int,
    comment_body: str,
):
    # General PR conversation comments use Issues comments endpoint.
    # Every GitHub PR is also an issue.
    url = (
        f"{GITHUB_API_BASE_URL}/repos/"
        f"{owner}/{repo}/issues/{pull_number}/comments"
    )

    # Request body.
    payload = {
        "body": comment_body
    }

    # Post comment to GitHub PR.
    response = requests.post(
        url,
        headers=get_github_headers(),
        json=payload,
        timeout=30,
    )

    # Raise error if posting fails.

    if not response.ok:
        raise Exception(
            f"GitHub comment failed. "
            f"Status: {response.status_code}, "
            f"Response: {response.text}"
        )


    # Return GitHub API response.
    return response.json()