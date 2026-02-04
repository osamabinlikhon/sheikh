#!/bin/bash

# Agent Sheikh Docker Buildx Cloud Builder Setup Script
# This script sets up Docker Buildx with cloud builder for the Agent Sheikh project

echo "🐳 Setting up Docker Buildx Cloud Builder for Agent Sheikh..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    echo "Please start Docker Desktop"
    exit 1
fi

echo "✅ Docker is available and running"

# Step 1: Create local instance of the cloud builder
echo "📦 Creating local instance of cloud builder..."
docker buildx create --driver cloud osamabinlikhon/sheikh

if [ $? -eq 0 ]; then
    echo "✅ Successfully created cloud builder instance"
else
    echo "❌ Failed to create cloud builder instance"
    exit 1
fi

# Step 2: Switch to the new builder
echo "🔄 Switching to cloud builder..."
docker buildx use cloud-osamabinlikhon-sheikh

if [ $? -eq 0 ]; then
    echo "✅ Successfully switched to cloud builder"
else
    echo "❌ Failed to switch to cloud builder"
    exit 1
fi

# Step 3: Verify builder is active
echo "🔍 Verifying active builder..."
docker buildx inspect

# Step 4: Build the Agent Sheikh project
echo "🏗️ Building Agent Sheikh project with cloud builder..."
echo "Note: First build may take longer as there's no performance data yet"

# Build the backend
echo "Building backend..."
docker buildx build --builder cloud-osamabinlikhon-sheikh -t agent-sheikh-backend:latest ./backend

# Build the frontend  
echo "Building frontend..."
docker buildx build --builder cloud-osamabinlikhon-sheikh -t agent-sheikh-frontend:latest ./frontend

# Build the sandbox
echo "Building sandbox..."
docker buildx build --builder cloud-osamabinlikhon-sheikh -t agent-sheikh-sandbox:latest ./sandbox

echo ""
echo "🎉 Docker Buildx cloud setup complete!"
echo ""
echo "📊 Note: As mentioned, there's no performance data initially."
echo "    After a few builds, you'll see performance metrics."
echo ""
echo "🚀 To run the complete stack:"
echo "   docker-compose up -d"
echo ""
echo "📖 To view build performance:"
echo "   docker buildx inspect --bootstrap"