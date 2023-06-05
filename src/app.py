import os
from slack_bolt import App
import logging
import json
import openai
from slack_sdk.web import WebClient
import ssl as ssl_lib
import certifi
import re
from chatgpt import ChatGTP
from chatbot import Chatbot
from openai.error import InvalidRequestError
from config import *
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

os.environ["OPENAI_API_KEY"] = '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'
# Initializes your app with your bot token and signing secret
app = App(
  token = SLACK_BOT_TOKEN,
  signing_secret = SLACK_SIGNING_SECRET
)

loader = CSVLoader(file_path='../data/output/prods.csv')
data = loader.load()

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(data, embeddings)

logger = logging.getLogger(__name__)
channel_chatgpt = {}

def _remove_mention(text):
  """Remove the mention from the text"""
  return re.compile(r'<@[^>]+>').sub('', text).lstrip()

# Add functionality here
@app.message("Hello")
def answer(message, say):
    user = message['user']
    say(f"Hello, glad to see you <@{user}>!")


@app.event("message")
def handle_message_events(body, say, logger):
  try:
    event_user = body.get("event", {}).get("user")
    event_text = body.get("event", {}).get("text")
    event_channel = body.get("event", {}).get("channel")

    if event_channel not in channel_chatgpt:
      channel_chatgpt[event_channel] = Chatbot(vectorstore)
    chatbot = channel_chatgpt[event_channel]
    say(f"Processing your request...")
    try:
      #response_message_text  = chatbot.conversational_chat(event_text)
      chain = chatbot.conversational_chat(event_text)
      chain_input = {"question": event_text, "chat_history":''}
      result = chain(chain_input)
      response_message_text = result['answer']
    except Exception as err:
      raise err
    
  except Exception as err:
    say(f"""\
<@{event_user}>
Opps! Something went wrong {err}
Reply `reset` to reset the conversation.
""")
  else:
    say(f"""\
<@{event_user}>
""")
    say(response_message_text)
  

@app.event("app_mention")
def handle_mention(body, say, logger):
  past_messages = []
  result = {}
  try:
    event_user = body.get("event", {}).get("user")
    event_ts = body.get("event", {}).get("ts")
    event_text = _remove_mention(body.get("event", {}).get("text"))
    event_channel = body.get("event", {}).get("channel")

    if event_channel not in channel_chatgpt:
      channel_chatgpt[event_channel] = ChatGTP()
    chatgpt = channel_chatgpt[event_channel]

    # Reset the conversation
    if event_text == "reset":
      chatgpt.past_messages = []
      say(f"Conversation reset.")
      return

    say(f"<@{event_user}> Processing your request...")
    try:
      response_message_text, past_messages, result = chatgpt.completion(event_text)
    except Exception as err:
      raise err

  except Exception as err:
    say(f"""\
<@{event_user}>
Opps! Something went wrong {err}
Reply `reset` to reset the conversation.
""")
  else:
    say(f"""\
<@{event_user}>
====================
{response_message_text}
""")


# Start your app
if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(port=int(os.environ.get("PORT", 80)))