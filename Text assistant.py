import ollama
import subprocess
from subprocess import DEVNULL, STDOUT

ollamaServer = subprocess.Popen('cmd.exe /K ollama serve',stdout=DEVNULL,stderr=STDOUT) 
modello="phi3"

#Function definitions

def sendMessageToAI(content):
    stream = ollama.chat(
        model=modello,
        messages=[{'role': 'user', 'content':content}],
        stream=True,
        )

    phrase=""
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        phrase=phrase + chunk['message']['content']
    return phrase



#Greeting
answer=sendMessageToAI("You have been called, briefly greet the user")
#Input dialogue
inp=input(">>")
while not("shut down" in inp):
    answer=sendMessageToAI(inp)
    inp=input(">>")

#Saying goodbye
answer=sendMessageToAI("You are being shutdown, briefly farewell the user")
ollamaServer.kill()