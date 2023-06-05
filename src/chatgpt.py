import openai
from config import *

class ChatGTP:
  def __init__(self): 
    openai.api_key = OPENAI_API_KEY
    self.past_messages = []
  
  def completion(self, new_message_text:str, settings_text:str = ''):
    new_message = {"role": "user", "content": new_message_text}
    self.past_messages.append(new_message)

    result = openai.ChatCompletion.create(
      model=CHATGPT_MODEL,
      messages=self.past_messages
    )
    response_message = {"role": "assistant", "content": result.choices[0].message.content}
    self.past_messages.append(response_message)
    response_message_text = result.choices[0].message.content
    return response_message_text, self.past_messages, result

if __name__ == "__main__":
  chatgpt = ChatGTP()
  response_message_text, past_messages = chatgpt.completion("""\
Hello World Hello World Hello World Hello World Hello World Hello World Hello World Hello World hello
""")
  print(response_message_text)