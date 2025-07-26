# Deploying Arcade Tools

## Requirements
- Python 3.10 or higher
- Arcade account
- Arcade CLI installed via `pip install arcade-ai`

## Deployment Steps

### 1. Create Configuration File
Create a `worker.toml` configuration file with:
- Worker ID
- Secret
- Local source package path

### 2. Deploy the Worker
```bash
arcade deploy
```

### 3. Verify Deployment
List workers to confirm deployment:
```bash
arcade worker list
```

## Configuration Example
```toml
[[worker]]
[worker.config]
id = "my-worker"
secret = <your secret>

[worker.local_source]
packages = ["./<your-toolkit-directory>"]
```

## Additional Notes
- Deployment creates a cloud-hosted endpoint for your toolkit
- Workers can be enabled/disabled through the dashboard
- Supports local toolkit deployment