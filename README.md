# GitHub Toolkit

An Arcade AI toolkit for interacting with GitHub repositories, pull requests, issues, and more.

## Features

- **Repository Management**: List recent repositories with filtering options
- **Branch Operations**: Create new branches from any base branch
- **File Management**: Commit changes to files (create or update)
- **Pull Requests**: Create pull requests and add comments
- **Issue Tracking**: Create issues with labels and assignees

## Installation

```bash
make install
```

## Tools

### `list_recent_repos`
List recent repositories the user has access to.

**Parameters:**
- `limit` (int): Maximum number of repositories to return (default: 10)
- `include_private` (bool): Whether to include private repositories (default: true)

**Returns:** List of repository information as JSON strings

### `create_branch`
Create a new branch in a repository.

**Parameters:**
- `repo_full_name` (str): Full name of the repository (owner/repo)
- `branch_name` (str): Name of the new branch to create
- `base_branch` (str, optional): Base branch to create from (defaults to repo's default branch)

**Returns:** JSON string with branch creation details

### `commit_changes`
Commit changes to a file in a repository.

**Parameters:**
- `repo_full_name` (str): Full name of the repository (owner/repo)
- `branch` (str): Branch name to commit to
- `file_path` (str): Path to the file in the repository
- `content` (str): New content of the file
- `commit_message` (str): Commit message describing the changes

**Returns:** JSON string with commit details

### `create_pull_request`
Create a pull request in a repository.

**Parameters:**
- `repo_full_name` (str): Full name of the repository (owner/repo)
- `title` (str): Title of the pull request
- `body` (str): Description of the pull request
- `head_branch` (str): Branch containing the changes
- `base_branch` (str, optional): Branch to merge into (defaults to repo's default branch)

**Returns:** JSON string with pull request details

### `create_issue`
Create an issue in a repository.

**Parameters:**
- `repo_full_name` (str): Full name of the repository (owner/repo)
- `title` (str): Title of the issue
- `body` (str): Description of the issue
- `labels` (list[str], optional): List of label names to apply
- `assignees` (list[str], optional): List of usernames to assign

**Returns:** JSON string with issue details

### `comment_on_pr`
Leave a comment on a pull request.

**Parameters:**
- `repo_full_name` (str): Full name of the repository (owner/repo)
- `pr_number` (int): Pull request number
- `comment` (str): Comment text to post

**Returns:** JSON string with comment details

## Authentication

All tools require GitHub authentication with appropriate scopes. The toolkit uses Arcade's built-in GitHub OAuth provider to handle authentication automatically.

Required scopes vary by tool:
- Repository operations: `repo`
- User operations: `read:user`, `user:email`
- Organization operations: `read:org`, `write:org`
- Pull requests: `pull_request`
- Issues: `issues`

## Development

### Running Tests
```bash
make test
```

### Type Checking
```bash
make check
```

### Building
```bash
make build
```

## License

This project is part of the Arcade AI ecosystem.