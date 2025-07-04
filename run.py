# run.py
from app import create_app # Import the create_app function from your app package

app = create_app() # Call create_app to get the configured Flask app

if __name__ == "__main__":
    app.run(debug=True)