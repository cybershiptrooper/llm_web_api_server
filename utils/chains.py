from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from . import *

class ContextBasedGenerator:
    def __init__(self, pdf_path) -> None:
        prompt_template = """You are a document creator that creates html files based on prompts. The context shall provide details required for the job. The output should be a valid html. You may include css in the html script. Now create a document for the user prompt:
        Context: {context}
        Prompt: {prompt}
        html:"""
        self.PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "prompt"]
        )
        llm = OpenAI(model_name="text-davinci-003", max_tokens=3600, temperature=0.0)
        self.chain = LLMChain(llm=llm, prompt=self.PROMPT)
        self.db = self.generate_db_from_pdf(pdf_path)
    
    def generate_db_from_pdf(self, pdf_path):
        loader = PyMuPDFLoader(pdf_path)
        document = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
        texts = text_splitter.split_documents(document)

        vectordb = Chroma.from_documents(documents=texts, 
                                        embedding=OpenAIEmbeddings(),
                                        persist_directory=db_dir)
        vectordb.persist()
        return vectordb

    def generate_chain_response(self, prompt):
        docs = self.db.similarity_search(prompt, k=3)
        inputs = [{"context": doc.page_content, "prompt": prompt} for doc in docs]
        return self.chain.apply(inputs)

