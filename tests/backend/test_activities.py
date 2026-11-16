"""
Integration tests for FastAPI Mergington High School activities API.

Tests use the AAA (Arrange-Act-Assert) pattern for clarity:
- Arrange: Set up test data and initial state
- Act: Execute the API endpoint being tested
- Assert: Verify the response and side effects
"""

import pytest


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid(self, client, clean_activities):
        """
        Test successful signup for an activity.
        
        Arrange: Choose an activity and email
        Act: POST to signup endpoint
        Assert: Verify email added to participants and 200 response
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert email in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_duplicate(self, client, clean_activities):
        """
        Test signup fails when student already registered.
        
        Arrange: Manually add email to activity participants
        Act: POST to signup endpoint with same email
        Assert: Verify 400 error and participants unchanged
        """
        # Arrange
        activity_name = "Programming Class"
        email = "bob@mergington.edu"
        clean_activities[activity_name]["participants"].append(email)
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count

    def test_signup_activity_not_found(self, client):
        """
        Test signup fails for non-existent activity.
        
        Arrange: Prepare invalid activity name
        Act: POST to signup with non-existent activity
        Assert: Verify 404 error
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "charlie@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_valid(self, client, clean_activities):
        """
        Test successful unregister from an activity.
        
        Arrange: Manually add email to activity participants
        Act: DELETE unregister endpoint
        Assert: Verify email removed from participants and 200 response
        """
        # Arrange
        activity_name = "Gym Class"
        email = "diana@mergington.edu"
        clean_activities[activity_name]["participants"].append(email)
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_not_registered(self, client, clean_activities):
        """
        Test unregister fails when student not registered.
        
        Arrange: Ensure email not in activity participants
        Act: DELETE unregister endpoint
        Assert: Verify 400 error and participants unchanged
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "evan@mergington.edu"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count

    def test_unregister_activity_not_found(self, client):
        """
        Test unregister fails for non-existent activity.
        
        Arrange: Prepare invalid activity name
        Act: DELETE unregister with non-existent activity
        Assert: Verify 404 error
        """
        # Arrange
        activity_name = "Missing Activity"
        email = "fiona@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestSanityChecks:
    """Basic sanity checks for other endpoints."""

    def test_get_activities_returns_dict(self, client):
        """
        Test that GET /activities returns activity data.
        
        Arrange: Prepare client
        Act: GET /activities
        Assert: Verify response is dict with expected activity names
        """
        # Arrange (implicit via fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_root_redirects(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        Arrange: Prepare client
        Act: GET / with follow_redirects=False
        Assert: Verify redirect response
        """
        # Arrange (implicit via fixture)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
