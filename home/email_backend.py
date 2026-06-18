import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class UnverifiedEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
            
        # FIXED: Points to Brevo's live transaction server route
        url = "https://api.brevo.com/v3/smtp/email"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": settings.EMAIL_HOST_PASSWORD
        }
        
        sent_count = 0
        for message in email_messages:
            payload = {
                "sender": {"name": "CarePulse Hospital", "email": settings.DEFAULT_FROM_EMAIL},
                "to": [{"email": to_email} for to_email in message.to],
                "subject": message.subject,
                "textContent": message.body
            }
            
            try:
                response = requests.post(url, json=payload, headers=headers)
                
                # FIXED: Checks for successful HTTP creation array list responses
                if response.status_code in [200, 201, 202]:
                    sent_count += 1
                else:
                    if not self.fail_silently:
                        print(f"\n--- Brevo API Delivery Feedback ---")
                        print(f"Status Code received: {response.status_code}")
                        print(f"Response Body error: {response.text}\n")
            except Exception as e:
                if not self.fail_silently:
                    raise e
                    
        return sent_count

