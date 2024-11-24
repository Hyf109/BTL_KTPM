import unittest
from unittest.mock import patch
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
from services.container_status import ContainerAPI

class TestServices(unittest.TestCase):
    @patch('requests.get')
    def test_check_external_api(self, mock_get):
        """Kiểm tra trạng thái API bên ngoài."""
        mock_get.return_value.status_code = 200
        result = ExternalAPI.check_external_api("http://example.com")
        self.assertTrue(result)

        mock_get.return_value.status_code = 500
        result = ExternalAPI.check_external_api("http://example.com")
        self.assertFalse(result)

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_check_system_health(self, mock_memory, mock_cpu):
        """Kiểm tra trạng thái hệ thống."""
        mock_cpu.return_value = 20
        mock_memory.return_value.percent = 50

        result = SystemAPI.check_system_health()
        self.assertEqual(result['cpu_usage'], 20)
        self.assertEqual(result['memory_usage'], 50)
        self.assertEqual(result['status'], 'healthy')

    @patch('docker.DockerClient.containers')
    def test_check_docker_status(self, mock_containers):
        """Kiểm tra trạng thái container Docker."""
        mock_containers.get.return_value.status = "running"
        result = ContainerAPI.check_docker_status("test_container")
        self.assertTrue(result)

        mock_containers.get.side_effect = Exception("Container not found")
        result = ContainerAPI.check_docker_status("test_container")
        self.assertFalse(result)
