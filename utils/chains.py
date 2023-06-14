from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from . import *

class ContextBasedGenerator:
    def __init__(self, pdf_path) -> None:
        prompt_template = """You are a document creator that creates html files based on prompts and context, which shall provide details required for the job. The output should be a valid and visually pleasing html. You may include css in the html script. Now create a document based on the context and prompt given below:
        Context: {context}
        Prompt: {prompt}
        html:"""
        # self.summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
        self.PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "prompt"]
        )
        self.llm = OpenAI(model_name="text-davinci-003", max_tokens=3500, temperature=0.0)
        self.chain = LLMChain(llm=self.llm, prompt=self.PROMPT)
        self.db = self.generate_db_from_pdf(pdf_path)
    
    def generate_db_from_pdf(self, pdf_path):
        loader = PyMuPDFLoader(pdf_path)
        document = loader.load()
        text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=1024, chunk_overlap=50)
        texts = text_splitter.split_documents(document)

        vectordb = Chroma.from_documents(documents=texts, 
                                        embedding=OpenAIEmbeddings(),
                                        persist_directory=db_dir)
        vectordb.persist()
        return vectordb

    def generate_chain_response(self, prompt):
        docs = self.db.max_marginal_relevance_search(
                  ' ', k=10, lambda_mult=0.0) # get the top x documents based mostly on diversity
        # strings = self.db.get()["documents"]
        # docs = [Document(page_content=string) for string in strings]
        # summarize_chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        # summary = summarize_chain.run(docs)
        # docs = self.db.max_marginal_relevance_search(
        #         summary, k=5, lambda_mult=0.5) # get the top x documents based on summary
        #open a log file and write the docs to it
        docs.sort(key=lambda x: len(x.page_content), reverse=True)
        with open("docs.log", "w") as f:
            for doc in docs:
                f.write(doc.page_content)
                f.write("\n============")
        # raise Exception("stop")
        inputs = [{"context": doc.page_content, "prompt": prompt} for doc in docs]
        return self.chain.apply(inputs)
