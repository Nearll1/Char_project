import threading
from Utils.Twitch.twitch import twitchbot
import time
from char import Char
from Utils.TTS.STT.tts_prototype import *
from Utils.VTS_plugins.vts_plugin import Emotion
import asyncio
from dotenv import load_dotenv
import os

#Dear user, i wish you goodluck!

load_dotenv()

#get path to Database
path = os.path.join(os.path.dirname(__file__),'Database')


#Twitch auth
channel = os.getenv('CHANNEL_NAME')
nickname = os.getenv('NICKNAME')
token = os.getenv('OAUTH_TOKEN')

#Ollama api (NO CHATGPT FOR YA!)
ollama_api = ''


#Run the VTS controller
control = Emotion()
asyncio.run(control.connect_auth())

#Instanciate the chatbot
rp = Char(url=ollama_api,model='mistral',path=path)

#Mode 1 to run as a streamer else run as a normal chatbot
mode = input('Mode >> ')


#Where the magic happens
async def main():
    sem = asyncio.Semaphore(10)
    while True:
        transcript = get_transcript()
        response,emotion = get_response(transcript)
        audio_file = tts(response)
        
        await sem.acquire()
        try:
            y = threading.Thread(target=stream,args=[audio_file])
            y.start()
            if mode == '1':
                x = threading.Thread(target=lambda :asyncio.run(main()))
                x.start()
            y.join()
            asyncio.run(control.trigger(emotion))
            print('Response Completed!')
        finally:
            sem.release()
  

#get the user input
def get_transcript() -> str:
    if mode == '1':
        while(len(bot.chat_history) == 0):
                print("no new messages")
                time.sleep(1)
            
        if len(bot.chat_history) > 5:
            bot.chat_history = bot.chat_history[-5:]
                
            transcript = f'{bot.chat_history[0][0]} : {bot.chat_history[0][1]}'
            print(transcript)
            bot.chat_history.pop(0)
            return transcript
    else:
        return input('>> ')

#get the AI response
def get_response(s: str):
    response,emotion = rp.response(s)

    return response,emotion



if __name__ == '__main__':
    if mode == '1':
        #Start receiving msg from twitch live chat
        bot = twitchbot(channel,nickname,token)
        threading.Thread(target=bot.run()).start()
        print(bot.chat_history)

        asyncio.run(main())

    else:
        asyncio.run(main())
