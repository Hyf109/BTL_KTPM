import unittest
from health_monitor.services.external_api import check_external_api
from health_monitor.services.system import check_system_health

class TestServices(unittest.TestCase):
    def test_check_external_api(self):
        self.assertTrue(check_external_api("http://localhost:8001/exchange_rates"))

    def test_check_system_health(self):
        health = check_system_health()
        self.assertIn("status", health)
