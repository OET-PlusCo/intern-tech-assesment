#!/bin/bash

# Test script for containerized ML API
# This helps identify bugs in the Docker setup

echo "=================================="
echo "Container Security & Build Test"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "TEST 1: Check for exposed secrets in Dockerfile"
echo "================================================"
if grep -q "ENV.*SECRET\|ENV.*PASSWORD\|ENV.*KEY" Dockerfile; then
    echo -e "${RED}❌ CRITICAL: Secrets exposed in Dockerfile!${NC}"
    echo "   Found hardcoded secrets in ENV variables"
    grep "ENV.*SECRET\|ENV.*PASSWORD\|ENV.*KEY" Dockerfile | head -3
else
    echo -e "${GREEN}✓ No exposed secrets found in Dockerfile${NC}"
fi
echo ""

echo "TEST 2: Check if running as root"
echo "================================="
if grep -q "USER" Dockerfile; then
    echo -e "${GREEN}✓ Non-root user configured${NC}"
else
    echo -e "${RED}❌ CRITICAL: Container runs as root user!${NC}"
    echo "   This is a security risk"
fi
echo ""

echo "TEST 3: Check layer caching efficiency"
echo "======================================"
# Check if COPY . comes before pip install
COPY_LINE=$(grep -n "COPY \." Dockerfile | head -1 | cut -d: -f1)
PIP_LINE=$(grep -n "pip install" Dockerfile | head -1 | cut -d: -f1)

if [ ! -z "$COPY_LINE" ] && [ ! -z "$PIP_LINE" ] && [ $COPY_LINE -lt $PIP_LINE ]; then
    echo -e "${YELLOW}⚠️  SUBTLE: Inefficient layer caching${NC}"
    echo "   COPY . before pip install means cache breaks on any file change"
    echo "   Better: COPY requirements.txt, RUN pip install, then COPY ."
else
    echo -e "${GREEN}✓ Layer caching looks optimized${NC}"
fi
echo ""

echo "TEST 4: Check for health check"
echo "==============================="
if grep -q "HEALTHCHECK" Dockerfile; then
    echo -e "${GREEN}✓ Health check defined in Dockerfile${NC}"
else
    echo -e "${YELLOW}⚠️  SUBTLE: No HEALTHCHECK in Dockerfile${NC}"
    echo "   Orchestrators can't detect if app is healthy"
fi
echo ""

echo "TEST 5: Check docker-compose security"
echo "======================================"
if grep -q "API_KEY=\|PASSWORD=\|SECRET=" docker-compose.yml; then
    echo -e "${RED}❌ CRITICAL: Secrets exposed in docker-compose.yml!${NC}"
    echo "   Use env_file or docker secrets instead"
else
    echo -e "${GREEN}✓ No exposed secrets in docker-compose.yml${NC}"
fi
echo ""

echo "TEST 6: Check for resource limits"
echo "=================================="
if grep -q "resources:" docker-compose.yml; then
    echo -e "${GREEN}✓ Resource limits configured${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING: No resource limits set${NC}"
    echo "   Container can consume all host resources"
fi
echo ""

echo "TEST 7: Build the image (if Docker is available)"
echo "================================================="
if command -v docker &> /dev/null; then
    echo "Building image..."
    if docker build -t ml-api-test . > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Image builds successfully${NC}"
        
        # Check image size
        SIZE=$(docker images ml-api-test --format "{{.Size}}")
        echo "   Image size: $SIZE"
        
        # Check for exposed secrets in image
        echo ""
        echo "   Checking image history for secrets..."
        if docker history ml-api-test | grep -q "API_KEY\|PASSWORD\|SECRET"; then
            echo -e "${RED}   ❌ Secrets visible in image history!${NC}"
        else
            echo -e "${GREEN}   ✓ No secrets visible in image history${NC}"
        fi
        
        # Cleanup
        docker rmi ml-api-test > /dev/null 2>&1
    else
        echo -e "${RED}✗ Image build failed${NC}"
    fi
else
    echo "Docker not available, skipping build test"
fi
echo ""

echo "=================================="
echo "Summary"
echo "=================================="
echo "Review the warnings above to identify bugs."
echo "Focus on:"
echo "  1. Security issues (exposed secrets, root user)"
echo "  2. Best practices (health checks, resource limits)"
echo "  3. Efficiency (layer caching, image size)"
echo ""


