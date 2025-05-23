from typing import TypedDict

class Email(TypedDict):
    email_id: str
    thread_id: str
    labels_id: list
    sender: str
    to: str
    timestamp: str
    subject: str
    body: str
    category: str
