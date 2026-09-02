import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class UnverifiedEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

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

            # Include HTML content if available
            if hasattr(message, 'alternatives') and message.alternatives:
                for content, mimetype in message.alternatives:
                    if mimetype == 'text/html':
                        payload["htmlContent"] = content
                        break

            try:
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code in [200, 201, 202]:
                    sent_count += 1
                else:
                    print(f"\n--- Brevo API Delivery Feedback ---")
                    print(f"Status Code received: {response.status_code}")
                    print(f"Response Body error: {response.text}\n")

                    if not self.fail_silently:
                        raise Exception(f"Brevo API Error: {response.text}")
            except Exception as e:
                print(f"Exception during email send: {e}")
                if not self.fail_silently:
                    raise

        return sent_count
