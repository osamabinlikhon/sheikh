import docker

def get_docker_client() -> docker.DockerClient:
    """Returns a Docker client."""
    return docker.from_env()
