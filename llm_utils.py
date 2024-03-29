import random
import streamlit as st
import os
import json
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro")

def get_randomized_options(options):
    correct_answer = options[0]
    random.shuffle(options)
    return options, correct_answer

# st.title("📚🧠Youtube Video Quiz App")


# name = st.text_input("👩‍💼 Enter your name: ")


def question_data(url):
    # with st.spinner("Loading youtube content..."):
    loader = YoutubeLoader.from_youtube_url(youtube_url=url, add_video_info=False)
    doc = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
    )
    docs = text_splitter.split_documents(doc)


    que_no = 6

    q = f"""
    You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, you're tasked with designing {que_no} distinct questions. Each of these questions will be accompanied by 3 possible answers: one correct answer and two incorrect ones. 
    provided text is deliminated in tripple ticks:
    ```{docs}```

    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

    Your output should be shaped as follows:

    1. An outer list that contains {que_no} inner lists.
    2. Each inner list represents a set of question and answers, and it should STRICTLY contains 4 strings in this order:
    - The generated question.
    - The correct answer.
    - The first incorrect answer.
    - The second incorrect answer.

    Your output should mirror this structure:
    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.
    strictly follow this instruction - all options should be different option from any question should match with each other
    """

    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    output = chain.invoke({"query":q})

    return output


url = 'https://youtu.be/zIwLWfaAg-8?si=nApllc7rPZz3CAx_'
output = question_data(url)



