"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    # ...existing code...
}

# --- User Profiles (students) ---
students = {
    "michael@mergington.edu": {
        "name": "Michael Smith",
        "grade": 11,
        "interests": ["Chess", "Math", "Programming"]
    },
    "emma@mergington.edu": {
        "name": "Emma Johnson",
        "grade": 10,
        "interests": ["Programming", "Art"]
    }
    # ...ajoutez d'autres élèves ici...
}

# --- Organization Profiles ---
organizations = {
    "Chess Club": {
        "description": "Chess enthusiasts club.",
        "members": ["michael@mergington.edu"],
        "contact": "chess@mergington.edu"
    },
    "Art Club": {
        "description": "Art and creativity club.",
        "members": ["emma@mergington.edu"],
        "contact": "art@mergington.edu"
    }
    # ...ajoutez d'autres organisations ici...
}

# --- Event Profiles ---
events = {
    1: {
        "title": "Chess Tournament",
        "date": "2025-10-10",
        "organization": "Chess Club",
        "participants": ["michael@mergington.edu"]
    },
    2: {
        "title": "Art Expo",
        "date": "2025-11-05",
        "organization": "Art Club",
        "participants": ["emma@mergington.edu"]
    }
    # ...ajoutez d'autres événements ici...
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


# --- Endpoints pour les profils ---

@app.get("/activities")
def get_activities():
    return activities

@app.get("/students")
def get_students():
    """Retourne la liste des profils élèves"""
    return students

@app.get("/students/{email}")
def get_student_profile(email: str):
    if email not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[email]

@app.get("/organizations")
def get_organizations():
    """Retourne la liste des organisations"""
    return organizations

@app.get("/organizations/{name}")
def get_organization_profile(name: str):
    if name not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organizations[name]

@app.get("/events")
def get_events():
    """Retourne la liste des événements"""
    return events

@app.get("/events/{event_id}")
def get_event_profile(event_id: int):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return events[event_id]


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
