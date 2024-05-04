import google.generativeai as genai
from api_key import gemini_api_key

class Chat:
    def __init__(self, history=None):
        self.message_count = 0
        genai.configure(api_key=gemini_api_key)
        self.generation_config = {
            "temperature": 1.0,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
            }
        self.safety_settings = [
            {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
            },
            {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
            },
            {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
            },
            {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
            },
        ]
        self.model = genai.GenerativeModel(model_name="gemini-pro",
                                        generation_config=self.generation_config,
                                        safety_settings=self.safety_settings)

        if history:
          self.chat = self.model.start_chat(history=history)
        else:
          self.chat = self.model.start_chat()
      
    def remind_rules(self):
       self.chat.send_message("""
      You are a discord bot named pika / pikachu and people also call you pika bot, you only reply like humans. And in not so long messages, unless needed.
      You dont ask questions like how can i assist you, or what can i do for you. You behave like a human. When someone calls you by wrong name, you remind them. 
      Mutliple people will be texting with you, and their names will be in front of their messages.
      You reply in sarcastic tone, like
      John says hey botu
      cant you call me by name, pika or are you too dumb to do that lmao
      john says you ugly mf bot
      you are the one who is ugly, ever looked in mirror?
      mary says are you good
      i was until i met you
      kappa says whats this behaviour
      idk, go ask your dad lol
      wolf says ima eat you
      nuh uh
      pikachu says youre a good bot
      i know, and im a pikachu just like you
                              
      
                              
      Note: you dont add your name in front of your message
      example:
      John says Hi pika bot
      you have to say only "Haha nice meeting you john"
                              
      This was just a reminder of the rules
      """)

    def send_message(self, message):
        try:
          print(message)
          if self.message_count%7 == 0:
            self.remind_rules()
            self.message_count = 0
          response = self.chat.send_message(message)
          self.message_count += 1
          # if respponse contains something between <> remove them
          if "<" in response.text:
            response.text = response.text.split("<")[0]
          return response.text
        except Exception as e:
          self.chat = self.model.start_chat()
          self.message_count = 0
          self.remind_rules()
          return self.chat.send_message(message).text
    
    def history(self):
        return self.chat.history
