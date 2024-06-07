"""
This code will load your pdf file, read and extract the data by using PdfReader.
Once we get the text we can make chunks of the data by providing chunk size and chunk overlap value in text splitter.
After we get the chunks we can create embeddings and stores those vectors in Chroma database .
We have used ConversationSummaryBufferMemory which works in storing the buffer and summary of conversation in memory 
and used RedisChatMessageHistory as cache memory for storing message history.
ConversatinalRetrievalChain which will help to give output as explicitly combining with history and query
and retrieve output by llm.
"""
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_message_histories import RedisChatMessageHistory
# from langchain.chains.conversational_retrieval.prompts import QA_PROMPT
from langchain.document_loaders import PyPDFLoader
from langchain.callbacks import get_openai_callback
import os
os.environ['OPENAI_API_KEY']=""

# loading pdf file
loader = PyPDFLoader("barakobama.pdf")
documents = loader.load()

# splitting the document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
texts = text_splitter.split_documents(documents)


# generating embedding and storing in vector db
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

# Connect to the Redis container using its URL
import subprocess
import redis_server
subprocess.Popen([redis_server.REDIS_SERVER_PATH])

_template = """Given the following conversation and a follow up question, 
rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

prompt_template_doc = """
Use the following pieces of context to answer the question at the end.
{context}
If you still cant find the answer, just say that you don't know, don't try to make up an answer.
You can also look into chat history.
{chat_history}
Question: {question}
Answer:
"""
prompt_doc = PromptTemplate(
    template=prompt_template_doc,
    input_variables=["context", "question","chat_history"]
)
#Using redis as cache memory for storing chat message history
message_history = RedisChatMessageHistory(session_id="my-session")

#Using ConversationSummaryBufferMemory as memory which stores buffer of interaction and summary
memory = ConversationBufferWindowMemory(
    llm = ChatOpenAI(model_name='gpt-3.5-turbo'),
    chat_memory=message_history,
    memory_key='chat_history',
    return_messages=True,
    output_key='answer',
    k=6)

#This chain retrieve answer 
model = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model_name='gpt-3.5-turbo',temperature=0),
    retriever=docsearch.as_retriever(),
    memory=memory,
    chain_type="stuff",
    return_source_documents=True,
    verbose=True,
    condense_question_prompt = CONDENSE_QUESTION_PROMPT,
    get_chat_history=lambda h:h,
    combine_docs_chain_kwargs={"prompt": prompt_doc})

while True:
    # Take input query from user 
    question = input("Enter your query: ")
    if question != "exit":
        with get_openai_callback() as cb:
            result = model({'question': question})
            print(f'Spent a total of {cb.total_tokens} tokens')
        print("Answer : ", result['answer'])
        print("----------------------------------------------")
    
    else:
        # Flush all history
        message_history.clear()
        # print(memory.return_messages) 
        # print(memory.buffer)
        # print(memory.chat_memory.messages)
        # print(message_history.messages)
        # print(message_history.messages)
        break