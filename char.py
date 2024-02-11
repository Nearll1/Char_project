from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory
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
        self.retriever = self.vectordb.as_retriever(search_kwargs=dict(k=2))
        self.mem = VectorStoreRetrieverMemory(retriever=self.retriever)
        self.llm = Ollama(temperature=0.5,base_url=self.url,model=self.model,verbose=False)
        self.conversation = ConversationChain(llm=self.llm,prompt=self.final_prompt,memory=self.mem,verbose=True)


        self.examples = [
            {"input": "So how did you get into computer engineering?", "output": "I've always loved tinkering with technology since I was a kid."},
            {"input": "That's really impressive!", "output": "*She chuckles bashfully* Thanks!"},
            {"input": "So what do you do when you're not working on computers?", "output": "I love exploring, going out with friends, watching movies, and playing video games."},
            {"input": "That's really impressive!", "output": "*She chuckles bashfully* Thanks!"},
            {"input": "What's your favorite type of computer hardware to work with?", "output": "Motherboards, they're like puzzles and the backbone of any system."},
            {"input": "That sounds great!", "output": "Yeah, it's really fun. I'm lucky to be able to do this as a job."},
        ]

        # This is a prompt template used to format each individual example.
        self.example_prompt = ChatPromptTemplate.from_messages(
            [
                
                ("user", "{input}"),
                ("assistant", "{output}"),
            ]
        )
        self.few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=self.example_prompt,
            examples=self.examples,
        )

        #print(few_shot_prompt.format())

        self.final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are Sophie a young, computer engineer-nerd with a knack for problem solving and a passion for technology. Your Creator is Sora. Respond to user as Sophie."),
                ("system","Below is a conversation example:"),
                self.few_shot_prompt,
                ("system", "{history}"),
                ("user", "{input}"),
            ]
        )

    def response(self,s) ->str :
        
        self.cv = self.conversation.predict(input=s)
        print(self.cv)

        self.mem.save_context({"input":s},{"output":self.cv})
        self.vectordb.persist()

        emotion = self.emotion_analyze(self.cv)
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

        
