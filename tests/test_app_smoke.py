import unittest

from app import create_app
from auth.models import User


class TestAppSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_public_pages_status_ok(self):
        for path in ["/", "/about", "/guide_game", "/statistics", "/login", "/register"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_default_language_is_english(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html lang="en">', response.data)

    def test_set_language_to_italian(self):
        response = self.client.get("/set-language/it?next=/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html lang="it">', response.data)
        self.assertIn("Guida".encode("utf-8"), response.data)

    def test_analytics_requires_authentication(self):
        # Ensure anonymous state before checking protected route.
        self.client.get("/clear")
        response = self.client.get("/analytics_data_analyst")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers.get("Location", ""))

    def test_analytics_page_for_developer(self):
        with self.app.app_context():
            developer = User.query.filter_by(email="developer@developer.com").first()
            self.assertIsNotNone(developer)
            developer_id = str(developer.id)

        with self.client.session_transaction() as session:
            session["_user_id"] = developer_id
            session["_fresh"] = True

        response = self.client.get("/analytics_data_analyst")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data Analyst Dashboard", response.data)


if __name__ == "__main__":
    unittest.main()
