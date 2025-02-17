import pytest
from fastapi.testclient import TestClient
from main import create_app


class TestUpdateTask:
    """Tests for PUT /tasks/{task_id}/"""
    client = TestClient(create_app())

    def test_invalid_input_type(self):
        """Test that a non-integer task_id results in a 422 error."""
        response = self.client.put("/tasks/not-an-int/", json={"title": "Updated Title"})
        assert response.status_code == 422  # Unprocessable Entity

    def test_invalid_task_id(self):
        """Test that updating a non-existent task results in a 404 error."""
        response = self.client.put("/tasks/99999/", json={"title": "Updated Title"})
        assert response.status_code == 404  # Task not found

    def test_update_single_value(self):
        """Test updating only one field and ensure only that value is changed."""
        # Step 1: Create a test task
        create_response = self.client.post("/tasks/", json={
            "title": "Original Title",
            "description": "Original Description",
            "priority": 2,
            "due_date": "2025-01-01T12:00:00",
            "completed": False
        })
        assert create_response.status_code == 200  # Created
        created_task = create_response.json()
        task_id = created_task["id"]

        # Step 2: Get the original task
        get_response = self.client.get(f"/tasks/{task_id}/")
        assert get_response.status_code == 200
        original_task = get_response.json()

        # Step 3: Update only the "title"
        update_response = self.client.put(f"/tasks/{task_id}/", json={"title": "Updated Title"})
        assert update_response.status_code == 200  # Successfully updated
        updated_task = update_response.json()

        # Step 4: Verify only "title" has changed
        assert updated_task["title"] == "Updated Title"
        assert updated_task["description"] == original_task["description"]
        assert updated_task["priority"] == original_task["priority"]
        assert updated_task["due_date"] == original_task["due_date"]
        assert updated_task["completed"] == original_task["completed"]

    def test_invalid_extra_key(self):
        """Test sending an extra unexpected key results in 422 error."""
        # Step 1: Get all tasks to find the first available task ID
        get_response = self.client.get("/tasks/")
        assert get_response.status_code == 200
        tasks = get_response.json()
        
        assert len(tasks) > 0, "No tasks available to test"  # Ensure at least one task exists
        task_id = tasks[0]["id"]  # Get the first task's ID

        # Step 2: Try updating the task with an extra unexpected key
        response = self.client.put(f"/tasks/{task_id}", json={"title": "Valid Title", "invalid_key": "Some Value"})
        
        # Step 3: Ensure the response is 422 Unprocessable Entity
        assert response.status_code == 422
