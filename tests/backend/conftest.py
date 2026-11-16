"""
Pytest configuration and fixtures for FastAPI backend tests.

Provides fixtures for:
- Fresh app instance with TestClient
- Clean in-memory activities state
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient instance for making HTTP requests to the app."""
    return TestClient(app)


@pytest.fixture
def clean_activities(client):
    """
    Fixture that returns a snapshot of clean activities state.
    
    This fixture modifies the app's activities dict to clear all participants
    before each test, ensuring test isolation.
    """
    # Import here to access the module's activities dict
    from src.app import activities
    
    # Clear participants from all activities for clean state
    for activity_name in activities:
        activities[activity_name]["participants"] = []
    
    yield activities
    
    # Cleanup after test - reset to clean state
    for activity_name in activities:
        activities[activity_name]["participants"] = []
