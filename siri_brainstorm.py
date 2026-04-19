from flask import Flask, request
from database import SessionLocal
from models import Task
from datetime import datetime

app = Flask(__name__)

@app.route('/brainstorm', methods=['GET'])
def add_brainstorm():
    # Siri will send the dictated text as a 'thought' parameter
    idea_text = request.args.get('thought')
    
    if not idea_text:
        return "No thought received", 400

    db = SessionLocal()
    try:
        new_idea = Task(
            name=f"Siri Thought: {idea_text}",
            task_type="Brainstorm",
            priority=3,
            is_completed=False
        )
        db.add(new_idea)
        db.commit()
        print(f"--- Voice Idea Saved: {idea_text} ---")
        return f"Idea '{idea_text}' saved to Point Street Nexus!", 200
    except Exception as e:
        return str(e), 500
    finally:
        db.close()

if __name__ == "__main__":
    # Runs on port 5000
    print("Siri Brainstorm Listener is ACTIVE...")
    app.run(host='0.0.0.0', port=5000)
