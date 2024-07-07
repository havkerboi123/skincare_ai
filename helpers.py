from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

llm = OpenAI(temperature=0, openai_api_key="")

# loader = TextLoader('/Users/mhmh/Desktop/p2/skincare/DATA.txt')
# docs = loader.load()

# splitter = RecursiveCharacterTextSplitter()
# chunks = splitter.split_documents(docs)

persist_directory = 'chroma/skin'
embeddings = OpenAIEmbeddings(openai_api_key="")
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)





template = """"Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}
"""
prompt = ChatPromptTemplate.from_template(template)
document_chain = create_stuff_documents_chain(llm, prompt)

user_input=""
retriever = db.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({
    "input": user_input
})


print(response['answer'])

from langchain_openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

def answer_question(input_question):
    # Initialize OpenAI language model
    llm = OpenAI(temperature=0, openai_api_key="")
    
    # Initialize embeddings and Chroma vector store
    embeddings = OpenAIEmbeddings(openai_api_key="")
    db = Chroma(persist_directory='chroma/skin', embedding_function=embeddings)

    # Define the prompt template
    template = """Answer the following question based only on the provided context:
    
    <context>
    {context}
    </context>
    
    Question: {input}
    """
    prompt = ChatPromptTemplate.from_template(template)

    
    document_chain = create_stuff_documents_chain(llm, prompt)

   
    user_input = input_question

    
    retriever = db.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Invoke retrieval chain with user input
    response = retrieval_chain.invoke({
        "input": input_question
    })

    return response['answer']


if __name__ == "__main__":
    input_question = "Your question goes here."
    persist_directory = 'chroma/skin'
    openai_api_key = ""
    
    answer = answer_question(input_question, persist_directory, openai_api_key)
    
