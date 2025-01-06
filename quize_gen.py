from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Dict
import os


class QuizQuestion(BaseModel):
    """
    Structured model for quiz questions and answers.
    """
    question: str = Field(description="The quiz question")
    options: List[str] = Field(description="List of answer options, including the correct one and incorrect alternatives")
    correct_answer: str = Field(description="The correct answer to the question")


class QuizSet(BaseModel):
    """
    Collection of quiz questions.
    """
    questions: List[QuizQuestion] = Field(description="List of quiz questions with their options and correct answers")


def generate_quiz_questions(llm, docs: str) -> List[Dict[str, str]]:
    """
    Generate quiz questions from provided text documentation.
    Returns a list of dictionaries, each containing a question, options, and correct answer.
    """
    output_parser = JsonOutputParser(pydantic_object=QuizSet)

    prompt = PromptTemplate(
        template="""
        You are a quiz generator tasked with creating questions based on the following text.
        Generate 5 distinct questions, each with one correct answer and two plausible but incorrect answers.

        Text to analyze:
        {input_text}

        {format_instructions}

        Generate questions that:
        - Test understanding of key concepts
        - Have clear, unambiguous correct answers
        - Include plausible but clearly incorrect alternative answers
        - Cover different aspects of the provided text

        Return the questions in a structured JSON format where:
        - Each question has a "question" field
        - An "options" field containing a list of answers (1 correct and 3 incorrect answers)
        - A "correct_answer" field that explicitly states the correct answer
        """,
        input_variables=["input_text"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )

    chain = prompt | llm | output_parser

    try:
    #     # Generate questions using the LLM
        result = chain.invoke({"input_text": docs})
        return result

    except Exception as e:
        print(f"Error in quiz generation: {e}")
        return []


