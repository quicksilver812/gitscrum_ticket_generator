# Email Issue Tracker (Gitscrum Logger)

An automated customer support system that monitors email inboxes for bug reports, creates tickets in a database, generates tasks in GitScrum, and sends notifications to both customers and employees.

## Features

- **Automated Email Processing**: Monitors IMAP inbox for unread emails
- **AI-Powered Classification**: Uses Google Gemini AI to identify and extract bug information from emails
- **Ticket Management**: Stores tickets in a database with SQLAlchemy
- **GitScrum Integration**: Automatically creates tasks in GitScrum for each bug
- **Email Notifications**: Sends confirmation emails to customers and assignment emails to employees
- **Follow-up System**: Tracks task duration and sends reminder emails for pending issues
- **Status Monitoring**: Periodically checks GitScrum for task completion status

## Architecture

The system runs as a FastAPI application with scheduled background jobs:

1. **Email Checking Job** (runs every 1 minute):
   - Fetches unread emails from inbox
   - Classifies emails using AI to detect bug reports
   - Creates tickets in database
   - Creates tasks in GitScrum
   - Sends confirmation emails

2. **Completion Checking Job** (runs at configured intervals):
   - Checks GitScrum for task completion status
   - Updates ticket status in database
   - Sends follow-up reminder emails for pending tasks

## Project Structure
```
.
├── main.py                      # FastAPI application and scheduler setup
├── models.py                    # SQLAlchemy and Pydantic models
├── requirements.txt             # Python dependencies
├── database/
│   └── database.py             # Database configuration
├── email_files/
│   ├── pull_mails.py           # IMAP email fetching
│   ├── process_mails.py        # AI email classification
│   └── send_mails.py           # SMTP email sending
├── gitscrum_files/
│   └── git_scrum.py            # GitScrum API integration
└── crud/
    └── ticket_crud.py          # Database CRUD operations
```

## Prerequisites

- Python 3.8+
- PostgreSQL or SQLite database
- IMAP-enabled email account
- SMTP email server access
- GitScrum account with API access
- Google AI API key (for Gemini)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd email-issue-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```env
# Email Configuration (IMAP)
EMAIL_HOST=imap.gmail.com
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-app-password

# Email Configuration (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASS=your-app-password

# GitScrum Configuration
GITSCRUM_API_KEY=your-api-key
GITSCRUM_PROJECT_ID=your-project-id

# Employee Configuration
EMPLOYEE_EMAIL=employee@example.com
CHECK_DURATION=4

# Google AI Configuration
GOOGLE_API_KEY=your-google-ai-key

# Database Configuration
DATABASE_URL=sqlite:///./tickets.db
```

## Configuration

### Email Setup

For Gmail:
1. Enable IMAP in Gmail settings
2. Generate an App Password (if using 2FA)
3. Use `imap.gmail.com` and `smtp.gmail.com` as hosts

### GitScrum Setup

1. Log in to your GitScrum account
2. Navigate to API settings
3. Generate an API key
4. Find your project ID from the project URL

### Check Duration

The `CHECK_DURATION` variable sets:
- How often (in hours) the system checks for completed tasks
- The interval added to pending tasks' duration counter

## Usage

### Starting the Application
```bash
uvicorn main:app --reload
```

The application will:
- Start the FastAPI server on `http://localhost:8000`
- Begin monitoring emails every minute
- Check task completion status at configured intervals

### API Endpoints

- `GET /` - Health check endpoint

### Email Format

The AI will extract bug information from emails with the following structure:
```
Subject: [Bug Report] Login button not working

Body:
I'm experiencing an issue where the login button 
doesn't respond when clicked on the homepage.

Priority: High
```

The system extracts:
- **Title**: From subject or body
- **User Email**: From sender
- **Summary**: Description of the issue
- **Priority**: Low, Medium, or High

## Database Schema

### Tickets Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| ticket_id | String | Unique GitScrum task UUID |
| user_email | String | Reporter's email |
| bug_title | String | Bug title |
| bug_summary | String | Bug description |
| bug_priority | String | Low/Medium/High |
| created_at | DateTime | Timestamp |
| status | Boolean | Completion status |
| duration | Integer | Time spent pending (hours) |

## AI Classification

The system uses Google Gemini to classify emails and extract bug information. Emails are classified as bugs if they:
- Describe a software issue or malfunction
- Contain error descriptions or unexpected behavior
- Request technical support

Non-bug emails (greetings, follow-ups, general inquiries) are ignored.

## Email Notifications

### Customer Confirmation Email
Sent immediately after ticket creation with:
- Ticket ID for reference
- Acknowledgment of issue receipt

### Employee Assignment Email
Sent to the configured employee with:
- Task ID
- Task title
- Request to start working on the issue

### Follow-up Reminder Email
Sent for pending tasks with:
- Task ID and title
- Time elapsed since creation
- Reminder to resolve the issue

## Error Handling

The system includes error handling for:
- Email connection failures
- AI API unavailability (503 errors)
- GitScrum API errors
- Database operations
- SMTP sending failures

Errors are logged to console with descriptive messages.

## Development

### Adding New Features

1. **Custom Ticket Fields**: Modify `models.py` and create database migrations
2. **Additional Email Templates**: Add functions to `send_mails.py`
3. **New Scheduling Jobs**: Add jobs to the scheduler in `main.py`

### Testing

Test individual components:
```python
# Test email fetching
from email_files.pull_mails import fetch_unread_emails
emails = fetch_unread_emails()

# Test AI classification
from email_files.process_mails import classify_and_parse_email
import asyncio
bug = asyncio.run(classify_and_parse_email(subject, body, from_email))

# Test GitScrum integration
from gitscrum_files.git_scrum import create_task_on_gitscrum
task = create_task_on_gitscrum("Test Task", "Description")
```

## Troubleshooting

### Email Connection Issues
- Verify IMAP/SMTP credentials
- Check if 2FA requires app passwords
- Ensure firewall allows email ports (993, 587)

### AI Classification Not Working
- Verify Google AI API key is valid
- Check API quota limits
- Review email format and content

### GitScrum Tasks Not Creating
- Verify API key and project ID
- Check network connectivity
- Review GitScrum API rate limits

## License

[Your License Here]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions, please create an issue in the repository.
