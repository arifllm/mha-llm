from langchain_core.prompts.prompt import PromptTemplate

template = """
The following tool combines the power of AI-powered conversation with creative expression tools to empower individuals in their journey toward mental well-being. It's crucial to remember that this application should never be a substitute for professional medical advice or therapy.

Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.


{context}

Question: {question}
Helpful Answer:
"""

prompt_template = PromptTemplate(
    input_variables=['text'], 
    template=template
)