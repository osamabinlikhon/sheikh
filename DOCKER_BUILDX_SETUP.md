# Docker Buildx Cloud Builder Setup for Agent Sheikh

This guide helps you set up Docker Buildx with cloud builder for the Agent Sheikh project.

## Prerequisites

1. **Install Docker Desktop** from https://www.docker.com/products/docker-desktop
2. **Sign up for Docker Hub** if you haven't already
3. **Create a Docker Cloud Builder** at https://hub.docker.com/builders/cloud

## Quick Setup

### Option 1: Automated Script

Run the automated setup script:

```bash
chmod +x scripts/setup-cloud-builder.sh
./scripts/setup-cloud-builder.sh
```

### Option 2: Manual Steps

1. **Create local instance of cloud builder:**
```bash
docker buildx create --driver cloud osamabinlikhon/sheikh
```

2. **Switch to the cloud builder:**
```bash
docker buildx use cloud-osamabinlikhon-sheikh
```

3. **Build the project:**
```bash
docker buildx build --builder cloud-osamabinlikhon-sheikh .
```

## Building Agent Sheikh Components

### Build All Components

```bash
# Backend
docker buildx build --builder cloud-osamabinlikhon-sheikh -t agent-sheikh-backend:latest ./backend

# Frontend
docker buildx build --builder cloud-osamabinlikhon-sheikh -t agent-sheikh-frontend:latest ./frontend

# Sandbox
docker buildx build --builder cloud-osamabinlikhon-sheikh -t agent-sheikh-sandbox:latest ./sandbox
```

### Build with Multi-Platform Support

```bash
docker buildx build --builder cloud-osamabinlikhon-sheikh --platform linux/amd64,linux/arm64 -t agent-sheikh-backend:latest ./backend
```

## Performance Monitoring

### Initial Build

> **Note:** As mentioned in your message, there's no performance data initially for new cloud builders:
> "There is no performance data to be found as this linux-amd64 builder has not been used to build locally or in CI/CD within the last 30 days."

### After Building

After running several builds, you can view performance metrics:

```bash
# Inspect builder with performance data
docker buildx inspect --bootstrap

# View build history
docker buildx ls
```

## Complete Workflow

1. **Setup:**
```bash
docker buildx create --driver cloud osamabinlikhon/sheikh
docker buildx use cloud-osamabinlikhon-sheikh
```

2. **Build:**
```bash
docker buildx build --builder cloud-osamabinlikhon-sheikh . -t agent-sheikh:latest
```

3. **Deploy:**
```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **Docker not running:**
   - Start Docker Desktop
   - Check with `docker info`

2. **Authentication issues:**
   - Login with `docker login`
   - Verify builder permissions

3. **Build timeouts:**
   - Check internet connection
   - Verify cloud builder status

### Performance Tips

1. **Cache optimization:**
```bash
docker buildx build --builder cloud-osamabinlikhon-sheikh --cache-from type=registry,ref=your-username/cache:latest .
```

2. **Parallel builds:**
```bash
docker buildx build --builder cloud-osamabinlikhon-sheikh --parallel ./backend ./frontend ./sandbox
```

## Next Steps

After initial builds, the cloud builder will:
- Collect performance metrics
- Optimize build times
- Provide caching benefits
- Show detailed performance analytics

The more you use the cloud builder, the better performance data you'll see!