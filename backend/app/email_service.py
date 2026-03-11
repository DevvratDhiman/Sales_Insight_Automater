import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_summary_email(email, summary):

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": "Sales Insights <onboarding@resend.dev>",
        "to": [email],
        "subject": "Your AI Sales Insights Report",
        "html": f"""
        <h2>AI Sales Dataset Summary</h2>
        <p>{summary}</p>
        """
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()