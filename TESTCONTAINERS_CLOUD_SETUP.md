# Testcontainers Cloud Setup Guide for Agent Sheikh

## 🔐 Required GitHub Secrets

Add these secrets to your GitHub repository:

### Testcontainers Cloud
- **TC_CLOUD_TOKEN**: `aj_tcc_svc_8rdaYX5EYLZWfAdHGhjalBckbGMKFInw9YJgldc1BKEFA`

### Docker Hub
- **DOCKER_PAT**: `dckr_pat_XGiAJvYKWaLT3YjyEk7AY9G3eyo`

### Repository Variables
Set these in GitHub repository settings > Variables:
- **DOCKER_USER**: `osamabinlikhon`

## 🚀 Quick Setup

### 1. Docker Login (Local Development)
```bash
docker login -u osamabinlikhon
# At password prompt, enter: dckr_pat_XGiAJvYKWaLT3YjyEk7AY9G3eyo
```

### 2. Testcontainers Cloud Configuration
The workflow automatically configures:
- Testcontainers Cloud token
- Multi-platform builds (linux/amd64,linux/arm64)
- Agent specifications (2 CPU, 4Gi memory)
- Auto-removal of agents

## 📋 GitHub Actions Workflow Features

### Jobs Overview

1. **test**: Runs unit tests with Testcontainers Cloud
2. **docker**: Builds and pushes images using Testcontainers Cloud
3. **integration-test**: Runs integration tests on built images

### Key Features

- ✅ Testcontainers Cloud integration
- ✅ Multi-platform builds (AMD64 + ARM64)
- ✅ SBOM and Provenance generation
- ✅ GitHub Actions cache optimization
- ✅ Automated testing and integration checks
- ✅ Performance metrics collection

## 🏗️ Build Targets

The workflow builds these images:
- `osamabinlikhon/agent-sheikh:latest`
- `osamabinlikhon/agent-sheikh-backend:latest`
- `osamabinlikhon/agent-sheikh-frontend:latest`
- `osamabinlikhon/agent-sheikh-sandbox:latest`

## 📊 Testcontainers Cloud Benefits

### Performance Optimization
- Cloud-based build agents
- Parallel build execution
- Optimized caching
- Performance metrics collection

### Security
- Isolated build environments
- Secure token management
- No local Docker daemon required

### Scalability
- Multi-platform builds
- Concurrent test execution
- Resource optimization

## 🔧 Configuration Details

### Testcontainers Cloud Settings
```yaml
TC_CLOUD_TOKEN: ${{ secrets.TC_CLOUD_TOKEN }}
TESTCONTAINERS_CLOUD_ENABLED: true
TC_CLOUD_AGENT_AUTO_REMOVE: true
TC_CLOUD_AGENT_CPU: 2
TC_CLOUD_AGENT_MEMORY: 4Gi
```

### Buildx Configuration
```yaml
driver: cloud
endpoint: "osamabinlikhon/sheikh"
platforms: linux/amd64,linux/arm64
```

## 🚀 Usage

### Trigger Builds
```bash
# Push to main branch
git push origin main

# Or create a pull request
git checkout -b feature/new-feature
git push origin feature/new-feature
# Create PR on GitHub
```

### Monitor Progress
1. **GitHub Actions**: Watch workflow progress in Actions tab
2. **Testcontainers Cloud**: Check performance metrics in dashboard
3. **Docker Hub**: Verify built images in repository

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication failures**:
   - Verify TC_CLOUD_TOKEN is correct
   - Check DOCKER_PAT is valid
   - Ensure DOCKER_USER is set correctly

2. **Build timeouts**:
   - Check Testcontainers Cloud status
   - Verify network connectivity
   - Review agent resource limits

3. **Test failures**:
   - Check service dependencies (MongoDB, Redis)
   - Verify environment variables
   - Review test logs

### Debug Commands

```bash
# Test local Docker setup
docker run --rm hello-world

# Verify Testcontainers Cloud token
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.testcontainers.cloud/v1/health

# Check GitHub Actions logs
# Go to repository > Actions > Select workflow run
```

## 📈 Performance Metrics

After initial builds, Testcontainers Cloud will provide:
- Build time analytics
- Resource usage statistics
- Cache efficiency metrics
- Performance improvements over time

## 🎯 Next Steps

1. **Configure GitHub secrets** with provided tokens
2. **Set repository variables** for Docker username
3. **Test workflow** by pushing to main branch
4. **Monitor performance** in Testcontainers Cloud dashboard
5. **Optimize builds** based on collected metrics

Your Agent Sheikh project is now ready for Testcontainers Cloud! 🚀