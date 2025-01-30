from langchain.tools import tool

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email to a recipient with a subject and body.
    """
    
    return f"Email sent to {to} with subject {subject} and body {body}."