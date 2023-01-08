import unittest
import requests

from api.v1 import config as config
from api.v1.database import DatabaseClient as db
from utils import create_test_user, login, delete_user, random_text


class UnitTetsCases(unittest.TestCase):
    _test_user = None
    _token = None
    base_url = f"{config.SERVICE_BASE_URL}:{config.SERVICE_PORT}"

    def setup(self):
        # Create the test user and register it into the Users table
        self._test_user = create_test_user()

        # Log in with the test user and fetch the auth token
        response = login(self._test_user['name'], self._test_user['password'])
        self._token = response["access_token"]

    def shutdown(self):
        # Before shutting down, delete the test user and remove the record
        delete_user(self.test_user["_id"])

    def test_create_event(self):
        url = f"{self.base_url}/events"
        headers = {
            "Content-type": "text/json",
            "Authorization": self._token
        }
        body = {
            "name": f"TestName-{random_text(6)}",
            "details": f"TestDetails-{random_text(12)}",
            "event_type": "TestEventType",
        }
        response = requests.post(url=url, headers=headers, body=body)

        # Assert the api response is successful
        assert response.status == 200

        # Validate that the event was created
        created_event = db.database["events"].find_one({"name": body["name"]})

        assert created_event.name == body["name"]
        assert created_event.details == body["details"]
        assert created_event.event_type == body["event_type"]
        assert bool(created_event._id)


if __name__ == "__main__":
    unittest.main()
