# Receipt Processor Challenge

This repository contains the source code for a take-home assignment for Fetch Rewards, implemented in Python using FastAPI. The server manages two main functions:

## Features

1. **POST `/receipts/process`**:
   - **Functionality**: Receives a JSON object representing a receipt, calculates points based on specified rules, and returns a JSON response containing a unique ID for the processed receipt. This ID is subsequently used to retrieve the points via a GET request.
   - **Error Handling**: Includes validations for missing attributes in the JSON body, incorrect date and time formats, and other internal server errors.

2. **GET `/receipts/{id}/points`**:
   - **Functionality**: Retrieves the points associated with a previously submitted receipt using the ID from the POST response.
   - **Error Handling**: Ensures the provided ID matches an existing entry in the in-memory store, returning errors if not found.

## Directory Structure

```plaintext
receipt_processor/
│
├── Dockerfile             # Docker configuration for containerization
├── main.py                # Main application file with FastAPI setup
├── models.py              # Data models for the application
├── utils.py               # Utility functions including point calculation
├── requirements.txt       # List of dependencies
```

**Note:**

- The code that's directly related to this assignment can be found in: main.py, models.py, utils.py
- Instructions below go into detail on how to test the Python FastAPI server endpoints using using curl

## How to run the Receipt API server using Docker

1. Within the `receipt_processor` directory build the Docker image by running `docker build -t receipt-processor-api .`

2. Confirm that a Docker image was created by running this command from the same directory `docker image ls`

3. If you see a new entry in the table printed with the name fetch-receipt-api and the tag latest then the docker build should have worked, you should see something like this printed in your console:
```
REPOSITORY               TAG     IMAGE ID      CREATED         SIZE
receipt-processor-api   latest  27a893d09711  6 seconds ago   851MB
```

4. Run the docker image using this command from the same directory `docker run -d -p 8000:8000 receipt-processor-api`
This will start the Docker image connecting the Docker container's port 8000 to your machine's 8000 port, this also allows the image to run in the background freeing up your console instead of forcing you to open a new one.
You do not need to specify the host here, although if you prefer to specify localhost or 127.0.0.1 that will still work.

5. Verify that you see the Docker container running in the Docker Desktop app

Docker Notes:

    This assumes you already have docker installed and know how to use it/know the basics around Docker

## How to run the Receipt API server without Docker

Within the `receipt-processor` directory simply run this following commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

     

# How to test the Receipt API
## Using curl

From your console run following curl command to hit the /receipts/process POST endpoint:
This command specifically holds the same Receipt data used in example one of the assignment

```
curl -X POST http://127.0.0.1:8000/receipts/process \
-H "Content-Type: application/json" \
-d '{
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        },
        {
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
        },
        {
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
        },
        {
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
        },
        {
            "shortDescription": "Klarbrunn 12-PK 12 FL OZ",
            "price": "12.00"
        }
    ],
    "total": "35.35"
}'

```

Verify you are sent back a JSON object that follows this format (id can be different) below:

`{ "id" : "1c23395b-7b6e-47bf-887c-f8e7608c809c" }`

Copy the uuid, this will be used to hit the `/receipts/{id}/points` GET endpoint

From the console run following curl command to hit the `/receipts/{id}/points` endpoint using the id received from the previous POST request:
Note: The uuid between receipts and points in this path must be the id from earlier

`curl -X GET http://127.0.0.1:8000/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points`

Verify you are sent back a JSON object that follows this format below:

`{ "points" : "28" }`

In this case 28 should be the correct amount of points that the receipt sent earlier has

## Further testing

Including another POST curl command that represents example two from the assignment, this receipt should return 109 points -- so verify this is what you see after sending your GET request.

```
curl -X POST http://127.0.0.1:8000/receipts/process \
-H "Content-Type: application/json" \
-d '{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}'

```

Use the same GET curl command from the above section using the new id -- verify that 109 points are returned.
