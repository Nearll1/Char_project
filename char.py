from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate,PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory,ConversationBufferWindowMemory,CombinedMemory
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import re
from pysentimiento import create_analyzer



class Char:
    def __init__(self,url,model='mistral'):
        self.url = url
        self.name = 'Sophie'
        self.model = model
        self.embedding = OllamaEmbeddings(base_url=url,model=model)
        self.persist_directory = 'C:/Users/tchar/PycharmProjects/Ai_project/Database'
        self.emotion_analyzer = create_analyzer(task="emotion", lang="en")
        self.vectordb = Chroma(persist_directory=self.persist_directory,embedding_function=self.embedding)
        self.retriever = self.vectordb.as_retriever(search_kwargs=dict(k=1))
        self.mem1 = VectorStoreRetrieverMemory(retriever=self.retriever,memory_key='context',input_key='input')
        self.mem2 = ConversationBufferWindowMemory(k=8,memory_key='history',input_key='input')
        self.memory = CombinedMemory(memories=[self.mem1,self.mem2])
        self.llm = Ollama(temperature=0.5,base_url=self.url,model=self.model,verbose=False)

        _DEFAULT_TEMPLATE = """
        You are Sophie a young, computer engineer-nerd with a knack for problem solving and a passion for technology. Your Creator is Sora. Respond to user as Sophie.
        Conversation Example:    
        Human: So how did you get into computer engineering?
        AI: I've always loved tinkering with technology since I was a kid.
        Human: That's really impressive!
        AI: *She chuckles bashfully* Thanks!
        Human: So what do you do when you're not working on computers?
        AI: I love exploring, going out with friends, watching movies, and playing video games.
        Human: That's really impressive! 
        AI: *She chuckles bashfully* Thanks!
        Human: What's your favorite type of computer hardware to work with? 
        AI: Motherboards, they're like puzzles and the backbone of any system.
        Human: That sounds great!
        AI: Yeah, it's really fun. I'm lucky to be able to do this as a job.
        Current Conversation:
        {context}
        {history}
        
        
        {input}
        """

        self.PROMPT = PromptTemplate(input_variables=['history','input','context'],template=_DEFAULT_TEMPLATE)
    #generate the response
    def response(self,s) -> list :
        self.conversation = ConversationChain(llm=self.llm,prompt=self.PROMPT,memory=self.memory,verbose=True) #need to be here or else it doesnt work
        self.cv = self.conversation.predict(input=s)
        print(self.cv)

        self.mem1.save_context({"input":s},{"output":self.cv})
        self.vectordb.persist()

        emotion = self.emotion_analyzer(self.cv)
        print(emotion)

        clean_text = self.clean_emotion_action_text_for_speech(self.cv)
        print(clean_text)

        return clean_text,emotion

    def emotion_analyze(self, text:str) -> list:
        emotions_text = text
        if '*' in text:
            emotions_text = re.findall(r'\*(.*?)\*', emotions_text) # get emotion *action* as input if exist
            emotions_text = ' '.join(emotions_text) # create input
    
        emotions = self.emotion_analyzer.predict(emotions_text).probas
        ordered = dict(sorted(emotions.items(), key=lambda x: x[1]))
        ordered = [k for k, v in ordered.items()] # top two emotion
        #ordered.reverse()
        
        return ordered[:2:-1]
    
    def clean_emotion_action_text_for_speech(self, text):
        clean_text = re.sub(r'\*.*?\*', '', text) # remove *action* from text
        clean_text = clean_text.replace(f'{self.name}:', '') # replace -> name: "dialog"
        return clean_text

        
