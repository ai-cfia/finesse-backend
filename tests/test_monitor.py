import unittest

from app.app_creator import create_app


class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.app = create_app({})
        self.client = self.app.test_client()

    def test_health_route(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "ok")


if __name__ == "__main__":
    unittest.main()
