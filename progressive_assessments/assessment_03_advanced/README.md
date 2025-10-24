# Assessment #3: Containerized ML API (Advanced)

## 📋 Overview
**Time**: 10 minutes  
**Difficulty**: Advanced  
**Type**: Docker security & deployment debugging

## 🎯 Objective
Fix critical security issues and deployment problems in a containerized ML API. The application works but has serious production bugs in the Docker configuration.

## 🐛 What to Find
- **2 Critical bugs**: Major security issues (exposed secrets, security risks)
- **2 Subtle bugs**: Work but violate best practices (efficiency, monitoring)

**Important**: Multiple valid solutions exist for each bug - use your preferred approach!

## 📂 Files
- `Dockerfile` - Container definition (**has bugs - fix this**)
- `docker-compose.yml` - Orchestration config (**has bugs - fix this**)
- `model_api.py` - FastAPI application (working, no bugs here)
- `.env.example` - Environment template
- `test_container.sh` - Test script to identify bugs
- `requirements.txt` - Python dependencies

## 🚀 How to Complete This Assessment

### Step 1: Review Files (2-3 min)
```bash
# Read the Dockerfile and docker-compose.yml carefully
# Look for security issues, inefficiencies, missing configurations
```

### Step 2: Run Security Check (1 min)
```bash
# Make script executable
chmod +x test_container.sh

# Run tests to identify bugs
./test_container.sh
```

The test script will show:
- ❌ = Critical issue found
- ⚠️ = Subtle issue found
- ✓ = Configuration is correct

### Step 3: Fix Bugs (6-7 min)
Edit `Dockerfile` and `docker-compose.yml` to fix all issues.

**Remember**: Most bugs have multiple valid solutions - choose your preferred approach!

### Step 4: Verify Fixes
```bash
# Run tests again
./test_container.sh

# If Docker is installed, try building:
docker-compose build

# And running:
docker-compose up
```

## 💡 Tips

### For Security Issues
- Think about what's visible in:
  - Dockerfile ENV variables
  - docker-compose environment section
  - Docker image history
  - Container processes

### For Best Practices
- Consider:
  - Layer caching and build efficiency
  - Health checks for orchestrators
  - Resource limits
  - User permissions

### Multiple Solutions Exist!
Each bug can be fixed in different ways. For example:
- **Secrets**: env_file, build args, docker secrets, secret managers
- **Security**: dedicated user, distroless image, security context
- **Efficiency**: multi-stage builds, layer reordering, .dockerignore

## ✅ Success Criteria
- No exposed secrets in Dockerfile or docker-compose.yml
- Container doesn't run as root
- Efficient layer caching
- Health checks configured
- All tests show ✓ or no warnings

## 📊 What This Tests
- Docker security best practices
- Container optimization
- Production deployment knowledge
- Understanding of multiple solution approaches
- DevOps/MLOps skills

## 🔍 Categories of Bugs

### Critical (Must Fix)
1. **Exposed Secrets** - Hardcoded in Dockerfile/compose
2. **Security Risk** - Running as root user

### Subtle (Best Practices)
3. **Inefficient Build** - Poor layer caching
4. **Missing Monitoring** - No health checks

## 📝 Testing Without Docker

If you don't have Docker installed:
1. Review the code for issues
2. Run `./test_container.sh` (first 6 tests don't need Docker)
3. Explain your fixes verbally

## 🎯 Focus Areas

**Security** (Most Important):
- Never hardcode secrets
- Never run as root
- Use principle of least privilege

**Efficiency**:
- Optimize for build cache
- Minimize image size
- Fast rebuilds during development

**Production Readiness**:
- Health checks for orchestrators
- Resource limits
- Proper signal handling

Good luck! 🚀


