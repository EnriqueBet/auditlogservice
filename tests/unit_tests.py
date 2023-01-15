import json
import unittest

import requests
import testing_utils

from api.v1 import config
from api.v1.database import DatabaseClient as db
from api.v1.utils.logger import Logger

logger = Logger.get_instance()

class UnitTestCases(unittest.TestCase):
    _test_user = None
    _token = None
    events_url = f"{config.SERVICE_BASE_URL}:{config.SERVICE_PORT}/events"

    def setUp(self):
        # Create the test user and register it into the Users table
        logger.info(f"------- Starting test: '{self._testMethodName}' -------")
        self._test_user = testing_utils.create_test_user()

        # Log in with the test user and fetch the auth token
        response = testing_utils.login(self._test_user['username'], self._test_user['password'])
        logger.info(f"Logged in with test user: {self._test_user['username']}")
        self._token = response["access_token"]

    def tearDown(self):
        # Before shutting down, delete the test user and remove the record
        logger.info(f"Attempting to delete test user")
        testing_utils.delete_user(self._test_user["_id"])
        logger.info(f"Test user: {self._test_user['username']} successfully deleted!")
        logger.info(f"------- Finalizing test: '{self._testMethodName}' -------\n")
        

    def test_create_event(self):
        """Validate that an event is created with required data only"""
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self._token}",
            "Accept-Encoding": "gzip, deflate, br"
        }
        body = {
            "name": f"TestName-{testing_utils.random_text()}",
            "detail": f"TestDetails-{testing_utils.random_text(length=12)}",
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
        """Validate that an event can be fetched"""
        # Create an event on the database
        event = testing_utils.create_an_event()

        # Get the event from the request
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        logger.info(f"Attempting to fetch event {event['_id']} via API...")
        response = requests.get(url=f"{self.events_url}/{event['_id']}", headers=headers)
        
        # Validate successful response
        self.assertEqual(response.status_code, 200, 
                         msg=f"Unexpected Status Code, expecting '200' got '{response.status_code}'. Message: {response._content}")

        # Validate the fields from the response
        fetched_event = response.json()
        logger.info("Validating API fetched data against the one stored on the db")
        self.assertEqual(fetched_event["name"], event["name"])
        self.assertEqual(fetched_event["detail"], event["detail"])
        self.assertEqual(fetched_event["event_type"], event["event_type"])

    def test_delete_an_event(self):
        """Validate that an event can be deleted by the user"""
        # Create an event on the database
        event = testing_utils.create_an_event()

        # Attempt to delete the event
        headers = {"Authorization": f"Bearer {self._token}"}
        logger.info(f"Attempting to delete event with id: {event['_id']}")
        response = requests.delete(url=f"{self.events_url}/{event['_id']}", headers=headers)

        # Validate that request was successful
        self.assertEqual(response.status_code, 204, 
                         msg=f"Unexpected Status Code, expecting '204' got '{response.status_code}'. Message: {response._content}")
        
        # Validate that the event can't be found on the database
        logger.info("Validating that the event is not found on the db")
        deleted_event = db.get_db()["events"].find_one({"_id": event['_id']})
        self.assertFalse(bool(deleted_event))

    def test_fetch_created_events(self):
        """Validate that multiple created events are fetched"""
        # Create multiple events on the database
        logger.info("Attempting to create 3 events on the database....")
        events = [testing_utils.create_an_event() for _ in range(3)]

        # Fetch all the testing events on the database
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(url=self.events_url, 
                                headers=headers,
                                params={"event_type": "TestEventType"})
        fetched_event_ids = [event['_id'] for event in response.json()]
        
        # Validate that the request was successful
        self.assertEqual(response.status_code, 200, 
                         msg=f"Unexpected Status Code, expecting '200' got '{response.status_code}'. Message: {response._content}")

        # Validate that the created events are fetched
        logger.info("Validate if the created events are fetched from the API")
        for event in events:
            result = str(event['_id']) in fetched_event_ids
            logger.info(f"event {event['_id']} in fetched events: {result}")
            self.assertTrue(result, msg=f"Event {event['_id']} not found in fetched events")
        
    

if __name__ == "__main__":
    unittest.main()
