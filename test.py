import random
import streamlit as st
import os
import json
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from llm_utils import question_data  # Import the function directly


def get_randomized_options(options):
    correct_answer = options[0]
    random.shuffle(options)
    return options, correct_answer

name = st.text_input("👩‍💼 Enter your name: ")
url = st.text_input("🔗 Enter your video url: ")

process = st.toggle("Submit and Process")


# Define the filename you want to check
filename = "quize_data.py"

# Check if the file exists in the current directory
if os.path.isfile(filename):
    print(f"The file '{filename}' exists in the current directory.")
else:
    print(f"The file '{filename}' does not exist in the current directory.")

    output = question_data(url) 
    output_file_name = "quize_data.py"

    # Write the output data to the Python file
    with open(output_file_name, "w") as file:
        file.write("output = ")
        json.dump(output, file)

from quize_data import output


if process:
    st.write(f"Hello, {name}!!")

    score = 0
    total_questions = len(output)
    incorrect_answers = []

    with st.form("quiz_form"):
        for i, question_data in enumerate(output, start=1):
            question, correct_answer, incorrect_answer1, incorrect_answer2 = question_data
            
            # Randomize options
            options, correct_answer = get_randomized_options([correct_answer, incorrect_answer1, incorrect_answer2])
            
            st.write(f"{i}. {question}")

            selected_option = st.radio(f"Choose the correct answer for Question {i}:", options, key=i)
            
            st.session_state[f"selected_option_{i}"] = selected_option

        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        for i, question_data in enumerate(output, start=1):
            correct_answer = question_data[1]
            selected_option = st.session_state[f"selected_option_{i}"]

            if selected_option == correct_answer:
                score += 1
            else:
                incorrect_answers.append(i)

        st.header("🎉Quiz Summary")

        for i in range(total_questions):
            if i+1 in incorrect_answers:
                st.write(f"❌ Question {i+1}: {output[i][0]}")
                st.write(f"Correct ans: {output[i][1]}")
            else:
                st.write(f"✔️ Question {i+1}: {output[i][0]}")
                st.write(f"Correct ans: {output[i][1]}")

        quiz_data = {
            "name": name,
            "questions": output,
            "score": score
        }

        output_file_name = f"result.json"

        if os.path.exists(output_file_name):
            with open(output_file_name, "r") as file:
                existing_data = json.load(file)
            
            existing_data.append(quiz_data)
            
            with open(output_file_name, "w") as file:
                json.dump(existing_data, file)
        else:
            with open(output_file_name, "w") as file:
                json.dump([quiz_data], file)


        if os.path.exists(filename):
            # Delete the file
            os.remove(filename)
            print(f"{filename} deleted successfully.")
        else:
            print(f"{filename} does not exist.")
