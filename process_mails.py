from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dotenv import load_dotenv


from models.models import BugIssue

load_dotenv()

# Initialize provider as None
google_provider = None
google_model = None

def get_google_model():
    global google_provider, google_model
    if google_model is None:
        google_provider = GoogleProvider()
        google_model = GoogleModel("gemini-2.5-flash-lite", provider=google_provider)
    return google_model


async def classify_and_parse_email(email_subject: str, email_body: str, email_from: str):
    prompt = f"""
You are a customer support assistant. Determine if the following email describes a software issue/bug. 
If it is an issue, extract:
- Bug title
- User facing the bug (email or name)
- Bug summary  
- Bug priority (Low, Medium, High)

Let the default value of title be 'No title', user be 'Unknown user', summary be 'none' and priority be 'Medium'.
If the mail is not an issue/complaint, then register all the values as 'not_bug'
Also register any kind of follow up emails or replies as 'not_bug'

Email From: {email_from}
Email Subject: {email_subject}
Email Body: {email_body}
"""
    agent = Agent(
        model=get_google_model(),
        output_type=BugIssue,
        instructions=prompt
    )

    try:
        # Use the async run method instead of run_sync
        result_obj = await agent.run(email_body)
        result = result_obj.output.model_dump()

        if (
            result['title'] == 'not_bug' and
            result['user_email'] == 'not_bug' and
            result['summary'] == 'not_bug' and
            result['priority'] == 'not_bug'
        ):
            return None
        
        # Do the matching of domain from the bug to the respective email

        bug = BugIssue(
            title=result['title'],
            user_email=result['user_email'],
            summary=result['summary'],
            priority=result['priority']
        )
        return bug
    except Exception as e:
        print(f"Error processing email with AI: {e}")
        print(f"Error type: {type(e).__name__}")
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            print("Google API is temporarily unavailable. Please try again later.")
        return None


async def close_provider():
    global google_provider
    if google_provider is not None:
        try:
            if hasattr(google_provider, 'aclose'):
                await google_provider.aclose()
            elif hasattr(google_provider, 'close'):
                google_provider.close()
        except Exception as e:
            print(f"Error closing provider: {e}")