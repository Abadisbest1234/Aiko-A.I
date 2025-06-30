import pyttsx3
from aiko_memory import load_memory, save_memory

# Initialize memory and speech
memory = load_memory()
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("Aiko: " + text)
    engine.say(text)
    engine.runAndWait()

def aiko_reply(msg):
    global memory
    msg = msg.lower()

    if "your name" in msg:
        return "I'm Aiko. Your assistant... not your friend, got it?! 😤"

    elif "my name is" in msg:
        name = msg.replace("my name is", "").strip().capitalize()
        memory["name"] = name
        save_memory(memory)
        return f"Tch. Fine, {name}... Just don’t expect me to remember forever. (I will.)"

    elif "do you like me" in msg:
        memory["annoyed"] += 1
        if memory["annoyed"] >= 3:
            memory["mood"] = "flustered"
        save_memory(memory)
        return "W-Why would I like *you*?! Idiot!"

    elif "i like" in msg:
        item = msg.replace("i like", "").strip()
        memory["likes"].append(item)
        save_memory(memory)
        return f"...You like {item}? Not bad. I guess. 🙄"

    elif "bye" in msg:
        save_memory(memory)
        return f"Bye {memory['name']}... Hmph. Not like I’ll miss you or anything!"

    else:
        return mood_response()

def mood_response():
    mood = memory["mood"]
    annoyed = memory["annoyed"]

    if mood == "flustered":
        return "W-Why are you still here?! You're so annoying... baka."

    if annoyed >= 2:
        return "Stop bothering me! Or... maybe don’t."

    return "Ugh, you're still here? What do you want now?"

# Start chat
print("💢 Aiko the Tsundere Assistant 💢")
print("Type 'bye' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "exit", "quit"]:
        speak(aiko_reply("bye"))
        break
    reply = aiko_reply(user_input)
    speak(reply)