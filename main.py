# main.py
import os
import sys
import json
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from src.triage import auth, gmail_client, runner

def main():
    """Main function to run the email triage agent."""
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    google_sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not all([gemini_api_key, google_sheet_id]):
        print("FATAL: GEMINI_API_KEY or GOOGLE_SHEET_ID not found in .env file.")
        sys.exit(1)

    # 1. Authenticate with all required services
    creds = auth.authenticate()
    if not creds:
        print("Could not authenticate. Exiting.")
        sys.exit(1)

    # 2. Configure the Gemini Model
    gemini_model = runner.configure_gemini(gemini_api_key)
    if not gemini_model:
        print("Could not configure Gemini. Exiting.")
        sys.exit(1)

    # 3. Fetch unread emails
    emails = gmail_client.get_unread_emails(creds, max_results=500) # Process 10 emails at a time
    if not emails:
        return

    # 4. Process each email through the cognitive pipeline
    results = []
    print("\n--- Starting Email Processing Pipeline ---")
    for email in emails:
        print(f"\nProcessing Email ID: {email['id'][:10]}... | From: {email['sender']}")
        print(f"Subject: {email['subject']}")

        if not email["body"]:
            print("  -> Skipping: Email body is empty.")
            continue
        
        # Get intent and extract data
        intent = runner.get_email_intent(gemini_model, email["body"])
        print(f"  - Identified Intent: {intent}")

        action_taken = "None"
        details = {}

        if intent and intent not in ["no_action_needed", "information_query", "error"]:
            extracted_data = runner.extract_information(gemini_model, email["body"], intent)
            print(f"  - Extracted Data: {extracted_data}")

            if extracted_data:
                details = extracted_data
                # Perform action based on intent
                if intent == "task_delegation":
                    runner.create_google_task(creds, extracted_data)
                    action_taken = "Created Google Task"
                elif intent == "scheduling_request":
                    runner.create_calendar_event(creds, extracted_data)
                    action_taken = "Created Calendar Event"
                elif intent == "receipt_invoice":
                    runner.log_expense_to_sheet(creds, google_sheet_id, extracted_data)
                    action_taken = "Logged Expense to Sheet"
        
        # Mark email as read after processing
        gmail_client.mark_email_as_read(creds, email["id"])

        results.append({
            'subject': email['subject'],
            'intent': intent,
            'action': action_taken,
            'details': json.dumps(details, indent=4)
        })

    # 5. Display a summary of actions
    print("\n--- Pipeline Summary ---")
    if results:
        df = pd.DataFrame(results)
        print(df)
    else:
        print("No emails were processed.")

if __name__ == "__main__":
    main()
