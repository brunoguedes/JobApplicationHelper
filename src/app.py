import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import html2text

from llms import LLMs
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 
from langchain.memory import ConversationBufferMemory

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# Required by Streamlit hosting:
os.system("playwright install")

class App:
    def read_file_content(self, file_path):
        try:
            if file_path.endswith('.pdf'):
                output_string = StringIO()
                with open(file_path, 'rb') as file:
                    parser = PDFParser(file)
                    doc = PDFDocument(parser)
                    rsrcmgr = PDFResourceManager()
                    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    for page in PDFPage.create_pages(doc):
                        interpreter.process_page(page)
                return output_string.getvalue()
            else:
                with open(file_path, 'r') as file:
                    content = file.read()
                    return content
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except IOError:
            print(f"An error occurred while reading the file: {file_path}")
            return None

    def extract_text_from_url(self, url):
        loader=AsyncChromiumLoader([url])
        html_content = loader.load()
        html2text_transformer = Html2TextTransformer()
        docs_transformed = html2text_transformer.transform_documents(html_content)
        content_text = []
        for doc in docs_transformed:
            page_content = html2text.html2text(doc.page_content)
            content_text.append(page_content)
        return content_text
    
    def job_ad_content(self, url_input, job_ad_content_input):
        page_content = ""
        if url_input:
            page_content = self.extract_text_from_url(url_input)   
        elif job_ad_content_input:
            page_content = job_ad_content_input
        else:
            page_content = None
        return page_content

    def summarize(self, job_ad_content, llm):
        if job_ad_content:
            summarize_job_prompt = PromptTemplate(
                input_variables = ['job_ad_content'], 
                template = """
                    Act as a skilled Tech Recruiter Analyst specialized in identifying key requirements from job ads. The result of your work will help, other Recruiters from your team, to identify the ideal candidate for a job position.
                    Your task is to extract ALL requirements from a given job position ad. The steps to complete the task are:
                        1. Read carefully the ad of the job position.
                        2. Extract ALL the requirements of the job position.
                        3. Generate a bullet point list, with ALL the requirements.
                    
                    IMPORTANT: All information you include in your output, should strictly come from the job ad. YOU MUST NOT INCLUDE ANYTHING ELSE.

                    Here is the is the ad: 
                    ```
                    {job_ad_content}
                    ```
                """
            )

            # Memory 
            job_ad_summary_memory = ConversationBufferMemory(input_key='job_ad_content', memory_key='chat_history')

            summarize_job_chain = LLMChain(llm=llm, prompt=summarize_job_prompt, verbose=True, output_key='job_requirements_summary', memory=job_ad_summary_memory)

            job_requirements_summary = summarize_job_chain.run(job_ad_content)
            return job_requirements_summary
        else:
            return None

    def generate_cv_summary(self, job_requirements_summary, cv_content, llm):
        if job_requirements_summary and cv_content is not None:
            cv_summary_prompt = PromptTemplate(
                input_variables = ['job_requirements_summary', 'cv_content'], 
                template = """
                    Act as a skilled copywriter specialized in writing summaries for candidates applying for jobs.
                    Your task is to write customized cv summaries that highlights candidates skills and education, which matches the requirements of the advertized job position.
                    The steps to complete the task are:
                        1. Read carefully the job position requirements bellow:
                        ```
                        {job_requirements_summary}
                        ```

                        2. Read carefully the candidate cv bellow:
                        ```
                        {cv_content}
                        ```
                        
                        3. write the cv summary, highlighting the candidates skills and education, which matches the requirements of the advertized job position.
                    
                    IMPORTANT:
                    - All information you include in your output, should strictly come from the candidate's cv. YOU MUST NOT INCLUDE ANYTHING ELSE.
                    - The summary MUST have between 100 and 200 words.
                """
            )
            cv_summary_memory = ConversationBufferMemory(input_key='job_requirements_summary', memory_key='chat_history')
            cv_summary_chain = LLMChain(llm=llm, prompt=cv_summary_prompt, verbose=True, output_key='cv_summary', memory=cv_summary_memory)
            cv_summary = cv_summary_chain.run(job_requirements_summary=job_requirements_summary, cv_content=cv_content)
            return cv_summary
        else:
            return None

    def generate_cover_letter(self, job_requirements_summary, cv_content, cover_letter_sample, candidate_observations, llm):
        if job_requirements_summary and cover_letter_sample is not None:
            cover_letter_prompt = PromptTemplate(
                input_variables = ['job_requirements_summary', 'cv_content', 'cover_letter_sample', 'candidate_observations'], 
                template = """
                    Act as a skilled copywriter specialized in writing cover letters for candidates applying for jobs.
                    Your task is to write customized cover letters, that describes how the candidate progress in his career, highlighting the skills and education, which matches the requirements of the advertized job position.
                    The steps to complete the task are:
                        1. Read carefully the job position requirements bellow:
                        ```
                        {job_requirements_summary}
                        ```

                        2. Read carefully the candidate cv bellow:
                        ```
                        {cv_content}
                        ```

                        3. Read carefully the candidate sample cover letter bellow:
                        ```
                        {cover_letter_sample}
                        ```

                        4. Read carefully the candidate observations bellow:
                        ```
                        {candidate_observations}
                        ``` 
                        
                        5. Write the cover letter, using the candidate's cv, sample cover letter and observations, highlighting the candidates skills, experience and education, which matches the requirements of the advertized job position.
                    
                    IMPORTANT: All information you include in your output, should strictly come from the candidate's cv. YOU MUST NOT INCLUDE ANYTHING ELSE.
                """
            )
            cover_letter_memory = ConversationBufferMemory(input_key='job_requirements_summary', memory_key='chat_history')
            cover_letter_chain = LLMChain(llm=llm, prompt=cover_letter_prompt, verbose=True, output_key='cover_letter', memory=cover_letter_memory)
            cover_letter = cover_letter_chain.run(
                job_requirements_summary=job_requirements_summary,
                cv_content=cv_content,
                cover_letter_sample=cover_letter_sample,
                candidate_observations=candidate_observations
            )
            return cover_letter
        else:
            return None
        
    def run(self):
        # Read Input Files
        cv_path = './input/candidate_cv.pdf'
        cv_content = self.read_file_content(cv_path)
        cover_letter_path = './input/cover_letter_sample.pdf'
        cover_letter_sample = self.read_file_content(cover_letter_path)

        # Input Fields
        st.title('Job Application Helper')
        url_input = st.text_input('paste the url of the position you are interested here')
        st.subheader('or')
        job_ad_content_input = st.text_area('paste the job ad content here', height=300)
        job_ad_content = self.job_ad_content(url_input = url_input, job_ad_content_input = job_ad_content_input)

        if job_ad_content and cv_content is not None and cover_letter_sample is not None:
            try:
                llms = LLMs()
                job_requirements_summary = self.summarize(job_ad_content=job_ad_content, llm=llms.claude)
                with st.expander('Extracted Text'):
                    st.write(job_ad_content)

                st.subheader('Job Requirements:')
                st.write(job_requirements_summary)

                st.subheader('Based on the job requirements, add any additional instructions bellow:')
                candidate_observations = st.text_area('additional instructions', height=300)

                st.subheader('CV Summary:')
                cv_summary = None
                if st.button('Generate CV Summary'):
                    cv_summary = self.generate_cv_summary(
                        job_requirements_summary=job_requirements_summary,
                        cv_content=cv_content,
                        llm=llms.claude
                    )
                st.write(cv_summary)

                st.subheader('Cover Letter:')
                cover_letter = None
                if st.button('Generate Cover Letter'):
                    cover_letter = self.generate_cover_letter(
                        job_requirements_summary=job_requirements_summary,
                        cv_content=cv_content,
                        cover_letter_sample=cover_letter_sample,
                        candidate_observations=candidate_observations,
                        llm=llms.claude
                    )
                st.write(cover_letter)

                # with st.expander('CV Summary History'): 
                #     st.info(cv_summary_memory.buffer)

                # with st.expander('Cover Letter History'): 
                #     st.info(cover_letter_memory.buffer)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.run()
