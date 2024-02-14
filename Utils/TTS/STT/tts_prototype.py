import os
import torch
import pyaudio
import wave
import time

def tts(text,):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'
    print('got here!')
    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file(f'https://models.silero.ai/models/tts/en/v3_en.pt',
                                    local_file)  
    print('got here!!')
    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)
    print('got here!!!')
    example_text = str(text).strip().lower()
    sample_rate = 48000
    speaker='en_67'
    print('got here!!!!')

    audio_paths = model.save_wav(text=example_text,
                                speaker=speaker,
                                sample_rate=sample_rate)
    #with open("reply.wav", "wb") as outfile:
        #outfile.write(audio_paths.content)
    print('got here!!!!!!')
    return 'test'

def stream(n: str) -> None:
    
    CHUNK = 1024
    
    with wave.open(f'{n}.wav','rb') as wf:
        def callback(in_data,frame_count,time_info,status):
            data = wf.readframes(frame_count)
            return (data,pyaudio.paContinue)
        
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)
        
    
        while stream.is_active():
            time.sleep(0.1)

            

        stream.close()
        p.terminate()
        return None

if __name__ == "__main__":
    tts('Hello, how are you today?')
