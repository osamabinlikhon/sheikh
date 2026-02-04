#!/bin/bash

# Agent Sheikh Deployment Script
# This script handles deployment of the complete Agent Sheikh stack

set -e

# Configuration
DOCKER_USER="osamabinlikhon"
COMPOSE_FILE="docker-compose.yml"
PROD_COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking deployment prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    # Check environment file
    if [ ! -f "$ENV_FILE" ]; then
        log_warning "Environment file not found. Creating default..."
        create_env_file
    fi
    
    log_success "Prerequisites check passed"
}

# Create environment file
create_env_file() {
    cat > "$ENV_FILE" << EOF
# Agent Sheikh Environment Configuration
# Generated on $(date)

# LLM Configuration
API_KEY=u2nkaN5BxVlI0ZfxP1ELKTKZ8Oz9eomf
API_BASE=https://codestral.mistral.ai/v1
MODEL_NAME=codestral-latest
TEMPERATURE=0.7
MAX_TOKENS=2000

# Database Configuration
MONGODB_URI=mongodb://admin:admin123@mongodb:27017
MONGODB_DATABASE=agent_sheikh
MONGODB_USERNAME=admin
MONGODB_PASSWORD=admin123

# Cache Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Sandbox Configuration
SANDBOX_IMAGE=agent-sheikh-sandbox:latest
SANDBOX_NAME_PREFIX=sheikh-sandbox
SANDBOX_TTL_MINUTES=30
SANDBOX_NETWORK=agent-sheikh-network

# Authentication Configuration
AUTH_PROVIDER=password
PASSWORD_SALT=agentsheikh-salt
PASSWORD_HASH_ROUNDS=10
JWT_SECRET_KEY=agentsheikh-secret-key-change-in-production-\$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Application Configuration
DEBUG=false
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
MAX_AGENT_ITERATIONS=10

# Logging Configuration
LOG_LEVEL=INFO
EOF
    log_success "Environment file created"
}

# Pull latest images
pull_images() {
    log_info "Pulling latest Docker images..."
    
    # Pull from Docker Hub
    docker pull "$DOCKER_USER/agent-sheikh:latest" || log_warning "Failed to pull agent-sheikh image"
    docker pull "$DOCKER_USER/agent-sheikh-backend:latest" || log_warning "Failed to pull backend image"
    docker pull "$DOCKER_USER/agent-sheikh-frontend:latest" || log_warning "Failed to pull frontend image"
    docker pull "$DOCKER_USER/agent-sheikh-sandbox:latest" || log_warning "Failed to pull sandbox image"
    
    # Pull base images
    docker pull mongo:7.0
    docker pull redis:7.0-alpine
    
    log_success "Images pulled successfully"
}

# Build local images (if needed)
build_images() {
    log_info "Building local images..."
    
    # Build backend
    log_info "Building backend..."
    cd backend
    docker build -t "$DOCKER_USER/agent-sheikh-backend:latest" .
    cd ..
    
    # Build frontend
    log_info "Building frontend..."
    cd frontend
    docker build -t "$DOCKER_USER/agent-sheikh-frontend:latest" .
    cd ..
    
    # Build sandbox
    log_info "Building sandbox..."
    cd sandbox
    docker build -t "$DOCKER_USER/agent-sheikh-sandbox:latest" .
    cd ..
    
    log_success "Local images built successfully"
}

# Deploy the stack
deploy_stack() {
    local environment=${1:-development}
    
    log_info "Deploying Agent Sheikh stack in $environment mode..."
    
    if [ "$environment" = "production" ] && [ -f "$PROD_COMPOSE_FILE" ]; then
        COMPOSE_FILE="$PROD_COMPOSE_FILE"
        log_info "Using production compose file"
    fi
    
    # Stop existing services
    log_info "Stopping existing services..."
    docker-compose -f "$COMPOSE_FILE" down
    
    # Deploy services
    log_info "Starting services..."
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log_success "Agent Sheikh stack deployed successfully"
}

# Wait for services to be ready
wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for MongoDB
    log_info "Waiting for MongoDB..."
    timeout 60 bash -c 'until docker exec agent-sheikh-mongodb mongosh --eval "db.adminCommand(\"ping\")" >/dev/null 2>&1; do sleep 2; done'
    
    # Wait for Redis
    log_info "Waiting for Redis..."
    timeout 60 bash -c 'until docker exec agent-sheikh-redis redis-cli ping >/dev/null 2>&1; do sleep 2; done'
    
    # Wait for Backend
    log_info "Waiting for Backend..."
    timeout 60 bash -c 'until curl -f http://localhost:8000/health >/dev/null 2>&1; do sleep 2; done'
    
    # Wait for Frontend
    log_info "Waiting for Frontend..."
    timeout 60 bash -c 'until curl -f http://localhost:3000 >/dev/null 2>&1; do sleep 2; done'
    
    log_success "All services are ready"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Check backend
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        log_success "Backend is healthy"
    else
        log_error "Backend is not responding"
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        log_success "Frontend is healthy"
    else
        log_error "Frontend is not responding"
    fi
    
    # Check MongoDB
    if docker exec agent-sheikh-mongodb mongosh --eval "db.adminCommand(\"ping\")" >/dev/null 2>&1; then
        log_success "MongoDB is healthy"
    else
        log_error "MongoDB is not responding"
    fi
    
    # Check Redis
    if docker exec agent-sheikh-redis redis-cli ping >/dev/null 2>&1; then
        log_success "Redis is healthy"
    else
        log_error "Redis is not responding"
    fi
}

# Show status
show_status() {
    log_info "Agent Sheikh Stack Status:"
    echo ""
    docker-compose ps
    echo ""
    log_info "Service URLs:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo "  MongoDB: mongodb://localhost:27017"
    echo "  Redis: redis://localhost:6379"
}

# Cleanup
cleanup() {
    log_info "Cleaning up..."
    
    # Stop and remove containers
    docker-compose down -v
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused networks
    docker network prune -f
    
    log_success "Cleanup completed"
}

# Main deployment function
deploy() {
    local environment=${1:-development}
    local build_local=${2:-false}
    
    log_info "Starting Agent Sheikh deployment..."
    log_info "Environment: $environment"
    log_info "Build local: $build_local"
    
    check_prerequisites
    
    if [ "$build_local" = "true" ]; then
        build_images
    else
        pull_images
    fi
    
    deploy_stack "$environment"
    wait_for_services
    health_check
    show_status
    
    log_success "Agent Sheikh deployment completed successfully!"
    
    echo ""
    log_info "🎉 Agent Sheikh is now running!"
    log_info "📖 Visit http://localhost:3000 to access the application"
    log_info "📚 API docs available at http://localhost:8000/docs"
}

# Show usage
show_usage() {
    echo "Agent Sheikh Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  deploy [environment] [build-local]   Deploy the stack"
    echo "    environment: development (default), production"
    echo "    build-local: true (build images), false (pull images)"
    echo ""
    echo "  pull                             Pull latest images"
    echo "  build                            Build local images"
    echo "  stop                             Stop the stack"
    echo "  restart                          Restart the stack"
    echo "  status                           Show stack status"
    echo "  health                           Perform health check"
    echo "  logs                             Show logs"
    echo "  cleanup                          Clean up resources"
    echo ""
    echo "Examples:"
    echo "  $0 deploy                    # Deploy with pulled images"
    echo "  $0 deploy development true   # Deploy with locally built images"
    echo "  $0 deploy production         # Deploy to production"
    echo "  $0 status                   # Show current status"
    echo "  $0 logs                    # Show logs"
}

# Parse commands
case "${1:-deploy}" in
    "deploy")
        deploy "${2:-development}" "${3:-false}"
        ;;
    "pull")
        check_prerequisites
        pull_images
        ;;
    "build")
        check_prerequisites
        build_images
        ;;
    "stop")
        log_info "Stopping Agent Sheikh stack..."
        docker-compose down
        log_success "Stack stopped"
        ;;
    "restart")
        log_info "Restarting Agent Sheikh stack..."
        docker-compose restart
        log_success "Stack restarted"
        ;;
    "status")
        show_status
        ;;
    "health")
        health_check
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac