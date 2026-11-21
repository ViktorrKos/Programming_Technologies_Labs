import unittest

import xmlrunner

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_hello_world(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.decode("utf-8"),
            "Hello world from app! It is a Pipeline testing.",
        )

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_unknown_route_returns_404(self):
        response = self.client.get("/no-such-page")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    # Результати тестів зберігаються у test-reports/*.xml (їх читає крок junit у Jenkins)
    runner = xmlrunner.XMLTestRunner(output="test-reports")
    unittest.main(testRunner=runner)
