<img width="1555" height="989" alt="Image" src="https://github.com/user-attachments/assets/ec250f1c-93f7-4785-823e-0c64b6fbe91d" />

# GitHub Webhook Listener

This repository provides a Flask application that acts as a listener for GitHub webhook events. It's designed to receive, process, and store push and pull request events from a designated GitHub repository into a MongoDB database, and display them via a simple web interface. The application is containerized using Docker and Docker Compose for easy setup and deployment.

## Features ✨

* **GitHub Webhook Reception**: Listens for `push` and `pull_request` events from GitHub.
* **Event Parsing**: Extracts key information such as event type, author, branches involved, request ID, and timestamp.
* **MongoDB Storage**: Persists processed events into a MongoDB collection.
* **Web Interface (UI)**: Provides a simple frontend to visualize the stored webhook events.
* **Real-time Display**: The UI's API endpoint (`/api/events`) now fetches and displays only the **latest 15 seconds** of GitHub event data, providing a near real-time view.
* **API Endpoint**: Offers a `/api/events` endpoint for the UI to fetch latest events in JSON format.
* **Dockerized**: The entire application (Flask app + MongoDB) is containerized using Docker and Docker Compose for easy setup and consistent environments.

## Technologies Used 🛠️

* **Python 3.9+**
* **Flask**: Web framework
* **PyMongo**: MongoDB driver for Python
* **MongoDB**: Database for storing events
* **Docker & Docker Compose**: For containerization and orchestration
* **Ngrok**: (Optional, for local development) To expose your local server to the internet for GitHub webhooks.

## Setup and Running the Application 🚀

### Prerequisites

* **Docker Desktop**: Make sure Docker Desktop is installed and running on your system.
* **Git**: For cloning the repository.
* **Ngrok (Optional for local testing)**: Download from [ngrok.com](https://ngrok.com/).

### 1. Clone the Repository

```bash
git clone https://github.com/ModiUTsav/webhook-repo.git
cd webhook_repo
```
2. Configure Environment Variables
Create a file named .env in the root of your project directory (where docker-compose.yml is located).

# .env
```
MONGO_URI=mongodb://mongodb:27017/
MONGO_DB_NAME=webhook_repo
MONGO_COLLECTION_NAME=webhook_events

# GITHUB_WEBHOOK_SECRET=your_strong_random_secret_here # Uncomment and set this if you implement signature verification
```
Note: The GITHUB_WEBHOOK_SECRET is commented out as the signature verification decorator was removed for this iteration. If you decide to add it back for security, remember to uncomment and set this.

3. Build and Run with Docker Compose
This command will build your Flask application image, pull the MongoDB image, and start both services.

Bash
```
docker-compose up --build -d
--build: Ensures your Flask app's Docker image is rebuilt (important if you change code or requirements.txt).

-d: Runs the containers in detached mode (in the background).
```

4. Verify Containers Are Running
Bash
```
docker-compose ps
You should see both webhook_listener and mongodb containers in a running state.
```

5. Expose Your Local Server to GitHub (for Webhooks)
GitHub needs a publicly accessible URL to send webhooks.

Start Ngrok (in a new terminal window):

Bash

ngrok http 5000
This will give you a public https URL (e.g., https://xxxxxx.ngrok-free.app).

Configure GitHub Webhook:

Go to your GitHub repository's Settings > Webhooks.

Click "Add webhook" or edit your existing one.

Set "Payload URL" to the Ngrok https URL followed by /webhook/receiver (e.g., https://xxxxxx.ngrok-free.app/webhook/receiver).

Set "Content type" to application/json.

Leave the "Secret" field empty (since webhook signature verification is not implemented in this version).

Choose "Just the push event." and "Pull requests" or "Send me everything." as needed.

Click "Add webhook" or "Update webhook".

6. Access the Web UI
Open your web browser and go to:
```
http://localhost:5000/
```
You should see your Flask application's UI, which will display the latest 15 seconds of GitHub events as they are received.

Usage 💡
Once the application is running and the GitHub webhook is configured:

Perform actions in your GitHub repository (e.g., push new commits, open/close pull requests).

Observe the events appearing dynamically on your http://localhost:5000/ web UI. Events will automatically disappear after 15 seconds.

You can also manually check the API endpoint at ```http://localhost:5000/api/events``` to see the raw JSON data.

Stopping the Application
To stop and remove the running Docker containers:

Bash
```
docker-compose down
This will stop and remove the webhook_listener and mongodb containers, but it will preserve the mongo_data volume by default, so your MongoDB data persists.
```

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


