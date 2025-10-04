from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)