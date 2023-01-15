# auditlogservice

## Overview
The `auditlogservice` is a microservice that allows for the `creation`, `retrieval`, and `deletion` of events from multiple sources. The service includes two main endpoints: the `token/` endpoint, which handles user authorization using the `OAuth2` protocol and returns a bearer token with a default expiration of 12 hours, and the `events/` endpoint, which allows for the creation and retrieval of events using the `GET`, `POST`, and `DELETE` request methods.

## Technical considerations

### Database
In terms of database choice, `mongoDB` was selected as a `NoSQL` database to store event data as documents. This allows easy horizontal scaling by initializing new instances and defining rules for evenly distributing data across instances. `SQL` databases were also considered, but it was determined that the dynamic structure of the `event_data` parameter would require serialization when storing and deserialization when fetching, and that the requirements did not need the use of `ACID` compliance.

### Backend
The backend of the service was developed using `PyDantic` for handling object models, `FastAPI` for handling requests and responses, and `Uvicorn` for running the server. `Uvicorn` was chosen for its compatibility with the `Asynchronous Server Gateway Interface (ASGI)` and backwards compatibility with `WSGI`, allowing for efficient handling of multiple incoming and outgoing events.

`FastAPI` was selected for its ability to handle requests asynchronously, its lightweight and high-performance nature, and its flexibility for maintenance. Other frameworks such as `Django` and `Flask` were considered, however, they did not provide the same level of performance and async support as `FastAPI`. This made `FastAPI` the best choice for the requirements of the service.

## Further considerations

In terms of future considerations, the service could benefit from the implementation of scoping to control user permission capabilities, such as allowing some users to only read events but not create or delete them. Additionally, smart event filtering could be implemented, such as the ability to filter by a range of dates or use partial matches or wildcards. Finally, the service could be configured to use multiple instances of `mongodb` for horizontal scaling.

## Deploying
The service can be deploying by using the command
```bash
$ docker-compose up --build
```
and a mock script for creating users directly on the `Users` table is included for testing purposes. In order to create a new user just execute:

```bash
$ python test/mock_script.py
```
and follow the instructions to register a new user in the database.

## Testing

### Unit testing

To run the unit tests for this service, follow these steps:

1. Install the necessary dependencies on your local machine.
2. Deploy the server as instructed in the `Deploying` section.
3. Execute the command:
```bash
$ python tests/unit_tests.py UnitTestCases 
```

### Functional testing

For functional testing, use the following instructions:

1. Ensure that the code has been deployed as instructed.
2. Execute the `mock_script.py` to create a user:
    ```bash
    $ python tests/mock_script.py
    ```
3. Follow the examples provided below for functional testing

#### Obtain an auth token

```bash
curl --location --request POST 'http://0.0.0.0:8080/token' \
--form 'username="<USERNAME>"' \
--form 'password="<PASSWORD>"'
```

example response:
```bash
{
    "access_token":"<AUTH_TOKEN>",
    "token_type":"bearer"
}
```
----
#### Create an event with required data only
```bash
curl --location --request POST 'http://0.0.0.0:8080/events' \
--header 'Authorization: Bearer <AUTH_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "<EVENT NAME>",
    "event_type": "<EVENT TYPE>",
    "detail": "<EVENT DETAIL>"
}'
```

example response:
```bash
{
    "name":"Some Event Name",
    "event_type":"Some Event Type",
    "detail":"Adding Some Event",
    "_id":"63c105beb78a3eaf4a440762",
    "timestamp":"2023-01-13T07:18:22.844000",
    "event_data":null
}  
```
 ----
#### Retrieve a list of events
  
```bash
curl --location --request GET 'http://0.0.0.0:8080/events' \
--header 'Authorization: Bearer <AUTH_TOKEN>'
```

example response:
```bash
[{"name":"EventName","event_type":"Some Event Type","detail":"Adding some Event","_id":"63c0a7f835205566abc6ee0e","timestamp":"2023-01-13T00:38:16.555000","event_data":null},{"name":"EventName","event_type":"Some Event Type","detail":"Adding some Event","_id":"63c0ee5fe84e0b8634928574","timestamp":"2023-01-13T05:38:39.148000","event_data":null},{"name":"EventName3","event_type":"Some Event Type","detail":"Adding some Event","_id":"63c0ee6be84e0b8634928575","timestamp":"2023-01-13T05:38:51.729000","event_data":null}]
```
----
#### Retrieve a single event


```bash
curl --location --request GET 'http://0.0.0.0:8080/events/<EVENT_ID>' \
--header 'Authorization: Bearer <AUTH_TOKEN>'
```

example response
```bash
{
    "name":"Some Event Name",
    "event_type":"Some Event Type",
    "detail":"Some Event Detail: Hello World!!",
    "_id":"63c30eeb347f3cc019fe0349",
    "timestamp":"2023-01-14T20:22:03.860000",
    "event_data":null
}
```
----
#### Retrieve events that match some criteria

```bash
curl --location --request GET 'http://0.0.0.0:8000/events?<FIELD>=<VALUE>' \
--header 'Authorization: Bearer <AUTH_TOKEN>'
```

example reponse:
```bash
curl --location --request GET 'http://0.0.0.0:8000/events?name=Some%20Event%20Name' \
--header 'Authorization: Bearer <AUTH_TOKEN>'


[{"name":"Some Event Name","event_type":"Some Event Type","detail":"Some Event Detail: Hello World!!","_id":"63c30eeb347f3cc019fe0349","timestamp":"2023-01-14T20:22:03.860000","event_data":null},{"name":"Some Event Name","event_type":"Some Event Type","detail":"Some Event Detail: Hello World!!","_id":"63c31048dee01b66b00b60a3","timestamp":"2023-01-14T20:27:52.873000","event_data":null}]
```
----
#### Delete an event

```bash
curl --location --request DELETE 'http://0.0.0.0:8000/events/<EVENT_ID>' \
--header 'Authorization: Bearer <AUTH_TOKEN>

```
