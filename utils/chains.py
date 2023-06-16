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
from utils.nlp_trainers import LDATrainer

class ContextBasedGenerator:
    def __init__(self, pdf_paths=None) -> None:
        prompt_template = """You are a document creator that creates html files based on prompts and context, which shall provide details required for the job. The output should be a valid and visually pleasing html. The content in the document generated must be standalone(i.e., it should only explicitly refer to another context or conversation). You may include css, and up to 2 images in the html script. The image "alt" tag will be used as description for an image generation model to generate an image. "src" tag should be an empty string and description should be in English. Now create a document based on the context and prompt given below:
        Context: {context}
        Prompt: {prompt}
        html:"""
        # self.summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
        self.PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "prompt"]
        )
        self.llm = OpenAI(model_name="text-davinci-003", max_tokens=3450, temperature=0.0)
        self.chain = LLMChain(llm=self.llm, prompt=self.PROMPT)
        self.text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=1024, chunk_overlap=50)
        if(pdf_paths is not None):
            self.generate_db_from_pdf(pdf_paths)
    
    def generate_db_from_pdf(self, pdf_paths):
        texts = []
        titles = []
        for pdf_path in pdf_paths:
            loader = PyMuPDFLoader(pdf_path)
            document = loader.load()
            titles.append(document[0])
            texts+=self.text_splitter.split_documents(document)
        self.max_search_len = len(texts)
        self.texts = texts
        self.titles = titles

    @property
    def db(self):
        vectordb = Chroma.from_documents(documents=self.texts, 
                                        embedding=OpenAIEmbeddings())
        return vectordb

    def generate_chain_response(self, prompt):
        docs = self.get_top_k_documents(prompt)
        with open("docs.log", "w") as f:
            for doc in docs:
                f.write(doc.page_content)
                f.write("\n============")
        # raise Exception("stop")
        inputs = [{"context": doc.page_content, "prompt": prompt} for doc in docs]
        return self.chain.apply(inputs)

    def get_top_k_documents(self, prompt, k=5):
        assert self.db is not None, "Database not initialized"
        
        prompt_result = self.db.similarity_search_with_score(prompt, k=k)
        
        docs = []
        for result in prompt_result:
            score = result[1]
            if(score >= 0.5):
                break
            docs.append(result[0])
        
        if(len(docs) < 1):
            print("No documents found with similarity score less than 0.5. Looking for generic results.")
            docs = self.get_generic_results(k)
        else:
            print("Found documents with similarity score less than 0.5: returning")
        
        return docs
    
    def get_generic_results(self, k=5):
        # TODO: optimize this
        k=min(k, self.max_search_len)
        # docs = self.db.max_marginal_relevance_search(
        #           ' ', k=k, lambda_mult=0.0)
        print("Creating prompts based on LDA keywords")
        text_list = [text.page_content for text in self.titles]
        lda = LDATrainer(5, text_list, passes=10)
        smart_queries = lda.make_smart_queries()
        print("Queries: ", smart_queries, sep="\n")
        docs = []
        for query in smart_queries:
            prompt_result = self.db.similarity_search_with_score(query, k=1)
            for result in prompt_result:
                score = result[1]
                if(score >= 0.5):
                    break
                docs.append(result[0])
        print("returning generic results")
        return docs