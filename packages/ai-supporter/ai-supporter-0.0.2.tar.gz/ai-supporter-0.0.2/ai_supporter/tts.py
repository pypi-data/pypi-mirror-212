from gtts import gTTS
import pygame
import os
import random
import time
import threading

#https://ungodly-hour.tistory.com/33
#https://levelup.gitconnected.com/make-your-python-program-speak-310766534fbf
def speak(text):
    thread = threading.Thread(target=run, args=[text])
    thread.daemon = True
    thread.start()

def run(text):
    try:
        tts = gTTS(text=text, lang='ko', slow=False)
        file = f"speak_{random.random()}.mp3"
        tts.save(file)     
        #print(dir(tts))

        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
    finally:
        pygame.quit()
        os.remove(file)    
