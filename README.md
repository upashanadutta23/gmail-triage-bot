# gmail-triage-bot
# Gmail Cognitive Triage Agent 🤖

This project is an intelligent Python script that automatically processes unread emails from a Gmail account. It uses the Google Gemini API to understand the content and intent of each email and then takes action by integrating with other Google Workspace services like Calendar, Tasks, and Sheets.

This agent is designed to be run both locally on a personal machine or deployed in a cloud environment like Google Colab.

## Features

* **Fetches Unread Emails**: Securely connects to the Gmail API to retrieve the latest unread emails.
* **AI-Powered Intent Classification**: Uses the Gemini AI to classify each email's intent (e.g., `receipt_invoice`, `task_delegation`, `scheduling_request`).
* **Automated Data Extraction**: Extracts key information from actionable emails, such as vendor names, purchase amounts, task descriptions, and due dates.
* **Google Workspace Integration**:
    * Logs expenses from receipts directly into a specified Google Sheet.
    * Creates new tasks in Google Tasks from emails that delegate work.
    * Creates draft events in Google Calendar from scheduling requests.
* **Automatic Cleanup**: Marks emails as read after they have been processed.

---

## Setup and Installation

Follow these steps to get the agent running on your local machine.

### 1. Prerequisites

* Python 3.10+
* A Google Cloud project with the following APIs enabled:
    * Gmail API
    * Google Calendar API
    * Google Tasks API
    * Google Sheets API
    * Generative Language API (for Gemini)
* A Google Sheet for logging expenses.
* A Gemini API Key from Google AI Studio.

### 2. Clone the Repository

Clone this project to your local machine:

```sh
git clone [https://github.com/upashnadutta23/gmail-triage-bot.git](https://github.com/upashnadutta23/gmail-triage-bot.git)
cd gmail-triage-bot


3. Set Up the Python Environment
Create and activate a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
4. Install Dependencies
Install all the required Python libraries:
pip install -r requirements.txt

Of course. Here is the complete README.md file for your project.

📄 Copy the entire text from the code block below and paste it into your README.md file using the nano README.md command.

Markdown

# Gmail Cognitive Triage Agent 🤖

This project is an intelligent Python script that automatically processes unread emails from a Gmail account. It uses the Google Gemini API to understand the content and intent of each email and then takes action by integrating with other Google Workspace services like Calendar, Tasks, and Sheets.

This agent is designed to be run both locally on a personal machine or deployed in a cloud environment like Google Colab.

## Features

* **Fetches Unread Emails**: Securely connects to the Gmail API to retrieve the latest unread emails.
* **AI-Powered Intent Classification**: Uses the Gemini AI to classify each email's intent (e.g., `receipt_invoice`, `task_delegation`, `scheduling_request`).
* **Automated Data Extraction**: Extracts key information from actionable emails, such as vendor names, purchase amounts, task descriptions, and due dates.
* **Google Workspace Integration**:
    * Logs expenses from receipts directly into a specified Google Sheet.
    * Creates new tasks in Google Tasks from emails that delegate work.
    * Creates draft events in Google Calendar from scheduling requests.
* **Automatic Cleanup**: Marks emails as read after they have been processed.

---

## Setup and Installation

Follow these steps to get the agent running on your local machine.

### 1. Prerequisites

* Python 3.10+
* A Google Cloud project with the following APIs enabled:
    * Gmail API
    * Google Calendar API
    * Google Tasks API
    * Google Sheets API
    * Generative Language API (for Gemini)
* A Google Sheet for logging expenses.
* A Gemini API Key from Google AI Studio.

### 2. Clone the Repository

Clone this project to your local machine:

```sh
git clone [https://github.com/upashnadutta23/gmail-triage-bot.git](https://github.com/upashnadutta23/gmail-triage-bot.git)
cd gmail-triage-bot
3. Set Up the Python Environment
Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

4. Install Dependencies:
Install all the required Python libraries:
pip install -r requirements.txt

5. Configure Credentials
credentials.json: Download your OAuth 2.0 Client ID credentials file from the Google Cloud Console and place it in the root of the project directory.
.env file: Create a file named .env in the root of the project and add your secret keys.

python3 main.py

