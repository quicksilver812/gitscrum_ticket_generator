import imapclient
import pyzmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def fetch_unread_emails():
    with imapclient.IMAPClient(EMAIL_HOST) as client:
        client.login(EMAIL_USER, EMAIL_PASS)
        client.select_folder("INBOX", readonly=False)
        
        # Search for unseen emails
        UIDs = client.search(["UNSEEN"])
        emails = []

        for uid in UIDs:
            raw_message = client.fetch(uid, ["BODY[]", "FLAGS"])
            message = pyzmail.PyzMessage.factory(raw_message[uid][b"BODY[]"])

            subject = message.get_subject()
            from_email = message.get_addresses("from")[0][1]
            
            if message.text_part:
                body = message.text_part.get_payload().decode(message.text_part.charset)
            elif message.html_part:
                body = message.html_part.get_payload().decode(message.html_part.charset)
            else:
                body = ""

            emails.append({
                "uid": uid,
                "from": from_email,
                "subject": subject,
                "body": body
            })

        return emails
