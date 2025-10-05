# src/triage/runner.py
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import datetime

# --- Cognitive Engine Functions ---
def configure_gemini(api_key):
    """Configures the Gemini API and returns the model."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-pro-latest')
        print("Gemini API configured successfully.")
        return model
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return None

def get_email_intent(model, email_body):
    """Uses Gemini to classify the intent of an email."""
    prompt = f"""
    Analyze the following email content and classify its primary intent.
    Choose from one of these categories:
    - task_delegation
    - scheduling_request
    - receipt_invoice
    - information_query
    - no_action_needed

    Email Content:
    ---
    {email_body}
    ---
    Return only the single intent category name.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"  -> Error classifying intent: {e}")
        return "error"


def extract_information(model, email_body, intent):
    """Uses Gemini to extract structured information based on the email's intent."""
    if intent == "task_delegation":
        prompt = f"""
        From the email below, extract the task details.
        Return a JSON object with keys: "task_description", "due_date" (YYYY-MM-DD or null), "priority" ("High", "Medium", "Low").
        Email Content: --- {email_body} ---
        """
    elif intent == "scheduling_request":
        prompt = f"""
        From the email below, extract event details.
        Return a JSON object with keys: "event_title", "attendees" (list of emails), "proposed_time" (YYYY-MM-DDTHH:MM:SS or null).
        Email Content: --- {email_body} ---
        """
    elif intent == "receipt_invoice":
        prompt = f"""
        From the email below, extract expense details.
        Return a JSON object with keys: "vendor_name", "total_amount" (float), "purchase_date" (YYYY-MM-DD).
        Email Content: --- {email_body} ---
        """
    else:
        return None

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"  -> Error extracting information: {e}")
        return None

# --- Workspace Action Functions ---
def create_google_task(creds, task_details):
    """Creates a new task in Google Tasks."""
    service = build("tasks", "v1", credentials=creds)
    if not task_details.get("task_description"):
        print("  -> Skipping task creation: No description found.")
        return
    task = {'title': task_details["task_description"]}
    if task_details.get("due_date"):
        task['due'] = f'{task_details["due_date"]}T00:00:00.000Z'
    try:
        result = service.tasks().insert(tasklist='@default', body=task).execute()
        print(f"  -> Successfully created task: '{result['title']}'")
    except HttpError as e:
        print(f"  -> Error creating Google Task: {e}")


def create_calendar_event(creds, event_details):
    """Creates a new event in Google Calendar."""
    service = build("calendar", "v3", credentials=creds)
    if not all(k in event_details for k in ["event_title", "proposed_time"]):
        print("  -> Skipping event creation: Missing title or time.")
        return
    start_time_str = event_details["proposed_time"]
    start_time = datetime.datetime.fromisoformat(start_time_str)
    end_time = start_time + datetime.timedelta(hours=1)
    event = {
        'summary': event_details["event_title"],
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'America/Chicago'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'America/Chicago'},
        'attendees': [{'email': email} for email in event_details.get("attendees", [])],
    }
    try:
        result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"  -> Successfully created event: '{result['summary']}'")
    except HttpError as e:
        print(f"  -> Error creating Google Calendar event: {e}")


def log_expense_to_sheet(creds, sheet_id, expense_details):
    """Appends a new row with expense data to a Google Sheet."""
    service = build("sheets", "v4", credentials=creds)
    if not all(k in expense_details for k in ["purchase_date", "vendor_name", "total_amount"]):
        print("  -> Skipping expense logging: Missing details.")
        return
    values = [[
        expense_details["purchase_date"],
        expense_details["vendor_name"],
        expense_details["total_amount"]
    ]]
    body = {'values': values}
    try:
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="Sheet1!A1",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print(f"  -> Successfully logged expense for '{expense_details['vendor_name']}'")
    except HttpError as e:
        print(f"  -> Error logging expense: {e}")
