import docker

client = docker.from_env()  # Kết nối với Docker daemon

class ContainerAPI:
    @staticmethod
    def check_docker_status(container_name):
        try:
            container = client.containers.get(container_name)
            return container.status == "running"
        except docker.errors.NotFound:
            return False