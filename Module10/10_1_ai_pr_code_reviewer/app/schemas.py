from pydantic import BaseModel

#defines the structure and validation rules for API request and response data.
class LocalReviewRequest(BaseModel):
    # Repository owner.
    owner: str

    # Repository name.
    repo: str

    # Pull request number.
    pull_number: int

    # Whether to actually post comment to GitHub.
    post_comment: bool = False