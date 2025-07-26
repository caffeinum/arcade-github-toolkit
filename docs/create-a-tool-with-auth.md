# Creating a Tool with Authentication in Arcade

## Prerequisites
- Set up Arcade
- Install Arcade SDK and required third-party SDKs
- Understand Tool Context

## Key Steps

### 1. Define Authorized Tool
```python
@tool(
    requires_auth=Slack(
        scopes=[
            "chat:write",
            "im:write",
            "users.profile:read",
            "users:read",
        ],
    )
)
def send_dm_to_user(
    context: ToolContext,
    user_name: str,
    message: str
) -> str:
    # Tool implementation
```

### 2. Authentication Methods
- Built-in providers (Slack, Google, GitHub)
- Custom OAuth2 provider
- Supports specifying scopes and provider ID

### 3. Tool Execution
```python
client = Arcade()
response = client.tools.execute(
    tool_name="Slack.SendDmToUser",
    input={
        "user_name": "johndoe",
        "message": "Hello!",
    },
    user_id=user_id,
)
```

## Key Concepts
- `requires_auth` decorator indicates authorization needed
- Arcade manages OAuth flow
- Tokens are stored and reused
- First-time use requires user permission

## Authorization Flow
- User is prompted to grant permissions via URL
- Application guides user through authorization
- Arcade remembers tokens to minimize repeated authorization

## Best Practices
- Specify minimal required scopes
- Handle potential authorization errors
- Guide users clearly through authentication process