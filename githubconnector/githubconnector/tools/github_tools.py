from typing import List, Dict, Any, Optional, Annotated
from datetime import datetime, timezone
import json
from arcade_tdk import tool, ToolContext
from arcade_core.auth import GitHub
from github import Github, GithubException
from github.Repository import Repository
from github.PullRequest import PullRequest
from github.Issue import Issue


@tool(
    requires_auth=GitHub(
        scopes=[
            "repo",
            "read:org",
            "write:org",
            "read:user",
            "user:email",
        ]
    )
)
def list_recent_repos(
    context: ToolContext,
    limit: Annotated[int, "Maximum number of repositories to return"] = 10,
    include_private: Annotated[bool, "Whether to include private repositories"] = True,
) -> List[str]:
    """List recent repositories the user has access to."""
    if not context.authorization:
        raise ValueError("Authorization required")
    
    github = Github(context.authorization.token)
    user = github.get_user()
    
    repos: List[str] = []
    for repo in user.get_repos(sort="updated", direction="desc"):
        if len(repos) >= limit:
            break
        if not include_private and repo.private:
            continue

        # print(json.dumps(repo, indent=2))
            
        repos.append(json.dumps({
            "name": repo.name,
            "full_name": repo.full_name,
            # "description": repo.description,
            "private": repo.private,
            "url": repo.html_url,
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
            "language": repo.language,
            # "default_branch": repo.default_branch.,
        }))
    
    return repos


@tool(
    requires_auth=GitHub(
        scopes=["repo"]
    )
)
def create_branch(
    context: ToolContext,
    repo_full_name: Annotated[str, "Full name of the repository (owner/repo)"],
    branch_name: Annotated[str, "Name of the new branch to create"],
    base_branch: Annotated[Optional[str], "Base branch to create from (defaults to repo's default branch)"] = None,
) -> str:
    """Create a new branch in a repository."""
    if not context.authorization:
        raise ValueError("Authorization required")
    
    github = Github(context.authorization.token)
    repo = github.get_repo(repo_full_name)
    
    if base_branch is None:
        base_branch = repo.default_branch
    
    base_ref = repo.get_branch(base_branch)
    repo.create_git_ref(f"refs/heads/{branch_name}", base_ref.commit.sha)
    
    return json.dumps({
        "branch_name": branch_name,
        "base_branch": base_branch,
        "created": True,
        "url": f"{repo.html_url}/tree/{branch_name}",
    })


@tool(
    requires_auth=GitHub(
        scopes=["repo"]
    )
)
def commit_changes(
    context: ToolContext,
    repo_full_name: Annotated[str, "Full name of the repository (owner/repo)"],
    branch: Annotated[str, "Branch name to commit to"],
    file_path: Annotated[str, "Path to the file in the repository"],
    content: Annotated[str, "New content of the file"],
    commit_message: Annotated[str, "Commit message describing the changes"],
) -> str:
    """Commit changes to a file in a repository."""
    if not context.authorization:
        raise ValueError("Authorization required")
    
    github = Github(context.authorization.token)
    repo = github.get_repo(repo_full_name)
    
    try:
        contents = repo.get_contents(file_path, ref=branch)
        # get_contents can return a list if path is a directory
        if isinstance(contents, list):
            raise ValueError(f"{file_path} is a directory, not a file")
        
        result = repo.update_file(
            path=file_path,
            message=commit_message,
            content=content,
            sha=contents.sha,
            branch=branch,
        )
    except GithubException:
        result = repo.create_file(
            path=file_path,
            message=commit_message,
            content=content,
            branch=branch,
        )
    
    return json.dumps({
        "file_path": file_path,
        "commit_sha": result["commit"].sha,
        "commit_message": commit_message,
        "branch": branch,
        "url": result["content"].html_url,
    })


@tool(
    requires_auth=GitHub(
        scopes=["repo", "pull_request"]
    )
)
def create_pull_request(
    context: ToolContext,
    repo_full_name: Annotated[str, "Full name of the repository (owner/repo)"],
    title: Annotated[str, "Title of the pull request"],
    body: Annotated[str, "Description of the pull request"],
    head_branch: Annotated[str, "Branch containing the changes"],
    base_branch: Annotated[Optional[str], "Branch to merge into (defaults to repo's default branch)"] = None,
) -> str:
    """Create a pull request in a repository."""
    if not context.authorization:
        raise ValueError("Authorization required")
    
    github = Github(context.authorization.token)
    repo = github.get_repo(repo_full_name)
    
    if base_branch is None:
        base_branch = repo.default_branch
    
    pr = repo.create_pull(
        title=title,
        body=body,
        head=head_branch,
        base=base_branch,
    )
    
    return json.dumps({
        "number": pr.number,
        "title": pr.title,
        "url": pr.html_url,
        "state": pr.state,
        "created_at": pr.created_at.isoformat(),
        "head_branch": head_branch,
        "base_branch": base_branch,
    })


@tool(
    requires_auth=GitHub(
        scopes=["repo", "issues"]
    )
)
def create_issue(
    context: ToolContext,
    repo_full_name: Annotated[str, "Full name of the repository (owner/repo)"],
    title: Annotated[str, "Title of the issue"],
    body: Annotated[str, "Description of the issue"],
    labels: Annotated[Optional[List[str]], "List of label names to apply"] = None,
    assignees: Annotated[Optional[List[str]], "List of usernames to assign"] = None,
) -> str:
    """Create an issue in a repository."""
    if not context.authorization:
        raise ValueError("Authorization required")
    
    github = Github(context.authorization.token)
    repo = github.get_repo(repo_full_name)
    
    issue = repo.create_issue(
        title=title,
        body=body,
        labels=labels or [],
        assignees=assignees or [],
    )
    
    return json.dumps({
        "number": issue.number,
        "title": issue.title,
        "url": issue.html_url,
        "state": issue.state,
        "created_at": issue.created_at.isoformat(),
        "labels": [label.name for label in issue.labels],
        "assignees": [user.login for user in issue.assignees],
    })


@tool(
    requires_auth=GitHub(
        scopes=["repo", "pull_request"]
    )
)
def comment_on_pr(
    context: ToolContext,
    repo_full_name: Annotated[str, "Full name of the repository (owner/repo)"],
    pr_number: Annotated[int, "Pull request number"],
    comment: Annotated[str, "Comment text to post"],
) -> str:
    """Leave a comment on a pull request."""
    if not context.authorization:
        raise ValueError("Authorization required")
    
    github = Github(context.authorization.token)
    repo = github.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)
    
    comment_obj = pr.create_issue_comment(comment)
    
    return json.dumps({
        "comment_id": comment_obj.id,
        "pr_number": pr_number,
        "comment": comment,
        "created_at": comment_obj.created_at.isoformat(),
        "url": comment_obj.html_url,
    })