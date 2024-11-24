import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from routes import routes

class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Khởi tạo ứng dụng Flask để kiểm thử."""
        self.app = Flask(__name__)
        self.app.register_blueprint(routes)
        self.client = self.app.test_client()

    @patch('services.external_api.ExternalAPI.check_external_api')
    @patch('services.system_api.SystemAPI.check_system_health')
    @patch('services.container_status.ContainerAPI.check_docker_status')
    def test_health_check(self, mock_check_docker_status, mock_check_system_health, mock_check_external_api):
        """Kiểm tra endpoint /health trả về dữ liệu chính xác."""
        
        # Mock dữ liệu
        mock_check_external_api.side_effect = [True, True]  # Gold và Exchange API
        mock_check_docker_status.side_effect = [True, True]  # Docker containers
        mock_check_system_health.return_value = {
            "status": "healthy",
            "cpu_usage": 20,
            "memory_usage": 40
        }

        # Gửi request GET
        response = self.client.get('/health')
        data = response.get_json()

        # Kiểm tra response status
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['gold_api'], 'connected')
        self.assertEqual(data['exchange_api'], 'connected')
        self.assertEqual(data['gold_docker'], 'running')
        self.assertEqual(data['exchange_docker'], 'running')
        self.assertEqual(data['system']['cpu_usage'], '20%')
        self.assertEqual(data['system']['memory_usage'], '40%')

    @patch('services.external_api.ExternalAPI.check_external_api')
    @patch('services.system_api.SystemAPI.check_system_health')
    @patch('services.container_status.ContainerAPI.check_docker_status')
    def test_health_check_unhealthy(self, mock_check_docker_status, mock_check_system_health, mock_check_external_api):
        """Kiểm tra trường hợp hệ thống không khỏe."""
        
        # Mock dữ liệu không khỏe
        mock_check_external_api.side_effect = [False, True]  # Gold API thất bại
        mock_check_docker_status.side_effect = [True, False]  # Một Docker container tắt
        mock_check_system_health.return_value = {
            "status": "unhealthy",
            "cpu_usage": 80,
            "memory_usage": 90
        }

        # Gửi request GET
        response = self.client.get('/health')
        data = response.get_json()

        # Kiểm tra response status
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['status'], 'unhealthy')
        self.assertEqual(data['gold_api'], 'disconnected')
        self.assertEqual(data['exchange_docker'], 'stopped')

    def test_history_data_structure(self):
        """Kiểm tra cấu trúc dữ liệu lịch sử."""
        from routes import history_data

        # Kiểm tra các key chính
        self.assertIn('timestamps', history_data)
        self.assertIn('cpu_usage', history_data)
        self.assertIn('memory_usage', history_data)
        self.assertIn('gold_api', history_data)
        self.assertIn('exchange_api', history_data)

