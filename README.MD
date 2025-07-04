<img width="1555" height="989" alt="Image" src="https://github.com/user-attachments/assets/ec250f1c-93f7-4785-823e-0c64b6fbe91d" />

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
## Virtual Environment Setup
It's highly recommended to use a virtual environment to manage dependencies:
```
python -m venv venv
```
On Windows (Command Prompt):

```

venv\Scripts\activate.bat
```

## Install Dependencies
Once your virtual environment is active, install the required Python packages:
```
pip install -r requirements.txt
# If requirements.txt is not present, you can manually install:
# pip install Flask pymongo python-dotenv
```

MongoDB Setup
Ensure your MongoDB server is running. By default, the application expects MongoDB to be accessible at mongodb://localhost:27017/.

The application will connect to a database named webhook_repo and store events in a collection named webhook_events. These will be created automatically if they don't exist.

## ngrok Setup
Download and Install: If you haven't already, download ngrok and follow their installation instructions.

Connect your Authtoken: After signing up on ngrok.com, you'll get an authtoken. Connect it to your ngrok client:

```
BASH

```
```
ngrok authtoken YOUR_AUTH_TOKEN
```

## GitHub Webhook Configuration
You need to configure a webhook in your GitHub repository (e.g., your action_repo) to send events to your local Flask application via ngrok.

Go to your GitHub repository (e.g., ModiUTsav/action_repo).

Navigate to Settings > Webhooks.

Click Add webhook.

Configure the webhook with the following details:

Payload URL: This will be your ngrok forwarding URL followed by /webhook/receiver.

Important: You will get this URL after you start ngrok (see Running the Application below). It will look something like https://abcdefg.ngrok-free.app/webhook/receiver.

Content type: Select application/json.

Secret: Leave this blank for now (your current Flask app doesn't validate it, but for production, this is crucial for security).

Which events would you like to trigger this webhook?: Select "Let me select individual events" and then choose:

Pushes

Pull requests

Active: Ensure this checkbox is ticked.

Click "Add webhook".

## Running the Application

You'll need three separate terminal windows: one for MongoDB, one for your Flask app, and one for ngrok.

Start MongoDB:
Ensure your MongoDB server is running. (e.g., mongod command, or via MongoDB Compass/service).

Start Flask Application:
Open a new terminal, activate your virtual environment, and run the Flask app:

```
cd /path/to/your/webhook_repo
# Activate virtual environment (if not already active)
# source venv/bin/activate (Linux/macOS)
# venv\Scripts\activate.bat (Windows)
python run.py
```
Your Flask app will start on http://127.0.0.1:5000. You should see output like:
```
MongoDB connected to DB: webhook_repo, Collection: webhook_events
 * Debugger is active!
 * Debugger PIN: ...
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Start ngrok Tunnel:
Open another new terminal and run ngrok to expose your Flask app:
```
ngrok http 5000
```
Ngrok will provide a public URL (e.g., https://abcdefg.ngrok-free.app). Copy this HTTPS URL. This is what you'll use for the GitHub webhook payload URL.

Remember to update the GitHub webhook Payload URL with the new ngrok URL if it changes (ngrok free tier URLs change every time you restart ngrok).


Usage
Trigger a Push Event: Make a commit and push it to the main branch of your action_repo on GitHub.

Trigger a Pull Request Event: Create a new branch, make changes, push the branch, and then open a pull request on GitHub from that branch to main. To test a MERGE event, merge the pull request on GitHub.

Viewing Events
Web Interface: Open your web browser and go to your ngrok URL (e.g., https://abcdefg.ngrok-free.app/). This will display the latest events.

API Endpoint: Access the raw JSON data by going to your_ngrok_url/api/events.

MongoDB Compass/Shell: Connect to your MongoDB instance and inspect the webhook_repo.webhook_events collection.

Event Data Stored
For push events, the following data is stored:
```
{
    "action": "PUSH",
    "request_id": "commit_sha",
    "author": "pusher_name",
    "to_branch": "branch_name",
    "from_branch": null,
    "timestamp": "ISO_8601_UTC_timestamp"
}
```

For pull_request events (opened/reopened):
        ```
         {
    "action": "PULL_REQUEST",
    "request_id": "pull_request_id",
    "author": "pr_user_login",
    "from_branch": "source_branch_name",
    "to_branch": "target_branch_name",
    "timestamp": "ISO_8601_UTC_timestamp"
}
        ```
For pull_request events (merged):
```
{
    "action": "MERGE",
    "request_id": "pull_request_id",
    "author": "merging_user_login", # or pr_user_login depending on actual payload
    "from_branch": "source_branch_name",
    "to_branch": "target_branch_name",
    "timestamp": "ISO_8601_UTC_timestamp"
}
```


