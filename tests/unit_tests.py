import datetime
import json
import logging
import sys
import unittest

import pytz
import requests
import testing_utils

from api.v1 import config
from api.v1.database import DatabaseClient as db

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel("INFO")

class UnitTestCases(unittest.TestCase):
    _test_user = None
    _token = None
    events_url = f"{config.SERVICE_BASE_URL}:{config.SERVICE_PORT}/events"

    def setUp(self):
        # Create the test user and register it into the Users table
        logger.info('Creating test user')
        self._test_user = testing_utils.create_test_user()
        logger.info(f'Created test user: {self._test_user["username"]}')

        # Log in with the test user and fetch the auth token
        response = testing_utils.login(self._test_user['username'], self._test_user['password'])
        logger.info(f"Logged in with test user: {self._test_user['username']}")
        self._token = response["access_token"]

    def tearDown(self):
        # Before shutting down, delete the test user and remove the record
        logger.info(f"Attempting to delete test user")
        testing_utils.delete_user(self._test_user["_id"])
        logger.info(f"Test user: {self._test_user['username']} successfully deleted!")
        

    def test_create_event(self):
        """Create an event with required data only"""
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self._token}",
            "Accept-Encoding": "gzip, deflate, br"
        }
        body = {
            "name": f"TestName-{testing_utils.random_text(6)}",
            "detail": f"TestDetails-{testing_utils.random_text(12)}",
            "event_type": "TestEventType",
        }
        logger.info("Attempting to create a new event with data:")
        logger.info(f"-- Event Name: {body['name']}")
        logger.info(f"-- Event Detail: {body['detail']}")
        logger.info(f"-- Event Type: {body['event_type']}")

        response = requests.post(url=self.events_url, headers=headers, data=json.dumps(body))
        
        # Assert the api response is successful
        self.assertEqual(response.status_code, 201, 
                         msg=f"Unexpected Status Code, expecting '200' got '{response.status_code}'. Message: {response._content}")
        logger.info("Event created!!")

        # Fetch the created event
        logger.info("Attempting to fetch created event from db...")
        created_event = db.get_db()["events"].find_one({"name": body["name"]})

        # Validate that the created event
        logger.info("Validating event request data against the event on the database")
        self.assertEqual(created_event['name'], body["name"])
        self.assertEqual(created_event['detail'], body["detail"])
        self.assertEqual(created_event['event_type'], body["event_type"])
        self.assertTrue(bool(created_event['_id']))

    def test_fetch_an_event(self):
        # Create an event on the database
        result = db.get_db()["events"].insert_one(
            {
                "name": f'TestFetchEvent-{testing_utils.random_text(6)}',
                "detail": f'TestDetail-{testing_utils.random_text(12)}',
                'event_type': 'TestEventType',
                'timestamp': str(datetime.datetime.now(pytz.utc))
            }
        )
        event = db.get_db()['events'].find_one({"_id": result.inserted_id})
        print(event)

        # Get the event from the request
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        response = requests.get(url=f"{self.events_url}/{event['_id']}", headers=headers)
        
        # Validate successful response
        self.assertEqual(response.status_code, 200, 
                         msg=f"Unexpected Status Code, expecting '200' got '{response.status_code}'. Message: {response._content}")

        # Validate the fields from the response
        fetched_event = response.json()
        self.assertEqual(fetched_event["name"], event["name"])
        self.assertEqual(fetched_event["detail"], event["detail"])
        self.assertEqual(fetched_event["event_type"], event["event_type"])





        

    

if __name__ == "__main__":
    unittest.main()
