# BUG #1 (CRITICAL): Exposed secrets in Dockerfile!
# API keys and secrets should NEVER be hardcoded
# Multiple solutions: build args, env vars, docker secrets, secret management

FROM python:3.11

WORKDIR /app

# BUG #1 (CRITICAL): Hardcoded secrets - MAJOR SECURITY ISSUE!
# These will be visible in docker history and image layers
ENV API_KEY="sk-prod-1234567890abcdef"
ENV DATABASE_PASSWORD="SuperSecret123!"
ENV JWT_SECRET="my-jwt-secret-key-2024"

# BUG #3 (SUBTLE): Inefficient layer caching
# Copying everything first means ANY file change rebuilds dependencies
# Should copy requirements.txt first, then install, then copy code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# BUG #2 (CRITICAL): Running as root user - SECURITY RISK!
# Container runs as root by default, should create non-root user
# If container is compromised, attacker has root access

# BUG #4 (SUBTLE): No health check defined
# Kubernetes/Docker can't detect if app is healthy
# Container might be "running" but app is crashed

EXPOSE 8000

# BUG: Still running as root!
CMD ["uvicorn", "model_api:app", "--host", "0.0.0.0", "--port", "8000"]


