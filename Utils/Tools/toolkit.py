#NOT WORKING YET :)

from langchain_community.llms.ollama import Ollama
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory






class toolkit:
    def __init__(self,api,model='mistral'):
        self.api = api
        self.embeddings = OllamaEmbeddings(base_url=self.api,model=model)
        self.persist_directory = 'C:/Users/tchar/PycharmProjects/Ai_project/Database'
        self.vectordb = Chroma(persist_directory=self.persist_directory,embedding_function=self.embeddings)
        self.retriever = self.vectordb.as_retriever(search_kwargs=dict(k=2))
        self.llm = Ollama(temperature=0.5,base_url=self.api,model=model,verbose=False)
    def retrievers(self):
        prompt = ChatPromptTemplate.from_messages([
            ('system','{history}')
            ('user','input')
            ('user','Given the above conversation, generate a search query to look up in order to get information relevant to the conversation')
        ])
        
        retriever_chain = create_history_aware_retriever(llm=self.llm,retriever=self.retriever,prompt=prompt)
