from email.message import Message
from typing import List
from log import generate_log
import os

from simplegmail import Gmail
from simplegmail.message import Message
from simplegmail.query import construct_query


gmail = Gmail()


class SubjectEmail():
    tag: str
    system: str

    def __init__(self, tag, system):
        self.tag = tag
        self.system = system


def get_emails(subject: SubjectEmail) -> List[Message]:
    newer_than = int(os.getenv("EMAIL_NEWER_THAN", 2))
    newer_than_unit = os.getenv("EMAIL_NEWER_THAN_UNIT", "year")
    user = os.getenv("EMAIL_USER_ID", "")

    query_params = {
        "newer_than": (newer_than, newer_than_unit),
        "subject": subject.tag,
        "unread": True,
    }

    try:
        if user:
            messages = gmail.get_messages(user_id=user,
                query=construct_query(query_params))
        else:
            messages = gmail.get_messages(
                query=construct_query(query_params))
    except Exception as fail:
        generate_log('exception request emails, fail: %s!' %(fail))

    print(subject.tag)
    generate_log('get emails successful! return %d messages.' %(len(messages)))

    return messages

def update_email(messages: List[Message]):
    for message in messages:
        try:
            message.mark_as_read()
            generate_log('message id: %s, alter status unread to read.' %(message.id))
        except Exception as fail:
            generate_log('exception update mensage id: %s, fail: %s!' %(message.id, fail))
