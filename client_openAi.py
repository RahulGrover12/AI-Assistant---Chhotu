from openai import OpenAI
client = OpenAI(
    api_key="YOUR_API_KEY"
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Give a short description."},
        {
            "role": "user",
            "content": "What is coding?"
        }
    ]
)
  
print(completion.choices[0].message.content)