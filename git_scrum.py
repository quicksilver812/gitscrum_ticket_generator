import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GITSCRUM_API_KEY")
PROJECT_ID = os.getenv("GITSCRUM_PROJECT_ID")
BASE_URL = "https://api.gitscrum.com/tasks/"

def create_task_on_gitscrum(title, description="", value_fixed=None, workflow_id=None, effort_id=None, type_id=None, start_date=None, due_date=None, is_draft=False, is_archived=False):
    """
    Create a task in GitScrum using API query parameters for authentication.
    
    Args:
        title: Task title (required, max 255 chars)
        description: Task description (optional)
        value_fixed: Decimal value (optional, e.g., 10.15)
        workflow_id: Workflow ID (optional)
        effort_id: Effort ID (optional)
        type_id: Type ID (optional)
        start_date: Start date (optional, format: YYYY-MM-DD HH:MM:SS)
        due_date: Due date (optional, format: YYYY-MM-DD HH:MM:SS)
        is_draft: Boolean flag for draft status (optional)
        is_archived: Boolean flag for archived status (optional)
    
    Returns:
        dict: Full response data from GitScrum API or None if error
    """
    if not API_KEY or not PROJECT_ID:
        print("❌ Missing GITSCRUM_API_KEY or GITSCRUM_PROJECT_ID in environment variables")
        return None

    # Construct URL with authentication parameters
    url = f"{BASE_URL}?project_key={PROJECT_ID}&api_id={API_KEY}"

    payload = {
        "title": title,
        "description": description,
        "value_fixed": value_fixed,
        "workflow_id": workflow_id,
        "effort_id": effort_id,
        "type_id": type_id,
        "start_date": start_date,
        "due_date": due_date,
        "is_draft": is_draft,
        "is_archived": is_archived,
    }

    # Remove None values from payload to avoid sending unnecessary fields
    payload = {k: v for k, v in payload.items() if v is not None}

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 201:
            response_data = response.json()
            # The API likely returns the full task object, not just task_id
            # Access it based on actual API response structure
            task_id = response_data.get("id") or response_data.get("task_id") or response_data.get("data", {}).get("id")
            print(f"✅ Task created successfully! Task ID: {task_id}")
            return response_data
        else:
            print(f"❌ Error creating task: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None
    
def get_task_status(task_id):
    """Fetch a task from GitScrum and extract the workflow title."""
    url = f"https://api.gitscrum.com/tasks/{task_id}?project_key={PROJECT_ID}&api_id={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # raise error if HTTP error occurs
        data = response.json()

        # Navigate to workflow.title
        workflow_title = data["data"]["workflow"]["title"]
        return workflow_title

    except requests.exceptions.RequestException as e:
        print("❌ Request error:", e)
    except KeyError:
        print("⚠️ Could not find 'workflow.title' in the response.")
    except Exception as e:
        print("⚠️ Unexpected error:", e)



