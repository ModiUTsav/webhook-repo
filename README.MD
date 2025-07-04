## GitHub Webhook Listener
This repository provides a Flask application that acts as a listener for GitHub webhook events. It is designed to receive, process, and store push and pull_request events from a designated GitHub repository into a MongoDB database, and display them via a simple web interface.



## Features
GitHub Webhook Reception: Listens for push and pull_request events from GitHub.

Event Parsing: Extracts key information such as event type, author, branches involved, request ID, and timestamp.

MongoDB Storage: Persists processed events into a MongoDB collection.

Web Interface: Provides a simple frontend to visualize the stored webhook events.

API Endpoint: Offers a /api/events endpoint to fetch events in JSON format.

Robust Timestamp Handling: Converts all incoming timestamps to UTC for consistent storage.

## Technologies Used
Python 3.x

Flask: Web framework for the application.

PyMongo: Python driver for MongoDB.

MongoDB: NoSQL database for storing event data.

python-dotenv: For managing environment variables (e.g., MongoDB URI).

ngrok: To expose the local Flask server to the internet for GitHub webhooks.

## setup Instrction

Prerequisites:

Before you begin, ensure you have the following installed:

Python 3.7+: python.org

Git: git-scm.com

MongoDB Community Server: mongodb.com/try/download/community

ngrok: ngrok.com/download 

## Clone the Repository

First, clone this repository to your local machine:
```
git clone https://github.com/ModiUTsav/webhook_repo.git
cd webhook_repo
```
