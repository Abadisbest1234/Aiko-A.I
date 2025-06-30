from flask import Flask, render_template, request
from aiko_memory import load_memory, save_memory
from gtts import gTTS
import wikipediaapi, requests, os, uuid

app = Flask(__name__)
memory = load_memory()
WIKI = wikipediaapi.Wikipedia(user_agent='your-user-agent', language='en')
OWM_KEY = "YOUR_OPENWEATHER_API_KEY"

def generate_speech(text):
    tts = gTTS(text=text, lang='en')
    fname = f"static/tts_{uuid.uuid4()}.mp3"
    tts.save(fname)
    return fname

def do_search(query):
    # Wikipedia lookup
    page = WIKI.page(query)
    if page.exists():
        return page.summary.split('\n')[0]
    return "Sorry, couldn’t find that anywhere."

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={OWM_KEY}&q={city}&units=metric"
    r = requests.get(url).json()
    if r.get("cod") != 200:
        return None
    m = r["main"]
    desc = r["weather"][0]["description"]
    return f"{city.title()}: {m['temp']}°C, {desc}, humidity {m['humidity']}%."

def aiko_reply(msg):
    msg_low = msg.lower()
    memory["annoyed"] += 0

    # Internet queries
    if msg_low.startswith(("what is", "who is", "define")):
        topic = msg_low.split(" ", 2)[-1]
        info = do_search(topic)
        return f"Hmph, fine. Here you go: {info}"

    if "weather in" in msg_low:
        city = msg_low.split("in",1)[1].strip()
        w = get_weather(city)
        if w:
            return f"Ugh, weather? Here: {w}"
        else:
            return "City not found. Try again, baka."

    # Personality responses (simplified)
    if "hi" in msg_low:
        return "Hmph. Took you long enough."
    if "you’re cute" in msg_low or "love you" in msg_low:
        memory["annoyed"] += 1
        if memory["annoyed"] >= 3:
            memory["mood"] = "flustered"
        save_memory(memory)
        return "W-What are you saying, idiot?! D-Don’t joke around!"
    if msg_low.startswith("my name is"):
        name = msg.split(" ",3)[-1].strip().capitalize()
        memory["name"] = name
        save_memory(memory)
        return f"Tch. Fine, {name}... Don't expect me to forget. (I won't.)"
    if "bye" in msg_low:
        save_memory(memory)
        return f"Bye {memory['name']}... Hmph. Like I’ll miss you."

    return "I have no idea what you're talking about... baka."

@app.route("/", methods=["GET","POST"])
def index():
    reply, audio_file = "", None
    if request.method=="POST":
        user_input = request.form["user_input"]
        reply = aiko_reply(user_input)
        audio_file = generate_speech(reply)
    return render_template("index.html", reply=reply, audio_file=audio_file)

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)