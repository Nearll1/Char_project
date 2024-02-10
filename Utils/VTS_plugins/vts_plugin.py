import pyvts
import asyncio

class Emotion:
    def __init__(self):
        
        self.hotkeys_list = {
            "neutral": None,
            "agree": "31abbc83310a49239e127d059fcc68ad",
            "wonder": "a7124841a0a745ceb0d49127066f4a02",
            "shy": "N4",
            "joy": "a5570764d55844dfbac32d43b232c1de",
            "sad": "N5",

        }
        self.plugin_info = {
            "plugin_name": "model control",
            "developer": "Sora",
            "authentication_token_path": "./token.txt"
        }
        self.myvts = pyvts.vts(plugin_info=self.plugin_info)
    #connect the plugin to VTS   
    async def connect_auth(self):
        
        await self.myvts.connect()
        await self.myvts.request_authenticate_token()
        await self.myvts.request_authenticate()
        await self.myvts.close()
    
    #(SHOULD)get all model animations from VTS
    async def get_triggers(self,):
        
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        
        
        
        hotkeys = await self.myvts.request(self.myvts.vts_request.requestHotKeyList())
        
        for hotkey in hotkeys['data']['availableHotkeys']:
            name = hotkey['name'].lower()
            self.hotkeys_list[name] = hotkey['hotkeyID']
        #print(self.hotkeys_list,hotkey['hotkeyID'])
            print(hotkey)

        await self.myvts.close()
    #trigger the animation
    async def trigger(self,emotions):
         
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        
        for emotion in emotions:
            if emotion in self.hotkeys_list:
                    buttom = self.hotkeys_list[emotion]
            break
    
        if not buttom:
            return None
        
            
        send_hotkeys_request = self.myvts.vts_request.requestTriggerHotKey(hotkeyID=buttom)

        await self.myvts.request(send_hotkeys_request)
        
        await self.myvts.close()
    
if __name__ == "__main__":
    w = Emotion()
    print('---------')
    asyncio.run(w.connect_auth())
    print('---------------------')
    print(asyncio.run(w.get_triggers()))
    print('---------------------')
    print(asyncio.run(w.trigger('joy')))


