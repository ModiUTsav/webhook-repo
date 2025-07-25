from flask import Blueprint, request, jsonify, render_template
from datetime import timezone, datetime,timedelta
from .extension import get_events_collection
from pymongo import DESCENDING

main_bp = Blueprint("main",__name__)

@main_bp.route('/')
def index():
    """Serves the main UI page."""
    return render_template('index.html')

@main_bp.route("/webhook/receiver",methods=["POST"])
def github_webhook_handler():
    
    event_collection = get_events_collection()

    if not request.headers.get("X-GitHub-Event"):
        return jsonify({"status":"error","message":"missing X-GitHub-Event"}),400
    
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    print(payload)

    event_data = {}

    try:
       if event_type == 'push':
          
          dt_object_with_tz = datetime.strptime(payload['head_commit']['timestamp'], "%Y-%m-%dT%H:%M:%S%z")
          
          event_data['action'] = 'PUSH'
          event_data['request_id'] = payload['head_commit']['id']
          event_data['author'] = payload['pusher']['name']
          event_data['to_branch'] = payload['ref'].split('/')[-1]
          event_data['from_branch'] = None 
          
          event_data['timestamp'] = dt_object_with_tz.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

       elif event_type == 'pull_request':
            
            pr = payload['pull_request']
            event_data['author'] = pr['user']['login']
            event_data['from_branch'] = pr['head']['ref']
            event_data['to_branch'] = pr['base']['ref']
            event_data['request_id'] = str(pr['id'])

            if payload['action'] == 'opened' or payload['action'] == 'reopened':
                event_data['action'] = "PULL_REQUEST"
                timestamp_str = pr['created_at']

                if timestamp_str.endswith('Z'):
                    dt_object = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                else:
                    dt_object = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S%z")

                event_data['timestamp'] = dt_object.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

                

            elif payload['action'] == 'closed' and pr['merged']:
                event_data['action'] = "MERGE" 
                if pr['merged_at']:
                    timestamp_str = pr['merged_at'] # Get the timestamp string for PR merge
                    
                    # Parse timestamp specifically for pull_request 'merged_at'
                    if timestamp_str.endswith('Z'):
                        dt_object = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    else:
                        dt_object = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S%z")

                    event_data['timestamp'] = dt_object.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

            else:
                
                return jsonify({"status": "ignored", "message": f"Unhandled pull_request action: {payload['action']}"}), 200

       else:
           return jsonify({"status": "ignored", "message": f"Unhandled GitHub event type: {event_type}"}), 200
        
       event_collection.insert_one(event_data)
       return jsonify({"status":"sucess","message":"event stored sucessfully"}),200 
    
    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing key in payload: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500
    


@main_bp.route("/api/events",methods=["GET"])
def get_events():
    """API endpoint for the UI to fetch latest events (last 15 seconds)."""
    events_collection = get_events_collection()
    
    # 1. Calculate the time threshold (15 seconds ago) in UTC
    now_utc = datetime.now(timezone.utc)
    time_15_seconds_ago = now_utc - timedelta(seconds=15)
    
    # 2. Convert to ISO 8601 string with 'Z' suffix for MongoDB query
    time_threshold_iso = time_15_seconds_ago.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    
    # 3. Query MongoDB for events within the last 15 seconds
    events_cursor = events_collection.find(
        {"timestamp": {"$gte": time_threshold_iso}}
    ).sort("timestamp", DESCENDING).limit(50) 
    
    # NEW: Convert ObjectId to string for JSON serialization
    events_list = []
    for event in events_cursor:
        if '_id' in event:
            event['_id'] = str(event['_id']) # Convert ObjectId to string
        events_list.append(event)
    
    return jsonify(events_list), 200