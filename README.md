# auditlogservice

## Overview
The `auditlogservice` is a microservice that can `create`, `retrieve`, and `delete` events coming from multiple services. This service includes two endpoints:

- `token/`
- `events/`

The `token/` endpoint takes care of authorization by implementing an `OAuth2` protocol tha receives the `credentials` from the user and returns a `bearer token` with a default expiration of 12 hours. 

The `events/` endpoint is used to create and retrieve events created from other services. It has implemented the request methods `GET`, `POST`, and `DELETE`

## Techical considerations

### Database
I decided to use `mongoDB` a `NoSQL` database to facilitate the storage of not well defined `event_data` as documents. Also, `mongoDB` allows to easily escalate horizontally by initializing new instances and define rules to store the data evenly across instances.

On the other hand, I also considered using a `SQL` schema for the database. The tradeoffs of using `SQL` were:

* The `event_data` parameter doesn't have a dynamic structure and the requirements doensn't allow to make code updates to include these changes. This means that the `event_data` parameter will need to be serialized when storing it and deserialized when fetched.
* Ensures `ACID` compliance, but it's not needed by the application.

### Backend
I decided to develop the backend based on `PyDantic` to handle the object models, `FastAPI` to handle the requests and response of the server, and `Uvicorn` to run the server.


## Further considerations

* <ins>Implement `scoping` to control user permission capabilities</ins>. For instance, we might want to let some users to being capable of reading events but not being able to create/delete them.
* <ins>Implement `smart event filtering`.</ins> For now simple filtering has been implemented and users can filter events by exact matches (*see the ***Testing*** section*). Adding filters like being able to filter by a range of dates or to use partial matches or wildcards would be helpful
* <ins>Configure `mongodb` to use multiple instances</ins>. Add configuration that allow to use multiple instances of mongodb and escalate horizontally if needed.


## Deploying
This microservice uses `docker` in order to be deployed, to deploy just run the command:
```bash
docker-compose up --build
```
For the purposes of testing this technical assesment, I included a `mock` script that allows to create users directly on the `Users` table on `test/mock_script.py`. To create an user just run:

```bash
$ python test/mock_script.py
```
and follow the instructions to register a new user in the database.

## Testing

The instructions to test the code are given on a local setup and assuming the code was deployed according to the instructions given on the ***Deploying*** section
#### Retrieve auth token

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

example reponse:
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
#### Retrieve events that matches some criteria

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
