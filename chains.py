from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_openai import OpenAI
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from prompt import prompt_template


# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load from disk
db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

retriever = db3.as_retriever(search_type="mmr",
                            search_kwargs={'k': 5, 'fetch_k': 20})

qa = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(temperature=0.9,
               max_tokens=512),
    retriever=retriever,
    return_source_documents=True,
    return_generated_question=True,
)

# custom prompt
qa.combine_docs_chain.llm_chain.prompt = prompt_template