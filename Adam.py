import ollama
import subprocess
from subprocess import DEVNULL, STDOUT
import speech_recognition as sr
import pyttsx3

ollamaServer = subprocess.Popen('cmd.exe /K ollama serve',stdout=DEVNULL,stderr=STDOUT) 
modello="Adam"
r = sr.Recognizer()

#Function definitions
def Listen():
    while(1):    

        print("\nListening..")
        # Exception handling to handle
        # exceptions at the runtime
        try:
         
        # use the microphone as source for input.
            with sr.Microphone() as source2:
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2)
             
            #listens for the user's input 
                audio2 = r.listen(source2)
             
            # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
 
                print('"',MyText,'"')
                return MyText
             
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("\nCould not understand.")
def speak(command):
    engine = pyttsx3.init()
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
    engine.say(command) 
    engine.runAndWait()
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

def sendMessageToAIAsSystem(content):
    stream = ollama.chat(
        model=modello,
        messages=[{'role': 'system', 'content':content}],
        stream=True,
        )
    
    phrase=""
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        phrase=phrase + chunk['message']['content']
    return phrase


#Greeting
answer=sendMessageToAI("You have been booted up, greet the user very shortly.")
speak(answer)

#Input dialogue
inp=Listen()
while not("shut down" in inp):
    answer=sendMessageToAI(inp)
    if not(answer=="1"):
        speak(answer)
    inp=Listen()

#Saying goodbye
answer=sendMessageToAIAsSystem("You are being shutdown by the user. Say farewell to him.")
speak(answer)
ollamaServer.kill()