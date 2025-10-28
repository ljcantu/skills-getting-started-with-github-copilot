from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

def test_signup_for_activity():
    email = "test@mergington.edu"
    activity_name = "Chess Club"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Verify user is in the activity's participants
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity_name = "Chess Club"
    
    # First signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    # Try to signup again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_from_activity():
    email = "unregister@mergington.edu"
    activity_name = "Chess Club"
    
    # First signup the user
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Then unregister
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    # Verify user is removed from participants
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_signed_up():
    email = "notsignedup@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_nonexistent_activity():
    response = client.post("/activities/NonexistentClub/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]