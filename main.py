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

#Twitch auth
channel = os.getenv('CHANNEL_NAME')
nickname = os.getenv('NICKNAME')
token = os.getenv('OAUTH_TOKEN')

#Ollama api (NO CHATGPT FOR YA!)
ollama_api = '...'


#Run the VTS controller
control = Emotion()
asyncio.run(control.connect_auth())

mode = input('Mode >> ')


#Where the magic happens
def main():
    while True:
        while(len(bot.chat_history) == 0):
            print("no new messages")
            time.sleep(1)
        
        if len(bot.chat_history) > 5:
            bot.chat_history = bot.chat_history[-5:]
            
        transcript = f'{bot.chat_history[0][0]} : {bot.chat_history[0][1]}'
        print(transcript)
        
        
        rp = Char(url=ollama_api,model='mistral')
        bot.chat_history.pop(0)
        response,emotion = rp.response(transcript)
        print(response)
        print('--------')
        print(emotion)
        
        audio_file = tts(response)
        stream(audio_file)
        if emotion:
            asyncio.run(control.trigger(emotion))
        print('Response Completed!')

def mode_0():
    while True:
        rp = Char(ollama_api,model='mistral')
        user_msg = input('>')
        if user_msg.lower() == 'exit':
            break
        response,emotion = rp.response(user_msg)
        print(response)
        print('--------')
        print(emotion)
            
        audio_file = tts(response)
        if not emotion:
            stream(audio_file)
            print('No emotion')
        stream(audio_file)
        asyncio.run(control.trigger(emotion))
        print('Response Completed!')  

if __name__ == '__main__':
    if mode == '1':
        #Start receiving msg from twitch live chat
        bot = twitchbot(channel,nickname,token)
        threading.Thread(target=bot.run()).start()
        print(bot.chat_history)

        main()

    else:
        mode_0()
