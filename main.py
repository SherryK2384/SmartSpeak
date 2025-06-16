import speech_recognition as sr
import os
import webbrowser
from together import Together
from config import apikey
import datetime
import random
import pyttsx3

chatStr = ""

# Initialize Together.ai
client = Together(api_key=apikey)

def chat(query):
    global chatStr
    chatStr += f"Harry: {query}\nJarvis: "
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",  # Make sure the model name is correct
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=256
        )
        answer = response.choices[0].message.content.strip()
        say(answer)
        chatStr += f"{answer}\n"
        return answer
    except Exception as e:
        say("Sorry, I encountered an error.")
        print(f"Error in chat: {e}")
        return "Error"


def ai(prompt):
    try:
        text = f"TogetherAI response for Prompt: {prompt} \n *************************\n\n"
        response = client.Complete.create(
            prompt=prompt,
            model="togethercomputer/llama-2-70b-chat",
            max_tokens=256,
            temperature=0.7,
            top_p=1,
            repetition_penalty=1.0
        )
        answer = response["output"]["choices"][0]["text"]
        text += answer

        if not os.path.exists("TogetherAI"):
            os.mkdir("TogetherAI")

        safe_name = f"{''.join(prompt.split('intelligence')[1:]).strip() or 'response'}"
        with open(f"TogetherAI/{safe_name}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        say("Could not process your AI request.")
        print(f"Error in AI function: {e}")

engine = pyttsx3.init()
def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()

        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath = "https://open.spotify.com/"
            os.system(f"open {musicPath}")

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {minute} minutes")

        elif "open facetime" in query.lower():
            os.system("open /System/Applications/FaceTime.app")

        elif "open pass" in query.lower():
            os.system("open /Applications/Passky.app")

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "jarvis quit" in query.lower():
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
