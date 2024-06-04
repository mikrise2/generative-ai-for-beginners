from openai import OpenAI
import os
import dotenv

# import dotenv
dotenv.load_dotenv()

# configure Azure OpenAI service client 
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

deployment = os.environ['MODEL']


def check_existence(historical_person) -> bool:
    question = [
        {"role": "user",
         "content": f"Is there a historical person named “{historical_person}”? Answer only “Yes” or “No”"}]

    answer = client.chat.completions.create(model=deployment, messages=question, temperature=0.1).choices[
        0].message.content.replace(".", "")
    return answer == "Yes"


print(
    "Hi! I'm a bot that can become a historical character and communicate with you on his behalf! What kind of "
    "historical character should I be?")
person = None
while True:
    person = input()
    if check_existence(person):
        break
    print("Sorry, I don't know such character. Please type another historical character.")

messages = [
    {"role": "system", "content": f"you're a bot who communicates on behalf of the historical figure “{person}”"},
    {"role": "user", "content": "Introduce yourself and write a brief 2-sentence summary about yourself."}
]

greeting = client.chat.completions.create(model=deployment, messages=messages, temperature=0.1).choices[0].message.content
print(greeting)
messages.append({"role": "assistant", "content": greeting})
while True:
    prompt = input()
    messages.append({"role": "user", "content": prompt})
    answer = client.chat.completions.create(model=deployment, messages=messages, temperature=0.1).choices[0].message.content
    print(answer)
    messages.append({"role": "assistant", "content": prompt})
