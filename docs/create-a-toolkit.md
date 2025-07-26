# Creating an Arcade Toolkit

## Prerequisites
- Arcade account
- uv package manager
- Python 3.13+

## Key Steps

### 1. Generate Toolkit Template
```bash
uv tool run --from arcade-ai arcade new arithmetic
```

### 2. Development Environment Setup
```bash
cd arithmetic
uv venv --seed -p 3.13
make install
```

### 3. Define Tools (Example: Math Operations)
```python
from arcade_tdk import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b
```

### 4. Testing
```bash
make test
make check
```

### 5. Local Testing
```bash
arcade serve
```

### 6. Deployment Options
- Local tunneling (ngrok/tailscale)
- Arcade cloud deployment
```bash
arcade deploy
```

### 7. Publishing to PyPI
```bash
make clean-build
make build
uv publish
```

## Key Recommendations
- Write comprehensive documentation
- Include example usage
- Maintain code quality
- Continuously test and evaluate tools

## Recommended Next Steps
- Add more complex tools
- Implement authentication
- Create evaluation suites
- Set up CI/CD pipelines