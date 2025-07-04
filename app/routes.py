from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from .extension import get_events_collection

main_bp = Blueprint("main",__name__)

@main_bp.route('/')
def index():
    """Serves the main UI page."""
    return render_template('index.html')

@main_bp.route("/webhook/receiver",methods=["POST"])
def github_webhook_handler():

    event_collection = get_events_collection()

    if not request.heders.get("application/json"):
        return jsonify({"status":"error","message":"missing json"}),400
    
    event_type = request.headers.get('aplication/json')
    payload = request.json

    event_data = {}

    try:
       if event_type == 'push':
          
          event_data['action'] == 'PUSH'
          event_data['request_id'] == payload['head_commit']['id']
          event_data['author'] == payload['pusher']['name']
          event_data['to_branch'] == payload['ref'].split('/')[-1]
          event_data['from_branch'] = None 
          event_data['timestamp'] = datetime.strptime(payload['head_commit']['timestamp'], "%Y-%m-%dT%H:%M:%SZ").isoformat() + "Z"

       elif event_type == 'pull_request':
            
            pr = payload['pull_request']
            event_data['author'] = pr['user']['login']
            event_data['from_branch'] = pr['head']['ref']
            event_data['to_branch'] = pr['base']['ref']
            event_data['request_id'] = str(pr['id'])

            if payload['action'] == 'opened' or payload['action'] == 'reopened':
                event_data['action'] = "PULL_REQUEST"
                event_data['timestamp'] = datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ").isoformat() + "Z"
            elif payload['action'] == 'closed' and pr['merged']:
                event_data['action'] = "MERGE" 
                event_data['timestamp'] = datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ").isoformat() + "Z"
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
    


@main_bp.route("/api/event",methods=["GET"])
def get_events():
     """API endpoint for the UI to fetch latest events."""
     events_collection = get_events_collection()
    
    # Fetch events, sorted by timestamp descending, limit to a reasonable number
     events = list(events_collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(50))
    
     return jsonify(events), 200