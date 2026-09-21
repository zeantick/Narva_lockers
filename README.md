Telegram Locker Registration Bot
A comprehensive Telegram bot designed to automate the registration process for personal storage lockers.

Key Features:

User Data Collection: Gathers user contact information and preferences directly through the Telegram interface.

Automated Document Generation: Automatically generates a personalized rental agreement based on the data provided by the user.

Email Integration: Uses email.message and dotenv to automatically send the generated contract and user details to designated reviewers via email.

Interactive Email Workflow: Includes HTML buttons ("Accept" / "Decline") directly within the email notification, allowing administrators/reviewers to approve or reject requests seamlessly.

Database Management: Utilizes a database to track locker confirmation statuses, manage request lifecycles, and store user language preferences.

Tech Stack:

Python (asyncio, aiogram)

Email handling (emailmessage, dotenv)

Database (SQL/Relational DB for status and language tracking)

Automated document generation and processing