import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai import OpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from chains import qa

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')


# chat_history = []

# question = "Which yoga is better for mental health?"
# result = qa({"question": question, "chat_history": chat_history})
# chat_history.extend([(question, result["answer"])])
# print(result['answer'])


# question = "How often do we need to do it?"
# result = qa({"question": question, "chat_history": chat_history})
# chat_history.extend([(question, result["answer"])])
# print(result['answer'])

# print(chat_history)

# question = "I am a 24 year old male, now tell me"
# result = qa({"question": question, "chat_history": chat_history})
# chat_history.extend([(question, result["answer"])])
# print(result['answer'])

def main(question, chat_history):

    result = qa({"question": question, "chat_history": chat_history})
    chat_history.extend([(question, result["answer"])])
    
    return result['answer'], chat_history

if __name__ == "__main__":
    chat_history = []
    question = input("\nHi there! How may I help you ?\n")

    while True:
        output, chat_history = main(question, chat_history)
        print("\nAnswer : ", output)
        # print("\nChat History : ", chat_history)
        question = input("\n--------------------------\n\nDo you have any more questions ? If not then just type 'No'\n")
        if question.lower() == "no":
            print("Thanks! It was nice talking to you :) \nHave a nice Day!\nBye!")
            break
