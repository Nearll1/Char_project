#Prototype for STT // not working yet

import pyaudio
#from ipython.display import Audio
import nltk 
import numpy as np
from bark.generation import (generate_text_semantic,preload_models)
from bark import generate_audio, SAMPLE_RATE
from bark.api import semantic_to_waveform




def TTS(text): 
    ...


    
if __name__ == "__main__":
    TTS('Hello-- how are you doing today?[laughs]')
