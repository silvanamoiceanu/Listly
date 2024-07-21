import imaplib
import email
from email.header import decode_header
import datetime
import csv
import re

def connect_to_email(email_address, password, imap_server):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, password)
    return mail

def get_emails(mail, folder="INBOX", limit=100):
    mail.select(folder)
    _, search_data = mail.search(None, "ALL")
    email_ids = search_data[0].split()
    return email_ids[-limit:]  # Get the latest 'limit' emails

def decode_email_subject(subject):
    decoded, encoding = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or 'utf-8')
    return decoded

def calculate_priority(subject, sender, date):
    priority = 0
    
    # Check for urgent keywords in subject
    urgent_keywords = ['urgent', 'important', 'asap', 'deadline']
    if any(keyword in subject.lower() for keyword in urgent_keywords):
        priority += 5
    
    # Prioritize recent emails
    days_old = (datetime.datetime.now() - date).days
    if days_old == 0:
        priority += 3
    elif days_old <= 2:
        priority += 2
    elif days_old <= 7:
        priority += 1
    
    # Prioritize based on sender (example: prioritize emails from your boss)
    if 'boss@company.com' in sender:
        priority += 3
    
    return priority

def process_emails(mail, email_ids):
    prioritized_emails = []
    
    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)
        
        subject = decode_email_subject(email_message["subject"])
        sender = email_message["from"]
        date = datetime.datetime.strptime(email_message["date"], "%a, %d %b %Y %H:%M:%S %z")
        
        priority = calculate_priority(subject, sender, date)
        
        prioritized_emails.append({
            "subject": subject,
            "sender": sender,
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "priority": priority
        })
    
    return sorted(prioritized_emails, key=lambda x: x["priority"], reverse=True)

def save_to_csv(prioritized_emails, filename="email_priorities.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["subject", "sender", "date", "priority"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for email in prioritized_emails:
            writer.writerow(email)

def main():
    email_address = "hackathonemail8@gmail.com"
    password = "UxxQF2yy"
    imap_server = "imap.example.com"
    
    mail = connect_to_email(email_address, password, imap_server)
    email_ids = get_emails(mail)
    prioritized_emails = process_emails(mail, email_ids)
    save_to_csv(prioritized_emails)
    
    mail.logout()

if __name__ == "__main__":
    main()