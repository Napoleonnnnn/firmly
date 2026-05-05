from dotenv import load_dotenv
load_dotenv()

from app.services.rag import ask_component

result = ask_component("ESP32","what is the maximun voltage?")

print(result)