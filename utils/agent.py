from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.chains import LLMChain, RetrievalQA
from langchain.chains.summarize import load_summarize_chain
from . import *
from utils.nlp_trainers import LDATrainer
from utils.chain_utils import *
from langchain.agents import LLMSingleActionAgent, AgentExecutor
import asyncio

class ContextBasedGeneratorAgent:
    def __init__(self, pdf_paths, k=5) -> None:
        self.prompt_template = """You are a document creator that creates visually pleasing html based on prompts and documents which provide context about the prompt. You have access to the following tools:

        {tools}

        You are also given a summary of relevant parts of documents.

        The summary and search results are based on *people's* views on various topics: you must rephrase them as a new person's view. Do not copy them as-is. 
        You may include css, and up to 3 images in the html script. The image "alt" tag will be used as description for an image generation model to generate an image. "src" tag should be an empty string and description should be in English. Only add images if necessary or asked in prompt.

        Use the following format:
        Prompt: the input for creating the document
        Summary: the summary of the documents
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Task Completed: Yes

        Begin!

        Prompt: {input}
        Summary: {summary}
        {agent_scratchpad}
        """
        self.k = 5
        self.llm = OpenAI(model_name="text-davinci-003", max_tokens=1750, temperature=0.0)
        print("creating tools")
        self.db_tool = DatabaseTool(pdf_paths=pdf_paths)
        self.db = self.db_tool.get_db()
        qa = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=self.db.as_retriever()
        )
        self.writer_tool = WriterTool()
        print("tools created")
        qa_tool = Tool(
            name="custom search",
            func=qa.run,
            description="Useful for when you need to answer questions about the documents given.",
        ),
        self.tools = [self.db_tool.tool, self.writer_tool.tool]
    
    def generate_chain_response(self, prompt):
        summary_chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        docs = self.get_top_k_documents(prompt)
        with open("docs.log", "w") as f:
            for doc in docs:
                f.write(doc.page_content)
                f.write("\n============\n")
        print("Summarising documents")
        summary = summary_chain.run(docs)
        print("Summarised documents: ", summary, "========", sep="\n")

        prompt = CustomPromptTemplate(
            template=self.prompt_template,
            tools=self.tools,
            summary=summary,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"]
        )
        llm_chain = LLMChain(llm=self.llm, prompt=prompt, verbose=True)
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain, 
            output_parser=CustomOutputParser(),
            # We use "Observation" as our stop sequence so it will stop when it receives Tool output
            # If you change your prompt template you'll need to adjust this as well
            stop=["\nObservation:"], 
            allowed_tools=[tool.name for tool in self.tools]
        )
        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools, verbose=True)
        res = agent_executor.run(prompt=prompt, input=prompt, summary=summary)
        output = self.writer_tool.get_html()
        return output

    def get_top_k_documents(self, prompt):
        assert self.db is not None, "Database not initialized"
        k = self.k
        prompt_result = self.db.similarity_search_with_score(prompt, k=k)
        
        docs = []
        for result in prompt_result:
            score = result[1]
            if(score >= 0.5):
                break
            docs.append(result[0])
        
        if(len(docs) < 1):
            print("No documents found with similarity score less than 0.5. Looking for generic results.")
            docs = self.get_generic_results()
        else:
            print("Found documents with similarity score less than 0.5: returning")
        
        return docs
    
    def get_generic_results(self):
        # TODO: optimize this
        k=min(self.k, self.max_search_len)
        # docs = self.db.max_marginal_relevance_search(
        #           ' ', k=k, lambda_mult=0.0)
        print("Creating prompts based on LDA keywords")
        text_list = [text.page_content for text in self.titles]
        lda = LDATrainer(k, text_list, passes=10)
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
    
    async def summarise(self, texts):
        return await self.summary_chain.arun(texts)
    
    async def _generate_chain_response_from_inputs(self, inputs):
        return await self.chain.aapply(inputs)