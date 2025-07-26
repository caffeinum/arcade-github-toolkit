# Arcade Deploy Configuration Guide

## Requirements
- Python 3.10+ 
- Arcade account
- Arcade CLI (`pip install arcade-ai`)

## Worker Configuration (`worker.toml`)

### Basic Structure
```toml
[[worker]]
[worker.config]
id = "my-example-worker"  # Unique worker identifier
enabled = true            # Optional worker status
timeout = 30              # Optional request timeout
retries = 3               # Optional connection retry attempts
secret = <your secret>    # Required unique secret
```

### Configuration Options

#### 1. Local Source Packages
```toml
[worker.local_source]
packages = ["./my_toolkit1", "./my_toolkit2"]
```

#### 2. PyPI Packages
```toml
[worker.pypi_source]
packages = ["arcade-math", "my-pypi-package"]
```

### Secrets Management
- Use environment variables: `secret = "${env: MY_ENVIRONMENT_SECRET}"`

## Deployment Commands
- Deploy worker: `arcade deploy`
- Deploy with local engine: `arcade deploy -h localhost -p 9099 --no-tls`
- View worker logs: `arcade logs my-example-worker`

## Key Tips
- Multiple workers can be configured in one `worker.toml`
- Default "dev" secret is not allowed
- Specify worker file with `-d` flag if not in current directory

## Recommended Practices
- Use unique, secure secrets
- Enable only necessary workers
- Set appropriate timeouts and retries
- Manage dependencies carefully