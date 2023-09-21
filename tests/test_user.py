import json

from . import BaseTestCase


class TestHandler(BaseTestCase):
    def test_register_user(self):
        response = self.fetch(
            "/user/register",
            method="POST",
            body=json.dumps(
                {
                    "email": "abc@example.com",
                    "password": "123456",
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        resp = json.loads(response.body)

        self.assertTrue(resp["data"]["access_token"] > 100)

    def test_signin_user(self):
        response = self.fetch(
            "/user/signin",
            method="POST",
            body=json.dumps(
                {
                    "email": "abc@example.com",
                    "password": "123456",
                }
            ),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        resp = json.loads(response.body)

        self.assertTrue(len(resp["data"]["access_token"]) > 100)
