"""
import logging, json, certifi, re, uuid, base64, regex, binascii
from peewee import DoesNotExist
from requests import Request, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from common.constants import Constants
from database.db_operations import create_record, get_record_by_field, update_record
from database.database_config import db_conn
from database.models import Conversation, Messages, User, FollowUpQuestion, Language, MultilingualText
from django_core.config import Config
from django_core import celery
from language_service.translation import *
from language_service.utils import get_language_by_code

logger = logging.getLogger(__name__)
"""

def send_request(
    url, headers={}, 
    #data=None, 
    #content_type="form-data", 
    #request_type="GET", 
    #total_retry=10, 
    #params=None
):
    """
    Generic helper function to send requests to a specified URL with the relevant HTTP method,
    query params, request body, content negotiation and number of retries.

    org defn:
    def send_request(
    url, headers={}, data=None, content_type="form-data", request_type="GET", total_retry=10, params=None
):
    """
    response = None
    try:
        if content_type == "JSON":
            headers["Content-Type"] = "application/json"
            data = json.dumps(data)

        request_obj = Request(request_type, url, data=data, headers=headers, params=params)
        session = Session()
        request_prepped = session.prepare_request(request_obj)
        retries = Retry(
            total=total_retry,
            backoff_factor=0.1,
            status_forcelist=[403, 502, 503, 504],
            allowed_methods={"GET", "POST", "PUT"},
        )
        session.mount(url, HTTPAdapter(max_retries=retries))
        response = session.send(
            request_prepped,
            stream=True,
            verify=certifi.where(),
            # verify=False,
        )
        logger.info(f"URL: {url} | Response Status Code: {response.status_code}")
        # json_response = json.loads(response.text) if response and response.status_code == 200 else {}
        # json_response.update({"status_code": response.status_code})
        # logger.info(f"Response: {json_response}")

    except Exception as error:
        logger.error(error, exc_info=True)

    return response


#def get_or_create_latest_conversation(conversation_data: dict) -> Conversation:
def get_or_create_latest_conversation(conversation_data):
    """
    Fetch the latest conversation instance if available or create a new conversation.
    def get_or_create_latest_conversation(conversation_data: dict) -> Conversation:
    """
    conversation = None
    user_id = conversation_data.get("user_id", None)
    try:
        with db_conn:
            conversation_qs = (
                Conversation.select()
                .where(Conversation.user_id == user_id)
                .order_by(Conversation.created_on.desc())
                # .get()
            )

        conversation = conversation_qs.get() if len(conversation_qs) >= 1 else None
        if not conversation:
            conversation = create_record(Conversation, conversation_data)
            logger.info(f"New conversation created for user_id:{user_id}")

    except Exception as error:
        logger.error(error, exec_info=True)

    return conversation

#def get_user_chat_history(user_id, window=Config.CHAT_HISTORY_WINDOW):
def get_user_chat_history(user_id, ):
    """
    Fetch user chat history by querying the previous messages associated with the user.
    def get_user_chat_history(user_id, window=Config.CHAT_HISTORY_WINDOW):
    """
    chat_history = None
    with db_conn:
        conversation = get_or_create_latest_conversation({"user_id": user_id})
        messages = (
            Messages.select()
            .where(
                Messages.conversation_id == conversation.id,
                Messages.is_deleted == False,
                Messages.translated_message != None,
                Messages.message_response != None,
            )
            .order_by(Messages.created_on.desc())
            .limit(window)
        )
        chat_history = ""
        for message in reversed(messages):
            chat_history = (
                chat_history + f"\n\nUser : {message.translated_message}\nAI Assistant : {message.message_response}"
            )
        # history.append((message.translated_message, message.message_response))

    # print(f"\n ######## USER CHAT HISTORY BEGINS ########\n{chat_history} ######## USER CHAT HISTORY END ########\n")
    # logger.info(f"User chat history :\n {chat_history}")
    return chat_history
